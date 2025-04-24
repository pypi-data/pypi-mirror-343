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
# Move these inside the class later
# def get_python_executable(): ...
# def get_pip_executable(): ...

# Define loggers at module level for use before instance exists?
# Or handle carefully within instance methods.

# --- PowerShell Task Scheduler Helpers --- (These will become methods) ---

# _TASK_NAME_PREFIX = "OOTB_UserLogon_" # Move to class

# def run_powershell_command(command, log_output=True): ...
# def create_or_update_logon_task(username, task_command, python_executable): ...
# def remove_logon_task(username): ...

# --- End PowerShell Task Scheduler Helpers ---

TARGET_EXECUTABLE_NAME = "computer-use-ootb-internal.exe"

class GuardService(win32serviceutil.ServiceFramework):
    _svc_name_ = _SERVICE_NAME
    _svc_display_name_ = _SERVICE_DISPLAY_NAME
    _svc_description_ = _SERVICE_DESCRIPTION
    _task_name_prefix = "OOTB_UserLogon_" # Class attribute for task prefix

    # --- Instance Logging Methods ---
    def log_info(self, msg):
        thread_name = threading.current_thread().name
        full_msg = f"[{thread_name}] {msg}"
        logging.info(full_msg)
        try:
            if threading.current_thread().name in ["MainThread", "CommandProcessor"]:
                 servicemanager.LogInfoMsg(str(full_msg))
        except Exception as e:
            # Log only to file if event log fails
            logging.warning(f"(Instance) Could not write info to Windows Event Log: {e}")

    def log_error(self, msg, exc_info=False):
        thread_name = threading.current_thread().name
        full_msg = f"[{thread_name}] {msg}"
        logging.error(full_msg, exc_info=exc_info)
        try:
            if threading.current_thread().name in ["MainThread", "CommandProcessor"]:
                servicemanager.LogErrorMsg(str(full_msg))
        except Exception as e:
            logging.warning(f"(Instance) Could not write error to Windows Event Log: {e}")
    # --- End Instance Logging --- 

    # --- Instance Helper Methods (Moved from module level) ---
    def _find_target_executable(self):
        """Finds the target executable (e.g., computer-use-ootb-internal.exe) in the Scripts directory."""
        try:
            # sys.executable should be python.exe or pythonservice.exe in the env root/Scripts
            env_dir = os.path.dirname(sys.executable)
            # If sys.executable is in Scripts, go up one level
            if os.path.basename(env_dir.lower()) == 'scripts':
                env_dir = os.path.dirname(env_dir)

            scripts_dir = os.path.join(env_dir, 'Scripts')
            target_exe_path = os.path.join(scripts_dir, TARGET_EXECUTABLE_NAME)

            self.log_info(f"_find_target_executable: Checking for executable at: {target_exe_path}")

            if os.path.exists(target_exe_path):
                self.log_info(f"_find_target_executable: Found executable: {target_exe_path}")
                # Quote if necessary for command line usage
                if " " in target_exe_path and not target_exe_path.startswith('"'):
                    return f'"{target_exe_path}"'
                return target_exe_path
            else:
                self.log_error(f"_find_target_executable: Target executable not found at {target_exe_path}")
                # Fallback: Check env root directly (less common for scripts)
                target_exe_path_root = os.path.join(env_dir, TARGET_EXECUTABLE_NAME)
                self.log_info(f"_find_target_executable: Checking fallback location: {target_exe_path_root}")
                if os.path.exists(target_exe_path_root):
                     self.log_info(f"_find_target_executable: Found executable at fallback location: {target_exe_path_root}")
                     if " " in target_exe_path_root and not target_exe_path_root.startswith('"'):
                         return f'"{target_exe_path_root}"'
                     return target_exe_path_root
                else:
                     self.log_error(f"_find_target_executable: Target executable also not found at {target_exe_path_root}")
                     return None

        except Exception as e:
            self.log_error(f"Error finding target executable: {e}")
            return None

    def __init__(self, args):
        global _service_instance
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_running = True
        self.server_thread = None
        self.command_queue = queue.Queue()
        self.command_processor_thread = None
        self.session = requests.Session()

        self.target_executable_path = self._find_target_executable()
        if not self.target_executable_path:
             # Log error and potentially stop service if critical executable is missing
             self.log_error(f"CRITICAL: Could not find {TARGET_EXECUTABLE_NAME}. Service cannot function.")
             # Consider stopping the service here if needed, or handle appropriately
        else:
             self.log_info(f"Using target executable: {self.target_executable_path}")

        _service_instance = self
        self.log_info(f"Service initialized. Target executable set to: {self.target_executable_path}")

    def SvcStop(self):
        self.log_info(f"Service stop requested.")
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.is_running = False
        # Signal the command processor thread to stop
        self.command_queue.put(None) # Sentinel value
        # Signal the main wait loop
        win32event.SetEvent(self.hWaitStop)
        # Stopping waitress gracefully from another thread is non-trivial.
        # We rely on the SCM timeout / process termination for now.
        self.log_info(f"{_SERVICE_NAME} SvcStop: Stop signaled. Server thread will be terminated by SCM.")


    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        try:
            self.log_info(f"{_SERVICE_NAME} starting.")
            # Start the command processor thread
            self.command_processor_thread = threading.Thread(
                target=self.process_commands, name="CommandProcessor", daemon=True)
            self.command_processor_thread.start()
            self.log_info("Command processor thread started.")

            # Start the Flask server (via Waitress) in a separate thread
            self.server_thread = threading.Thread(
                target=self.run_server, name="WebServerThread", daemon=True)
            self.server_thread.start()
            self.log_info(f"Web server thread started, listening on {_LISTEN_HOST}:{_LISTEN_PORT}.")

            self.log_info(f"{_SERVICE_NAME} running. Waiting for stop signal.")
            # Keep the main service thread alive waiting for stop signal
            win32event.WaitForSingleObject(self.hWaitStop, win32event.INFINITE)
            self.log_info(f"{_SERVICE_NAME} received stop signal in main thread.")

        except Exception as e:
            self.log_error(f"Fatal error in SvcDoRun: {e}", exc_info=True)
            self.SvcStop() # Signal stop if possible
        finally:
            self.log_info(f"{_SERVICE_NAME} SvcDoRun finished.")


    def run_server(self):
        """Runs the Flask app using Waitress."""
        self.log_info(f"Waitress server starting on {_LISTEN_HOST}:{_LISTEN_PORT}")
        try:
            serve(flask_app, host=_LISTEN_HOST, port=_LISTEN_PORT, threads=4)
            self.log_info("Waitress server has stopped.") # Should only happen on shutdown
        except Exception as e:
            self.log_error(f"Web server thread encountered an error: {e}", exc_info=True)
            # Consider signaling the main thread to stop if the web server fails critically
            # For now, just log the error.


    def process_commands(self):
        """Worker thread to process commands from the queue."""
        self.log_info("Command processor thread starting.")
        while self.is_running:
            try:
                item = self.command_queue.get(block=True, timeout=1) # Add timeout to check is_running periodically
                if item is None:
                    self.log_info("Command processor received stop signal.")
                    break # Exit loop

                command_id, command = item
                action = command.get("action")
                target = command.get("target_user", "all_active")
                status = "failed_unknown" # Default

                self.log_info(f"Dequeued Command ID {command_id}: action='{action}', target='{target}'")

                try:
                    if action == "update":
                        status = self.handle_update()
                    elif action == "stop_ootb":
                        status = self.handle_stop(target)
                    elif action == "start_ootb":
                        status = self.handle_start(target)
                    else:
                        self.log_error(f"Unknown action in queue: {action}")
                        status = "failed_unknown_action"
                except Exception as handler_ex:
                    self.log_error(f"Exception processing Command ID {command_id} ({action}): {handler_ex}", exc_info=True)
                    status = "failed_exception"
                finally:
                    self.report_command_status(command_id, status)
                    self.command_queue.task_done()

            except queue.Empty:
                # Timeout occurred, just loop again and check self.is_running
                continue
            except Exception as e:
                 self.log_error(f"Error in command processing loop: {e}", exc_info=True)
                 if self.is_running:
                     time.sleep(5)

        self.log_info("Command processor thread finished.")


    def report_command_status(self, command_id, status, details=""):
        """Sends command status back to the server."""
        if not _SERVER_STATUS_REPORT_URL:
            self.log_error("No server status report URL configured. Skipping report.")
            return

        payload = {
            "command_id": command_id,
            "status": status,
            "details": details,
            "machine_id": os.getenv('COMPUTERNAME', 'unknown_guard')
        }
        self.log_info(f"Reporting status for command {command_id}: {status}")
        try:
            response = self.session.post(_SERVER_STATUS_REPORT_URL, json=payload, timeout=15)
            response.raise_for_status()
            self.log_info(f"Status report for command {command_id} accepted by server.")
        except requests.exceptions.RequestException as e:
            self.log_error(f"Failed to report status for command {command_id}: {e}")
        except Exception as e:
             self.log_error(f"Unexpected error reporting status for command {command_id}: {e}", exc_info=True)

    # --- Command Handlers --- Now call self. for helpers

    def handle_update(self):
        self.log_info("Executing OOTB update...")
        if not self.target_executable_path:
            self.log_error("Cannot update: Target executable not found.")
            return "failed_executable_not_found"

        update_command = f"{self.target_executable_path} update"
        self.log_info(f"Running update command: {update_command}")
        try:
            result = subprocess.run(update_command, shell=True, capture_output=True, text=True, check=True, timeout=300, encoding='utf-8')
            self.log_info(f"Update successful: \nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
            return "success"
        except subprocess.CalledProcessError as e:
            self.log_error(f"Update failed (Exit Code {e.returncode}):\nSTDOUT:\n{e.stdout}\nSTDERR:\n{e.stderr}")
            return f"failed_exit_{e.returncode}"
        except subprocess.TimeoutExpired:
             self.log_error(f"Update command timed out.")
             return "failed_timeout"
        except Exception as e:
            self.log_error(f"Unexpected error during update: {e}", exc_info=True)
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
            self.log_info(f"Searching for OOTB processes for users: {target_users}")
            
            # Use the potentially corrected python.exe path for matching
            python_exe_path_for_check = self.target_executable_path.strip('"') 
            self.log_info(f"_get_ootb_processes: Checking against python path: {python_exe_path_for_check}")

            for proc in psutil.process_iter(['pid', 'name', 'username', 'cmdline', 'exe']):
                try:
                    pinfo = proc.info
                    proc_username = pinfo['username']
                    if proc_username:
                        proc_username = proc_username.split('\\')[-1].lower()

                    if proc_username in target_users:
                        cmdline = ' '.join(pinfo['cmdline']) if pinfo['cmdline'] else ''
                        # Check if the process executable matches our corrected python path AND module is in cmdline
                        if pinfo['exe'] and pinfo['exe'] == python_exe_path_for_check and _OOTB_MODULE in cmdline:
                            self.log_info(f"Found matching OOTB process: PID={pinfo['pid']}, User={pinfo['username']}, Cmd={cmdline}")
                            ootb_procs.append(proc)
                            target_pid_list.append(pinfo['pid'])
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            self.log_info(f"Found {len(ootb_procs)} OOTB process(es) matching criteria: {target_pid_list}")
        except Exception as e:
             self.log_error(f"Error enumerating processes: {e}", exc_info=True)
        return ootb_procs

    def handle_stop(self, target_user="all_active"):
        self.log_info(f"Executing stop OOTB for target '{target_user}'...")
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
                             self.log_error(f"Could not query session {session['SessionId']} during stop: {query_err}")
            except Exception as user_enum_err:
                  self.log_error(f"Error enumerating users/sessions during stop: {user_enum_err}", exc_info=True)
                  return "failed_user_enumeration"

            self.log_info(f"Stop target: '{target_user}'. Active sessions: {active_sessions}")

            target_users_normalized = set()
            if target_user == "all_active":
                  # Target only currently active users for stop all
                  target_users_normalized = set(active_sessions.keys())
                  self.log_info(f"Stop targeting all active users: {target_users_normalized}")
            else:
                  # Target the specific user, regardless of active status (for task removal)
                  normalized_target = target_user.lower()
                  target_users_normalized.add(normalized_target)
                  self.log_info(f"Stop targeting specific user: {normalized_target}")

            if not target_users_normalized:
                  self.log_info("No target users identified for stop.")
                  return "failed_no_target_users" # Or success if none were targeted?

            # --- Process each target user ---
            for user in target_users_normalized:
                 task_removed_status = "task_unknown"
                 immediate_stop_status = "stop_not_attempted"
                 stopped_count = 0

                 self.log_info(f"Processing stop for user '{user}'...")

                 # 1. Always try to remove the scheduled task
                 try:
                     # remove_logon_task always returns True for now, just logs attempt
                     self.remove_logon_task(user)
                     task_removed_status = "task_removed_attempted"
                 except Exception as task_err:
                      self.log_error(f"Exception removing scheduled task for {user}: {task_err}", exc_info=True)
                      task_removed_status = "task_exception"
                      failed_users.add(user)
                      # Continue to try and stop process if active

                 # 2. If user is active, try to terminate process
                 is_active = user in active_sessions

                 if is_active:
                     immediate_stop_status = "stop_attempted"
                     self.log_info(f"User '{user}' is active. Attempting to terminate OOTB process(es)...")
                     # Pass the specific username to _get_ootb_processes
                     procs_to_stop = self._get_ootb_processes(user)

                     if not procs_to_stop:
                         self.log_info(f"No running OOTB processes found for active user '{user}'.")
                         immediate_stop_status = "stop_skipped_not_running"
                     else:
                         self.log_info(f"Found {len(procs_to_stop)} process(es) for user '{user}' to stop.")
                         for proc in procs_to_stop:
                             try:
                                 pid = proc.pid # Get pid before potential termination
                                 username = proc.info.get('username', 'unknown_user')
                                 self.log_info(f"Terminating process PID={pid}, User={username}")
                                 proc.terminate()
                                 try:
                                     proc.wait(timeout=3)
                                     self.log_info(f"Process PID={pid} terminated successfully.")
                                     stopped_count += 1
                                 except psutil.TimeoutExpired:
                                     self.log_error(f"Process PID={pid} did not terminate gracefully, killing.")
                                     proc.kill()
                                     stopped_count += 1
                             except psutil.NoSuchProcess:
                                  self.log_info(f"Process PID={pid} already terminated.")
                                  # Don't increment stopped_count here as we didn't stop it now
                             except psutil.AccessDenied:
                                 self.log_error(f"Access denied trying to terminate process PID={pid}.")
                                 failed_users.add(user) # Mark user as failed if stop fails
                             except Exception as e:
                                 self.log_error(f"Error stopping process PID={pid}: {e}", exc_info=True)
                                 failed_users.add(user) # Mark user as failed

                         # Determine status based on how many were found vs stopped
                         if user in failed_users:
                              immediate_stop_status = f"stop_errors_terminated_{stopped_count}_of_{len(procs_to_stop)}"
                         elif stopped_count == len(procs_to_stop):
                              immediate_stop_status = f"stop_success_terminated_{stopped_count}"
                         else: # Should ideally not happen if NoSuchProcess doesn't count
                              immediate_stop_status = f"stop_partial_terminated_{stopped_count}_of_{len(procs_to_stop)}"

                 else: # User not active
                     self.log_info(f"User '{user}' is not active. Skipping immediate process stop (task removal attempted).")
                     immediate_stop_status = "stop_skipped_inactive"

                 # Record final results for this user
                 stop_results[user] = (task_removed_status, immediate_stop_status)


            # --- Consolidate status ---
            total_processed = len(target_users_normalized)
            final_status = "partial_success" if failed_users else "success"
            if not stop_results: final_status = "no_targets_processed"
            if len(failed_users) == total_processed and total_processed > 0 : final_status = "failed"

            self.log_info(f"Finished stopping OOTB. Overall Status: {final_status}. Results: {stop_results}")
            try:
                details = json.dumps(stop_results)
            except Exception:
                details = str(stop_results) # Fallback
            return f"{final_status}::{details}" # Use :: as separator

        except Exception as e:
             self.log_error(f"Error during combined stop OOTB process: {e}", exc_info=True)
             return "failed_exception"


    def handle_start(self, target_user="all_active"):
        self.log_info(f"Executing start OOTB for target '{target_user}'...")
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
                            self.log_error(f"Could not query session {session['SessionId']}: {query_err}")
            except Exception as user_enum_err:
                 self.log_error(f"Error enumerating users/sessions: {user_enum_err}", exc_info=True)
                 return "failed_user_enumeration"

            self.log_info(f"Found active user sessions: {active_sessions}")

            target_users_normalized = set()
            if target_user == "all_active":
                 # If targeting all_active, only target those CURRENTLY active
                 target_users_normalized = set(active_sessions.keys())
                 self.log_info(f"Targeting all active users: {target_users_normalized}")
            else:
                 normalized_target = target_user.lower()
                 # Check if the target user actually exists on the system, even if inactive
                 # This check might be complex/unreliable. Rely on task scheduler potentially failing?
                 # Let's assume admin provides a valid username for specific targeting.
                 # if normalized_target in all_system_users: # Removing this check, assume valid user input
                 target_users_normalized.add(normalized_target)
                 self.log_info(f"Targeting specific user: {normalized_target}")
                 # else:
                 #     log_error(f"Target user '{target_user}' does not appear to exist on this system based on psutil.")
                 #     return "failed_user_does_not_exist"

            if not target_users_normalized:
                 self.log_info("No target users identified (or none active for 'all_active').")
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
                 self.log_error(f"Error checking existing processes: {e}")
            self.log_info(f"Users currently running OOTB: {running_procs_by_user}")

            # --- Process each target user ---
            for user in target_users_normalized:
                task_created_status = "task_unknown"
                immediate_start_status = "start_not_attempted"
                token = None # Ensure token is reset/defined

                self.log_info(f"Processing start for user '{user}'...")

                # 1. Always try to create/update the scheduled task
                try:
                    task_created = self.create_or_update_logon_task(user)
                    task_created_status = "task_success" if task_created else "task_failed"
                except Exception as task_err:
                     self.log_error(f"Exception creating/updating scheduled task for {user}: {task_err}", exc_info=True)
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
                        self.log_info(f"User '{user}' is active and not running OOTB. Attempting immediate start...")
                        try:
                            session_id = active_sessions[user]
                            token = win32ts.WTSQueryUserToken(session_id)
                            # env = win32profile.CreateEnvironmentBlock(token, False) # <-- Temporarily disable creating env block
                            env = None # Use default environment provided by CreateProcessAsUser
                            startup = win32process.STARTUPINFO()
                            creation_flags = 0x00000010 # CREATE_NEW_CONSOLE

                            # --- Launch via cmd /K ---
                            lpApplicationName = None
                            lpCommandLine = f'cmd.exe /K "{self.target_executable_path}"' 
                            cwd = os.path.dirname(self.target_executable_path.strip('"')) if os.path.dirname(self.target_executable_path.strip('"')) != '' else None
                            # --- End Launch via cmd /K ---

                            self.log_info(f"Calling CreateProcessAsUser to launch via cmd /K (Default Environment Test):") # Added note to log
                            self.log_info(f"  lpApplicationName: {lpApplicationName}")
                            self.log_info(f"  lpCommandLine: {lpCommandLine}")
                            self.log_info(f"  lpCurrentDirectory: {cwd if cwd else 'Default'}")
                            self.log_info(f"  dwCreationFlags: {creation_flags} (CREATE_NEW_CONSOLE)")

                            # CreateProcessAsUser call with env = None
                            hProcess, hThread, dwPid, dwTid = win32process.CreateProcessAsUser(
                                token,              # User token
                                lpApplicationName,  # Application name (None)
                                lpCommandLine,      # Command line (cmd.exe /K "...")
                                None,               # Process attributes
                                None,               # Thread attributes
                                False,              # Inherit handles
                                creation_flags,     # Creation flags (CREATE_NEW_CONSOLE)
                                env,                # Environment block (Now None)
                                cwd,                # Current directory for cmd.exe
                                startup             # Startup info
                            )

                            self.log_info(f"CreateProcessAsUser call succeeded for user '{user}' (PID: {dwPid}). Checking existence...")
                            win32api.CloseHandle(hProcess)
                            win32api.CloseHandle(hThread)

                            time.sleep(1)
                            if psutil.pid_exists(dwPid):
                                self.log_info(f"Immediate start succeeded for user '{user}' (PID {dwPid}).")
                                immediate_start_status = "start_success"
                            else:
                                self.log_error(f"Immediate start failed for user '{user}': Process {dwPid} exited immediately.")
                                immediate_start_status = "start_failed_exited"
                                failed_users.add(user)

                        except Exception as proc_err:
                             self.log_error(f"Exception during immediate start for user '{user}': {proc_err}", exc_info=True)
                             immediate_start_status = "start_failed_exception"
                             failed_users.add(user)
                        finally:
                             if token:
                                  try: win32api.CloseHandle(token)
                                  except: pass
                    else: # User is active but already running
                        self.log_info(f"User '{user}' is active but OOTB is already running. Skipping immediate start.")
                        immediate_start_status = "start_skipped_already_running"
                else: # User is not active
                     self.log_info(f"User '{user}' is not active. Skipping immediate start (task created/updated).")
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

            self.log_info(f"Finished starting OOTB. Overall Status: {final_status}. Results: {start_results}")
            # Return detailed results as a JSON string for easier parsing/logging server-side
            try: 
                details = json.dumps(start_results)
            except Exception: 
                details = str(start_results) # Fallback
            return f"{final_status}::{details}" 

        except Exception as e:
             self.log_error(f"Error during combined start OOTB process: {e}", exc_info=True)
             return "failed_exception"

    def create_or_update_logon_task(self, username):
        """Creates/updates task to run OOTB app via cmd /K on session connect (RDP/Console)."""
        if not self.target_executable_path:
            self.log_error(f"Cannot create task for {username}: Target executable path is not set.")
            return False

        task_name = f"OOTB_UserConnect_{username}" # Renamed task slightly
        action_executable = "cmd.exe"
        action_arguments = f'/K "{self.target_executable_path}"'
        safe_action_executable = action_executable.replace("'", "''")
        safe_action_arguments = action_arguments.replace("'", "''")
        
        # Explicitly set the working directory to the executable's location
        try:
            executable_dir = os.path.dirname(self.target_executable_path.strip('"'))
            if not executable_dir: # Handle case where path might be just the exe name
                 executable_dir = "." # Use current directory as fallback?
                 self.log_warning(f"Could not determine directory for {self.target_executable_path}, task WorkingDirectory might be incorrect.")
            safe_working_directory = executable_dir.replace("'", "''")
            working_directory_setting = f"$action.WorkingDirectory = '{safe_working_directory}'"
        except Exception as e:
             self.log_error(f"Error determining working directory for task: {e}. WorkingDirectory will not be set.")
             working_directory_setting = "# Could not set WorkingDirectory" # Comment out in PS script

        # PowerShell command construction
        ps_command = f"""
        $taskName = "{task_name}"
        $principal = New-ScheduledTaskPrincipal -UserId "{username}" -LogonType Interactive
        
        # Action: Run cmd.exe with /K, setting the working directory
        $action = New-ScheduledTaskAction -Execute '{safe_action_executable}' -Argument '{safe_action_arguments}'
        {working_directory_setting}

        # Trigger: On session connect/reconnect events for Terminal Services
        $logName = 'Microsoft-Windows-TerminalServices-LocalSessionManager/Operational'
        $source = 'Microsoft-Windows-TerminalServices-LocalSessionManager'
        $eventIDs = @(21, 25) # 21=SessionLogon, 25=SessionReconnect
        # The Principal -UserId should ensure this only runs for the target user when they connect
        $trigger = New-ScheduledTaskTrigger -AtLogOn # Keep AtLogOn as a fallback?
        # --- Let's stick to ONE trigger type first. Replacing AtLogOn with Event --- 
        # $trigger = New-ScheduledTaskTrigger -AtLogOn -User "{username}" 
        $trigger = New-ScheduledTaskTrigger -Event -LogName $logName -Source $source -EventId $eventIDs[0] # Primary trigger
        # Register additional triggers if needed, or handle logic differently.
        # For simplicity, let's try one event trigger first (ID 21). If reconnect (25) is needed, we can add it.
        # Consider adding delay: -Delay 'PT15S' # Delay 15 seconds after event?
        
        $settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Days 9999) -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 1)
        $description = "Runs OOTB Application (via cmd) for user {username} upon session connect (Event Trigger)." # Updated description

        # Unregister existing task first (force) - Use the NEW task name
        Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

        # Register the new task
        Register-ScheduledTask -TaskName $taskName -Principal $principal -Action $action -Trigger $trigger -Settings $settings -Description $description -Force
        
        # Optional: Add second trigger for event ID 25 (Reconnect)
        # Requires creating a separate trigger object and adding it.
        # $trigger2 = New-ScheduledTaskTrigger -Event -LogName $logName -Source $source -EventId $eventIDs[1]
        # Set-ScheduledTask -TaskName $taskName -Trigger $trigger, $trigger2 # This replaces existing triggers
        # Append trigger is more complex via PowerShell cmdlets, often easier via XML or COM

        """
        self.log_info(f"Attempting to create/update task '{task_name}' for user '{username}' to run '{action_executable} {action_arguments}' on session connect.")
        try:
            # Need to actually run the powershell command here!
            success = self.run_powershell_command(ps_command)
            if success:
                 self.log_info(f"Successfully ran PowerShell command to create/update task '{task_name}'.")
                 return True
            else:
                 self.log_error(f"PowerShell command failed to create/update task '{task_name}'. See previous logs.")
                 return False
        except Exception as e:
            self.log_error(f"Failed to create/update scheduled task '{task_name}' for user '{username}': {e}", exc_info=True)
            return False

    def run_powershell_command(self, command, log_output=True):
        """Executes a PowerShell command and handles output/errors. Returns True on success."""
        self.log_info(f"Executing PowerShell: {command}")
        try:
            result = subprocess.run(
                ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
                capture_output=True, text=True, check=True, encoding='utf-8', errors='ignore'
            )
            if log_output and result.stdout:
                self.log_info(f"PowerShell STDOUT:\n{result.stdout.strip()}")
            if log_output and result.stderr:
                # Log stderr as info, as some commands write status here (like unregister task not found)
                self.log_info(f"PowerShell STDERR:\n{result.stderr.strip()}") 
            return True
        except FileNotFoundError:
            self.log_error("'powershell.exe' not found. Cannot manage scheduled tasks.")
            return False
        except subprocess.CalledProcessError as e:
            # Log error but still return False, handled by caller
            self.log_error(f"PowerShell command failed (Exit Code {e.returncode}):")
            self.log_error(f"  Command: {e.cmd}")
            if e.stdout: self.log_error(f"  STDOUT: {e.stdout.strip()}")
            if e.stderr: self.log_error(f"  STDERR: {e.stderr.strip()}")
            return False
        except Exception as e:
            self.log_error(f"Unexpected error running PowerShell: {e}", exc_info=True)
            return False

    def remove_logon_task(self, username):
        """Removes the logon scheduled task for a user."""
        task_name = f"{self._task_name_prefix}{username}"
        safe_task_name = task_name.replace("'", "''")
        command = f"Unregister-ScheduledTask -TaskName '{safe_task_name}' -Confirm:$false -ErrorAction SilentlyContinue"
        self.run_powershell_command(command, log_output=False)
        self.log_info(f"Attempted removal of scheduled task '{task_name}' for user '{username}'.")
        return True

# --- Main Execution Block ---
if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        self.log_info("Starting service in debug mode...")
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