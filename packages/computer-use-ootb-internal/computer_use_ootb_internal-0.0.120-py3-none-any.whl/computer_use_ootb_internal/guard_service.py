# src/computer_use_ootb_internal/guard_service.py
import sys
import os
import time
import logging
import subprocess
import pathlib
import ctypes
import threading # For running server thread
import queue # For queuing commands
import requests # Keep for status reporting back
import servicemanager # From pywin32
import win32serviceutil # From pywin32
import win32service # From pywin32
import win32event # From pywin32
import win32api # From pywin32
import win32process # From pywin32
import win32security # From pywin32
import win32profile # From pywin32
import win32ts # From pywin32 (Terminal Services API)
import win32con
import psutil # For process/user info
from flask import Flask, request, jsonify # For embedded server
from waitress import serve # For serving Flask app
import json # Needed for status reporting

# --- Configuration ---
_SERVICE_NAME = "OOTBGuardService"
_SERVICE_DISPLAY_NAME = "OOTB Guard Service"
_SERVICE_DESCRIPTION = "Background service for OOTB monitoring and remote management (Server POST mode)."
_PACKAGE_NAME = "computer-use-ootb-internal"
_OOTB_MODULE = "computer_use_ootb_internal.app_teachmode"
# --- Server POST Configuration ---
_LISTEN_HOST = "0.0.0.0" # Listen on all interfaces
_LISTEN_PORT = 14000 # Port for server to POST commands TO
# _SHARED_SECRET = "YOUR_SECRET_HERE" # !! REMOVED !! - No secret check implemented now
# --- End Server POST Configuration ---
_SERVER_STATUS_REPORT_URL = "http://52.160.105.102:7000/guard/status" # URL to POST status back TO (Path changed)
_LOG_FILE = pathlib.Path(os.environ['PROGRAMDATA']) / "OOTBGuardService" / "guard_post_mode.log" # Different log file
# --- End Configuration ---

_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=_LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(threadName)s: %(message)s'
)

# --- Global service instance reference (needed for Flask routes) ---
_service_instance = None

# --- Flask App Definition ---
flask_app = Flask(__name__)

@flask_app.route('/command', methods=['POST'])
def receive_command():
    global _service_instance
    if not _service_instance:
        logging.error("Received command but service instance is not set.")
        return jsonify({"error": "Service not ready"}), 503

    # --- Authentication REMOVED ---
    # secret = request.headers.get('X-Guard-Secret')
    # if not secret or secret != _SHARED_SECRET:
    #     logging.warning(f"Unauthorized command POST received (Invalid/Missing X-Guard-Secret). Remote Addr: {request.remote_addr}")
    #     return jsonify({"error": "Unauthorized"}), 403
    # --- End Authentication REMOVED ---

    if not request.is_json:
        logging.warning("Received non-JSON command POST.")
        return jsonify({"error": "Request must be JSON"}), 400

    command = request.get_json()
    logging.info(f"Received command via POST: {command}")

    # Basic validation
    action = command.get("action")
    command_id = command.get("command_id", "N/A") # Use for status reporting
    if not action:
         logging.error(f"Received command POST with no action: {command}")
         return jsonify({"error": "Missing 'action' in command"}), 400

    # Queue the command for processing in a background thread
    _service_instance.command_queue.put((command_id, command))
    logging.info(f"Queued command {command_id} ({action}) for processing.")

    return jsonify({"message": f"Command {command_id} received and queued"}), 202 # Accepted

# --- Helper Functions --- Only logging helpers needed adjustments
def get_python_executable():
    python_exe = sys.executable
    if " " in python_exe and not python_exe.startswith('"'):
        python_exe = f'"{python_exe}"'
    return python_exe

def get_pip_executable():
    """Tries to locate the pip executable in the same environment."""
    try:
        current_python = sys.executable
        log_info(f"get_pip_executable: sys.executable = {current_python}")
        python_path = pathlib.Path(current_python)
        # Common location is ../Scripts/pip.exe relative to python.exe
        pip_path = python_path.parent / "Scripts" / "pip.exe"
        log_info(f"get_pip_executable: Checking for pip at {pip_path}")

        if pip_path.exists():
            log_info(f"get_pip_executable: pip.exe found at {pip_path}")
            # Quote if necessary
            pip_exe = str(pip_path)
            if " " in pip_exe and not pip_exe.startswith('"'):
                pip_exe = f'"{pip_exe}"'
            return pip_exe
        else:
            log_error(f"get_pip_executable: pip.exe NOT found at {pip_path}. Falling back to 'python -m pip'.")
            # Fallback is intended here
            pass # Explicitly pass to reach the fallback return outside the else

    except Exception as e:
        log_error(f"get_pip_executable: Error determining pip path: {e}", exc_info=True)
        log_error("get_pip_executable: Falling back to 'python -m pip' due to error.")
    
    # Fallback return statement if 'exists' is false or an exception occurred
    return f"{get_python_executable()} -m pip"

def log_info(msg):
    thread_name = threading.current_thread().name
    full_msg = f"[{thread_name}] {msg}"
    logging.info(full_msg)
    try:
        # Only log to event log from main service thread or known non-daemon threads if possible
        # Trying from waitress/flask threads might cause issues.
        # For simplicity, maybe remove event log integration or make it conditional.
        if threading.current_thread().name in ["MainThread", "CommandProcessor"]: # Example condition
             servicemanager.LogInfoMsg(str(full_msg))
    except Exception as e:
        logging.warning(f"Could not write info to Windows Event Log: {e}")

def log_error(msg, exc_info=False):
    thread_name = threading.current_thread().name
    full_msg = f"[{thread_name}] {msg}"
    logging.error(full_msg, exc_info=exc_info)
    try:
        if threading.current_thread().name in ["MainThread", "CommandProcessor"]:
            servicemanager.LogErrorMsg(str(full_msg))
    except Exception as e:
        logging.warning(f"Could not write error to Windows Event Log: {e}")

# --- PowerShell Task Scheduler Helpers ---

_TASK_NAME_PREFIX = "OOTB_UserLogon_"

def run_powershell_command(command, log_output=True):
    """Executes a PowerShell command and handles output/errors. Returns True on success."""
    # Use log_info from the service instance if available, otherwise use root logger
    logger = _service_instance.log_info if _service_instance else logging.info
    error_logger = _service_instance.log_error if _service_instance else logging.error
    logger(f"Executing PowerShell: {command}")
    try:
        # Using encoding important for non-ASCII usernames/paths
        result = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
            capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore'
        )
        if log_output and result.stdout:
            logger(f"PowerShell STDOUT:\n{result.stdout.strip()}")
        if log_output and result.stderr:
            logger(f"PowerShell STDERR:\n{result.stderr.strip()}") # Log stderr as info
        return True
    except FileNotFoundError:
        error_logger("'powershell.exe' not found. Cannot manage scheduled tasks.")
        return False
    except subprocess.CalledProcessError as e:
        error_logger(f"PowerShell command failed (Exit Code {e.returncode}):")
        error_logger(f"  Command: {e.cmd}")
        if e.stdout: error_logger(f"  STDOUT: {e.stdout.strip()}")
        if e.stderr: error_logger(f"  STDERR: {e.stderr.strip()}")
        return False
    except Exception as e:
        error_logger(f"Unexpected error running PowerShell: {e}", exc_info=True)
        return False

def create_or_update_logon_task(username, task_command, python_executable):
    """Creates or updates a scheduled task to run a command at user logon."""
    logger = _service_instance.log_info if _service_instance else logging.info
    error_logger = _service_instance.log_error if _service_instance else logging.error
    task_name = f"{_TASK_NAME_PREFIX}{username}"
    # Escape single quotes in paths and commands for PowerShell
    safe_python_exe = python_executable.replace("'", "''")
    # Ensure task_command is just the arguments, not the python exe itself
    command_parts = task_command.split(' ', 1)
    if len(command_parts) > 1 and command_parts[0] == python_executable:
         safe_task_command_args = command_parts[1].replace("'", "''")
    else: # Fallback if task_command doesn't start with python_exe
         safe_task_command_args = task_command.replace(python_executable, "").strip().replace("'", "''")

    safe_task_name = task_name.replace("'", "''")
    safe_username = username.replace("'", "''") # Handle usernames with quotes?

    action = f"$Action = New-ScheduledTaskAction -Execute '{safe_python_exe}' -Argument '{safe_task_command_args}'"
    trigger = f"$Trigger = New-ScheduledTaskTrigger -AtLogOn -User '{safe_username}'"
    principal = f"$Principal = New-ScheduledTaskPrincipal -UserId '{safe_username}' -LogonType Interactive"
    settings = "$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -DontStopOnIdleEnd -ExecutionTimeLimit ([System.TimeSpan]::Zero) -RunOnlyIfNetworkAvailable:$false"

    command = f"""
    try {{
        {action}
        {trigger}
        {principal}
        {settings}
        Register-ScheduledTask -TaskName '{safe_task_name}' -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Force -ErrorAction Stop
        Write-Host "Scheduled task '{safe_task_name}' registered/updated successfully."
    }} catch {{
        Write-Error "Failed to register/update scheduled task '{safe_task_name}': $_"
        exit 1 # Indicate failure
    }}
    """
    success = run_powershell_command(command)
    if success:
        logger(f"Successfully created/updated scheduled task '{task_name}' for user '{username}'.")
    else:
        error_logger(f"Failed to create/update scheduled task '{task_name}' for user '{username}'.")
    return success


def remove_logon_task(username):
    """Removes the logon scheduled task for a user."""
    logger = _service_instance.log_info if _service_instance else logging.info
    task_name = f"{_TASK_NAME_PREFIX}{username}"
    safe_task_name = task_name.replace("'", "''")
    command = f"Unregister-ScheduledTask -TaskName '{safe_task_name}' -Confirm:$false -ErrorAction SilentlyContinue"
    run_powershell_command(command, log_output=False)
    logger(f"Attempted removal of scheduled task '{task_name}' for user '{username}'.")
    return True

# --- End PowerShell Task Scheduler Helpers ---

class GuardService(win32serviceutil.ServiceFramework):
    _svc_name_ = _SERVICE_NAME
    _svc_display_name_ = _SERVICE_DISPLAY_NAME
    _svc_description_ = _SERVICE_DESCRIPTION

    def __init__(self, args):
        global _service_instance
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
        self.server_thread = None
        self.command_queue = queue.Queue()
        self.command_processor_thread = None
        self.session = requests.Session() # For status reporting

        self.python_exe = get_python_executable()
        self.pip_command_base = get_pip_executable()
        self.ootb_command = f"{self.python_exe} -m {_OOTB_MODULE}"
        _service_instance = self # Set global reference

    def SvcStop(self):
        log_info(f"Service stop requested.")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        # Signal the command processor thread to stop
        self.command_queue.put(None) # Sentinel value
        # Signal the main wait loop
        win32event.SetEvent(self.hWaitStop)
        # Stopping waitress gracefully from another thread is non-trivial.
        # We rely on the SCM timeout / process termination for now.
        log_info(f"{_SERVICE_NAME} SvcStop: Stop signaled. Server thread will be terminated by SCM.")


    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        try:
            log_info(f"{_SERVICE_NAME} starting.")
            # Start the command processor thread
            self.command_processor_thread = threading.Thread(
                target=self.process_commands, name="CommandProcessor", daemon=True)
            self.command_processor_thread.start()
            log_info("Command processor thread started.")

            # Start the Flask server (via Waitress) in a separate thread
            self.server_thread = threading.Thread(
                target=self.run_server, name="WebServerThread", daemon=True)
            self.server_thread.start()
            log_info(f"Web server thread started, listening on {_LISTEN_HOST}:{_LISTEN_PORT}.")

            log_info(f"{_SERVICE_NAME} running. Waiting for stop signal.")
            # Keep the main service thread alive waiting for stop signal
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
            log_info(f"{_SERVICE_NAME} received stop signal in main thread.")

        except Exception as e:
            log_error(f"Fatal error in SvcDoRun: {e}", exc_info=True)
            self.SvcStop() # Signal stop if possible
        finally:
            log_info(f"{_SERVICE_NAME} SvcDoRun finished.")


    def run_server(self):
        """Runs the Flask app using Waitress."""
        log_info(f"Waitress server starting on {_LISTEN_HOST}:{_LISTEN_PORT}")
        try:
            serve(flask_app, host=_LISTEN_HOST, port=_LISTEN_PORT, threads=4)
            log_info("Waitress server has stopped.") # Should only happen on shutdown
        except Exception as e:
            log_error(f"Web server thread encountered an error: {e}", exc_info=True)
            # Consider signaling the main thread to stop if the web server fails critically
            # For now, just log the error.


    def process_commands(self):
        """Worker thread to process commands from the queue."""
        log_info("Command processor thread starting.")
        while self.is_running:
            try:
                item = self.command_queue.get(block=True, timeout=1) # Add timeout to check is_running periodically
                if item is None:
                    log_info("Command processor received stop signal.")
                    break # Exit loop

                command_id, command = item
                action = command.get("action")
                target = command.get("target_user", "all_active")
                status = "failed_unknown" # Default

                log_info(f"Dequeued Command ID {command_id}: action='{action}', target='{target}'")

                try:
                    if action == "update":
                        status = self.handle_update()
                    elif action == "stop_ootb":
                        status = self.handle_stop(target)
                    elif action == "start_ootb":
                        status = self.handle_start(target)
                    else:
                        log_error(f"Unknown action in queue: {action}")
                        status = "failed_unknown_action"
                except Exception as handler_ex:
                    log_error(f"Exception processing Command ID {command_id} ({action}): {handler_ex}", exc_info=True)
                    status = "failed_exception"
                finally:
                    self.report_command_status(command_id, status)
                    self.command_queue.task_done()

            except queue.Empty:
                # Timeout occurred, just loop again and check self.is_running
                continue
            except Exception as e:
                 log_error(f"Error in command processing loop: {e}", exc_info=True)
                 if self.is_running:
                     time.sleep(5)

        log_info("Command processor thread finished.")


    def report_command_status(self, command_id, status, details=""):
        """Sends command status back to the server."""
        if not _SERVER_STATUS_REPORT_URL:
            log_error("No server status report URL configured. Skipping report.")
            return

        payload = {
            "command_id": command_id,
            "status": status,
            "details": details,
            "machine_id": os.getenv('COMPUTERNAME', 'unknown_guard')
        }
        log_info(f"Reporting status for command {command_id}: {status}")
        try:
            response = self.session.post(_SERVER_STATUS_REPORT_URL, json=payload, timeout=15)
            response.raise_for_status()
            log_info(f"Status report for command {command_id} accepted by server.")
        except requests.exceptions.RequestException as e:
            log_error(f"Failed to report status for command {command_id}: {e}")
        except Exception as e:
             log_error(f"Unexpected error reporting status for command {command_id}: {e}", exc_info=True)

    # --- Command Handlers --- Copying full implementation from previous version

    def handle_update(self):
        log_info("Executing OOTB update...")
        if not self.pip_command_base:
            log_error("Cannot update: pip command not found.")
            return "failed_pip_not_found"

        update_command = f"{self.pip_command_base} install --upgrade --no-cache-dir {_PACKAGE_NAME}"
        log_info(f"Running update command: {update_command}")
        try:
            result = subprocess.run(update_command, shell=True, capture_output=True, text=True, check=True, timeout=300, encoding='utf-8')
            log_info(f"Update successful: \nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
            return "success"
        except subprocess.CalledProcessError as e:
            log_error(f"Update failed (Exit Code {e.returncode}):\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}")
            return f"failed_exit_{e.returncode}"
        except subprocess.TimeoutExpired:
             log_error(f"Update command timed out.")
             return "failed_timeout"
        except Exception as e:
            log_error(f"Unexpected error during update: {e}", exc_info=True)
            return "failed_exception"


    def _get_ootb_processes(self, target_user="all_active"):
        ootb_procs = []
        target_pid_list = []
        try:
            target_users = set()
            if target_user == "all_active":
                 for user_session in psutil.users():
                      username = user_session.name.split('\\')[-1]
                      target_users.add(username.lower())
            else:
                 target_users.add(target_user.lower())

            log_info(f"Searching for OOTB processes for users: {target_users}")

            python_exe_path = self.python_exe.strip('"') # Get unquoted path for comparison

            for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline', 'exe']):
                try:
                    pinfo = proc.info
                    proc_username = pinfo['username']
                    if proc_username:
                        proc_username = proc_username.split('\\')[-1].lower()

                    if proc_username in target_users:
                        cmdline = ' '.join(pinfo['cmdline']) if pinfo['cmdline'] else ''
                        # Check if the process executable matches our python path AND module is in cmdline
                        if pinfo['exe'] and pinfo['exe'] == python_exe_path and _OOTB_MODULE in cmdline:
                            log_info(f"Found matching OOTB process: PID={pinfo['pid']}, User={pinfo['username']}, Cmd={cmdline}")
                            ootb_procs.append(proc)
                            target_pid_list.append(pinfo['pid'])

                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            log_info(f"Found {len(ootb_procs)} OOTB process(es) matching criteria: {target_pid_list}")
        except Exception as e:
             log_error(f"Error enumerating processes: {e}", exc_info=True)
        return ootb_procs


    def handle_stop(self, target_user="all_active"):
        log_info(f"Executing stop OOTB for target '{target_user}'...")
        stop_results = {} # Track results per user {username: (task_status, immediate_status)}
        failed_users = set()

        try:
             # --- Get target users and active sessions ---
            active_sessions = {} # user_lower: session_id
            # No need for all_system_users for stop, we only care about active or the specific target
            try:
                 sessions = win32ts.WTSEnumerateSessions(win32ts.WTS_CURRENT_SERVER_HANDLE)
                 for session in sessions:
                     if session['State'] == win32ts.WTSActive:
                         try:
                             user = win32ts.WTSQuerySessionInformation(win32ts.WTS_CURRENT_SERVER_HANDLE, session['SessionId'], win32ts.WTSUserName)
                             if user:
                                 active_sessions[user.lower()] = session['SessionId']
                         except Exception as query_err:
                             log_error(f"Could not query session {session['SessionId']} during stop: {query_err}")
            except Exception as user_enum_err:
                  log_error(f"Error enumerating users/sessions during stop: {user_enum_err}", exc_info=True)
                  return "failed_user_enumeration"

            log_info(f"Stop target: '{target_user}'. Active sessions: {active_sessions}")

            target_users_normalized = set()
            if target_user == "all_active":
                  # Target only currently active users for stop all
                  target_users_normalized = set(active_sessions.keys())
                  log_info(f"Stop targeting all active users: {target_users_normalized}")
            else:
                  # Target the specific user, regardless of active status (for task removal)
                  normalized_target = target_user.lower()
                  target_users_normalized.add(normalized_target)
                  log_info(f"Stop targeting specific user: {normalized_target}")

            if not target_users_normalized:
                  log_info("No target users identified for stop.")
                  return "failed_no_target_users" # Or success if none were targeted?

            # --- Process each target user ---
            for user in target_users_normalized:
                 task_removed_status = "task_unknown"
                 immediate_stop_status = "stop_not_attempted"
                 stopped_count = 0

                 log_info(f"Processing stop for user '{user}'...")

                 # 1. Always try to remove the scheduled task
                 try:
                     # remove_logon_task always returns True for now, just logs attempt
                     remove_logon_task(user)
                     task_removed_status = "task_removed_attempted"
                 except Exception as task_err:
                      log_error(f"Exception removing scheduled task for {user}: {task_err}", exc_info=True)
                      task_removed_status = "task_exception"
                      failed_users.add(user)
                      # Continue to try and stop process if active

                 # 2. If user is active, try to terminate process
                 is_active = user in active_sessions

                 if is_active:
                     immediate_stop_status = "stop_attempted"
                     log_info(f"User '{user}' is active. Attempting to terminate OOTB process(es)...")
                     # Pass the specific username to _get_ootb_processes
                     procs_to_stop = self._get_ootb_processes(user)

                     if not procs_to_stop:
                         log_info(f"No running OOTB processes found for active user '{user}'.")
                         immediate_stop_status = "stop_skipped_not_running"
                     else:
                         log_info(f"Found {len(procs_to_stop)} process(es) for user '{user}' to stop.")
                         for proc in procs_to_stop:
                             try:
                                 pid = proc.pid # Get pid before potential termination
                                 username = proc.info.get('username', 'unknown_user')
                                 log_info(f"Terminating process PID={pid}, User={username}")
                                 proc.terminate()
                                 try:
                                     proc.wait(timeout=3)
                                     log_info(f"Process PID={pid} terminated successfully.")
                                     stopped_count += 1
                                 except psutil.TimeoutExpired:
                                     log_error(f"Process PID={pid} did not terminate gracefully, killing.")
                                     proc.kill()
                                     stopped_count += 1
                             except psutil.NoSuchProcess:
                                  log_info(f"Process PID={pid} already terminated.")
                                  # Don't increment stopped_count here as we didn't stop it now
                             except psutil.AccessDenied:
                                 log_error(f"Access denied trying to terminate process PID={pid}.")
                                 failed_users.add(user) # Mark user as failed if stop fails
                             except Exception as e:
                                 log_error(f"Error stopping process PID={pid}: {e}", exc_info=True)
                                 failed_users.add(user) # Mark user as failed

                         # Determine status based on how many were found vs stopped
                         if user in failed_users:
                              immediate_stop_status = f"stop_errors_terminated_{stopped_count}_of_{len(procs_to_stop)}"
                         elif stopped_count == len(procs_to_stop):
                              immediate_stop_status = f"stop_success_terminated_{stopped_count}"
                         else: # Should ideally not happen if NoSuchProcess doesn't count
                              immediate_stop_status = f"stop_partial_terminated_{stopped_count}_of_{len(procs_to_stop)}"

                 else: # User not active
                     log_info(f"User '{user}' is not active. Skipping immediate process stop (task removal attempted).")
                     immediate_stop_status = "stop_skipped_inactive"

                 # Record final results for this user
                 stop_results[user] = (task_removed_status, immediate_stop_status)


            # --- Consolidate status ---
            total_processed = len(target_users_normalized)
            final_status = "partial_success" if failed_users else "success"
            if not stop_results: final_status = "no_targets_processed"
            if len(failed_users) == total_processed and total_processed > 0 : final_status = "failed"

            log_info(f"Finished stopping OOTB. Overall Status: {final_status}. Results: {stop_results}")
            try:
                details = json.dumps(stop_results)
            except Exception:
                details = str(stop_results) # Fallback
            return f"{final_status}::{details}" # Use :: as separator

        except Exception as e:
             log_error(f"Error during combined stop OOTB process: {e}", exc_info=True)
             return "failed_exception"


    def handle_start(self, target_user="all_active"):
        log_info(f"Executing start OOTB for target '{target_user}'...")
        start_results = {} # Track results per user {username: (task_status, immediate_status)}
        failed_users = set()

        try:
            # --- Get target users and active sessions ---
            active_sessions = {} # user_lower: session_id
            all_system_users = set() # user_lower
            try:
                # Use psutil for system user list, WTS for active sessions/IDs
                for user_session in psutil.users():
                    username_lower = user_session.name.split('\\')[-1].lower()
                    all_system_users.add(username_lower)
                
                sessions = win32ts.WTSEnumerateSessions(win32ts.WTS_CURRENT_SERVER_HANDLE)
                for session in sessions:
                    if session['State'] == win32ts.WTSActive:
                        try:
                            user = win32ts.WTSQuerySessionInformation(win32ts.WTS_CURRENT_SERVER_HANDLE, session['SessionId'], win32ts.WTSUserName)
                            if user:
                                active_sessions[user.lower()] = session['SessionId']
                        except Exception as query_err:
                            log_error(f"Could not query session {session['SessionId']}: {query_err}")
            except Exception as user_enum_err:
                 log_error(f"Error enumerating users/sessions: {user_enum_err}", exc_info=True)
                 return "failed_user_enumeration"

            log_info(f"Found active user sessions: {active_sessions}")

            target_users_normalized = set()
            if target_user == "all_active":
                 # If targeting all_active, only target those CURRENTLY active
                 target_users_normalized = set(active_sessions.keys())
                 log_info(f"Targeting all active users: {target_users_normalized}")
            else:
                 normalized_target = target_user.lower()
                 # Check if the target user actually exists on the system, even if inactive
                 # This check might be complex/unreliable. Rely on task scheduler potentially failing?
                 # Let's assume admin provides a valid username for specific targeting.
                 # if normalized_target in all_system_users: # Removing this check, assume valid user input
                 target_users_normalized.add(normalized_target)
                 log_info(f"Targeting specific user: {normalized_target}")
                 # else:
                 #     log_error(f"Target user '{target_user}' does not appear to exist on this system based on psutil.")
                 #     return "failed_user_does_not_exist"

            if not target_users_normalized:
                 log_info("No target users identified (or none active for 'all_active').")
                 # If target was specific user but they weren't found active, still try task?
                 # Let's proceed to task creation anyway for specific user case.
                 if target_user != "all_active": target_users_normalized.add(target_user.lower())
                 if not target_users_normalized:
                      return "failed_no_target_users"
            
            # --- Check existing processes --- 
            # This check is only relevant for immediate start attempt
            running_procs_by_user = {} # user_lower: count
            try:
                current_running = self._get_ootb_processes("all_active") # Check all
                for proc in current_running:
                    try:
                        proc_username = proc.info.get('username')
                        if proc_username:
                             user_lower = proc_username.split('\\')[-1].lower()
                             running_procs_by_user[user_lower] = running_procs_by_user.get(user_lower, 0) + 1
                    except Exception: pass
            except Exception as e:
                 log_error(f"Error checking existing processes: {e}")
            log_info(f"Users currently running OOTB: {running_procs_by_user}")

            # --- Process each target user ---
            for user in target_users_normalized:
                task_created_status = "task_unknown"
                immediate_start_status = "start_not_attempted"
                token = None # Ensure token is reset/defined

                log_info(f"Processing start for user '{user}'...")

                # 1. Always try to create/update the scheduled task
                try:
                    task_created = create_or_update_logon_task(user, self.ootb_command, self.python_exe)
                    task_created_status = "task_success" if task_created else "task_failed"
                except Exception as task_err:
                     log_error(f"Exception creating/updating scheduled task for {user}: {task_err}", exc_info=True)
                     task_created_status = "task_exception"
                     failed_users.add(user)
                     # Continue to potentially try immediate start IF user is active?
                     # Or maybe skip if task creation failed badly?
                     # Let's skip immediate start if task creation had exception.
                     start_results[user] = (task_created_status, immediate_start_status)
                     continue

                # 2. If user is active AND not already running, try immediate start
                is_active = user in active_sessions
                is_running = running_procs_by_user.get(user, 0) > 0

                if is_active:
                    if not is_running:
                        immediate_start_status = "start_attempted"
                        log_info(f"User '{user}' is active and not running OOTB. Attempting immediate start...")
                        try:
                            session_id = active_sessions[user]
                            token = win32ts.WTSQueryUserToken(session_id)
                            env = win32profile.CreateEnvironmentBlock(token, False)
                            startup = win32process.STARTUPINFO()
                            startup.dwFlags = win32process.STARTF_USESHOWWINDOW
                            startup.wShowWindow = win32con.SW_HIDE
                            creation_flags = win32process.CREATE_NEW_CONSOLE | win32process.CREATE_UNICODE_ENVIRONMENT
                            user_profile_dir = win32profile.GetUserProfileDirectory(token)

                            hProcess, hThread, dwPid, dwTid = win32process.CreateProcessAsUser(
                                token, self.python_exe, self.ootb_command,
                                None, None, False, creation_flags, env, user_profile_dir, startup
                            )
                            log_info(f"CreateProcessAsUser call succeeded for user '{user}' (PID: {dwPid}). Checking existence...")
                            win32api.CloseHandle(hProcess)
                            win32api.CloseHandle(hThread)

                            time.sleep(1)
                            if psutil.pid_exists(dwPid):
                                log_info(f"Immediate start succeeded for user '{user}' (PID {dwPid}).")
                                immediate_start_status = "start_success"
                            else:
                                log_error(f"Immediate start failed for user '{user}': Process {dwPid} exited immediately.")
                                immediate_start_status = "start_failed_exited"
                                failed_users.add(user)

                        except Exception as proc_err:
                             log_error(f"Exception during immediate start for user '{user}': {proc_err}", exc_info=True)
                             immediate_start_status = "start_failed_exception"
                             failed_users.add(user)
                        finally:
                             if token:
                                  try: win32api.CloseHandle(token)
                                  except: pass
                    else: # User is active but already running
                        log_info(f"User '{user}' is active but OOTB is already running. Skipping immediate start.")
                        immediate_start_status = "start_skipped_already_running"
                else: # User is not active
                     log_info(f"User '{user}' is not active. Skipping immediate start (task created/updated).")
                     immediate_start_status = "start_skipped_inactive"
                
                # Record final results for this user
                start_results[user] = (task_created_status, immediate_start_status)


            # --- Consolidate status --- 
            total_processed = len(target_users_normalized)
            final_status = "partial_success" if failed_users else "success"
            if not start_results: final_status = "no_targets_processed"
            # If all processed users failed in some way (either task or start)
            if len(failed_users) == total_processed and total_processed > 0: final_status = "failed"
            # Special case: target was specific user who wasn't found active
            elif total_processed == 1 and target_user != "all_active" and target_user.lower() not in active_sessions: 
                user_key = target_user.lower()
                if user_key in start_results and start_results[user_key][0] == "task_success":
                    final_status = "success_task_only_user_inactive"
                else:
                    final_status = "failed_task_user_inactive"

            log_info(f"Finished starting OOTB. Overall Status: {final_status}. Results: {start_results}")
            # Return detailed results as a JSON string for easier parsing/logging server-side
            try: 
                details = json.dumps(start_results)
            except Exception: 
                details = str(start_results) # Fallback
            return f"{final_status}::{details}" 

        except Exception as e:
             log_error(f"Error during combined start OOTB process: {e}", exc_info=True)
             return "failed_exception"

# --- Main Execution Block ---
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        log_info("Starting service in debug mode...")
        print(f"Running Flask server via Waitress on {_LISTEN_HOST}:{_LISTEN_PORT} for debugging...")
        print("Service logic (command processing) will NOT run in this mode.")
        print("Use this primarily to test the '/command' endpoint receiving POSTs.")
        print("Press Ctrl+C to stop.")
        try:
             serve(flask_app, host=_LISTEN_HOST, port=_LISTEN_PORT, threads=1)
        except KeyboardInterrupt:
             print("\nDebug server stopped.")

    elif len(sys.argv) == 1:
        try:
            servicemanager.Initialize()
            servicemanager.PrepareToHostSingle(GuardService)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            import winerror
            if details.winerror == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                print(f"Error: Not started by SCM.")
                print(f"Use 'python {os.path.basename(__file__)} install|start|stop|remove|debug'")
            else:
                print(f"Error preparing service: {details}")
        except Exception as e:
             print(f"Unexpected error initializing service: {e}")
    else:
        win32serviceutil.HandleCommandLine(GuardService) 