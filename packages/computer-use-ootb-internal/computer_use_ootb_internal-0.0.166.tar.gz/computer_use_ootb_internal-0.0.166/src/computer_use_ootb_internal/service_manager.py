# src/computer_use_ootb_internal/service_manager.py
import sys
import os
import inspect
import subprocess
import ctypes
import platform
import time
import json
import shutil

# Constants need to match guard_service.py
_SERVICE_NAME = "OOTBGuardService"
_SERVICE_DISPLAY_NAME = "OOTB Guard Service"
_TASK_NAME_PREFIX = "OOTB_UserLogon_" # Must match guard_service.py
_SHORTCUT_NAME = "OOTB AutoStart Signal.lnk" # Name for the startup shortcut

def is_admin():
    """Check if the script is running with administrative privileges."""
    if platform.system() != "Windows":
        return False # Only applicable on Windows
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_service_module_path():
    """Gets the absolute path to the guard_service.py module."""
    # Find the path relative to this script's location
    # This assumes service_manager.py and guard_service.py are in the same installed package directory
    try:
        current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        service_module = os.path.join(current_dir, "guard_service.py")
        if not os.path.exists(service_module):
            raise FileNotFoundError(f"guard_service.py not found adjacent to service_manager.py in {current_dir}")
        return service_module
    except Exception as e:
         # Fallback if inspect fails (e.g., in some frozen environments)
         # Try finding it relative to the script itself? Unreliable.
         # Let's try sys.prefix - might work in standard venv/conda installs
         try:
             # sys.prefix points to the environment root (e.g., C:\path\to\env)
             # Package likely installed in Lib\site-packages\<package_name>
             # This depends heavily on installation layout
             package_name = __name__.split('.')[0] # Should be 'computer_use_ootb_internal'
             site_packages_path = os.path.join(sys.prefix, 'Lib', 'site-packages')
             module_dir = os.path.join(site_packages_path, package_name)
             service_module = os.path.join(module_dir, "guard_service.py")
             if os.path.exists(service_module):
                 print(f"Warning: Found service module via sys.prefix fallback: {service_module}")
                 return service_module
             else:
                 raise FileNotFoundError(f"guard_service.py not found via inspect or sys.prefix fallback (checked {module_dir})")
         except Exception as fallback_e:
             raise FileNotFoundError(f"Could not find guard_service.py using inspect ({e}) or sys.prefix ({fallback_e}). Check installation.")

def _run_command(cmd_list, check_errors=True, capture_output=False, verbose=True):
    """Helper to run an external command (like sc.exe)."""
    if verbose:
        # Safely join for printing, handle potential non-string elements just in case
        print(f"Executing command: {' '.join(map(str, cmd_list))}")
    try:
        result = subprocess.run(
            cmd_list,
            capture_output=capture_output,
            text=True,
            check=check_errors,
            encoding='utf-8',
            errors='ignore'
        )
        if capture_output and verbose:
             if result.stdout: print(f"  CMD STDOUT: {result.stdout.strip()}")
             if result.stderr: print(f"  CMD STDERR: {result.stderr.strip()}")
        return result if capture_output else (result.returncode == 0)
    except FileNotFoundError as e:
         print(f"Error: Command not found during execution: {cmd_list[0]}", file=sys.stderr)
         print(f" Details: {e}", file=sys.stderr)
         return None if capture_output else False
    except subprocess.CalledProcessError as e:
        # Don't print error if check_errors was False and it failed
        if check_errors and verbose:
            print(f"Error executing command {' '.join(map(str, cmd_list))} (Exit Code {e.returncode}).", file=sys.stderr)
            if e.stdout: print(f"Subprocess STDOUT:", file=sys.stderr); print(e.stdout, file=sys.stderr)
            if e.stderr: print(f"Subprocess STDERR:", file=sys.stderr); print(e.stderr, file=sys.stderr)
        return None if capture_output else False
    except Exception as e:
        if verbose:
            print(f"An unexpected error occurred running command: {e}", file=sys.stderr)
        return None if capture_output else False

def _get_startup_folder():
    """Gets the current user's Startup folder path."""
    try:
        # Use CSIDL value for Startup folder
        # Requires pywin32
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        # SHGetSpecialFolderPath requires integer CSIDL, Startup=7
        # Using shell.SpecialFolders is usually easier
        startup_path = shell.SpecialFolders("Startup")
        if startup_path and os.path.isdir(startup_path):
            print(f"Found Startup folder: {startup_path}")
            return startup_path
        else:
            print("Error: Could not resolve Startup folder path via WScript.Shell.", file=sys.stderr)
            return None
    except ImportError:
        print("Error: pywin32com is required to find Startup folder. Cannot manage startup shortcut.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error finding Startup folder: {e}", file=sys.stderr)
        return None

def _find_pythonw_executable():
    """Finds pythonw.exe in the same directory as sys.executable."""
    try:
        python_dir = os.path.dirname(sys.executable)
        pythonw_path = os.path.join(python_dir, "pythonw.exe")
        if os.path.exists(pythonw_path):
            return pythonw_path
        else:
            print(f"Warning: pythonw.exe not found next to sys.executable ({sys.executable}). Console window might flash on login.", file=sys.stderr)
            # Fallback to python.exe if pythonw not found
            return sys.executable
    except Exception as e:
        print(f"Error finding pythonw.exe: {e}. Using sys.executable as fallback.", file=sys.stderr)
        return sys.executable

def _create_startup_shortcut():
    """Creates a shortcut in the Startup folder to run signal_connection.py."""
    if not is_admin(): # Should already be checked, but double-check
        print("Admin privileges needed to potentially write shortcut.")
        return False

    startup_dir = _get_startup_folder()
    if not startup_dir:
        return False

    shortcut_path = os.path.join(startup_dir, _SHORTCUT_NAME)
    python_launcher = _find_pythonw_executable()
    signal_script = None
    try:
        # Find signal_connection.py relative to this script (service_manager.py)
        script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        signal_script = os.path.join(script_dir, "signal_connection.py")
        if not os.path.exists(signal_script):
             print(f"Error: signal_connection.py not found in {script_dir}", file=sys.stderr)
             return False
    except Exception as e:
        print(f"Error finding signal_connection.py: {e}", file=sys.stderr)
        return False

    # Target command for the shortcut
    target_cmd = f'"{python_launcher}"' # Quote launcher path
    # Quote script path
    target_cmd += f' "{signal_script}"'
    # Username argument - %USERNAME% will be expanded by shell when shortcut runs
    target_cmd += ' %USERNAME%'

    print(f"Creating Startup shortcut:")
    print(f"  Shortcut : {shortcut_path}")
    print(f"  Target   : {target_cmd}")

    # Use PowerShell to create the shortcut
    # Escape paths and arguments for the PowerShell command string
    ps_shortcut_path = shortcut_path.replace("'", "''")
    ps_target_cmd = target_cmd.replace("'", "''")
    ps_working_dir = os.path.dirname(signal_script).replace("'", "''") # Use script's dir as working dir
    ps_icon_location = python_launcher.replace("'", "''") # Use python icon

    ps_command = f"""
    $ws = New-Object -ComObject WScript.Shell
    $s = $ws.CreateShortcut('{ps_shortcut_path}')
    $s.TargetPath = '{ps_target_cmd.split()[0]}' # Executable part
    $s.Arguments = '{ps_target_cmd.split(' ', 1)[1] if ' ' in ps_target_cmd else ''}' # Arguments part
    $s.WorkingDirectory = '{ps_working_dir}'
    $s.IconLocation = '{ps_icon_location}'
    $s.WindowStyle = 7 # Minimized
    $s.Description = 'Triggers OOTB Guard Service connection check on login'
    $s.Save()
    Write-Host 'Shortcut created successfully.'
    """

    return _run_command([sys.executable, "-NoProfile", "-NonInteractive", "-Command", ps_command])

def _remove_startup_shortcut():
    """Removes the OOTB startup shortcut if it exists."""
    if not is_admin(): return False # Need admin to potentially delete
    startup_dir = _get_startup_folder()
    if not startup_dir:
        return False

    shortcut_path = os.path.join(startup_dir, _SHORTCUT_NAME)
    print(f"Attempting to remove Startup shortcut: {shortcut_path}")
    if os.path.exists(shortcut_path):
        try:
            os.remove(shortcut_path)
            print("Shortcut removed successfully.")
            return True
        except OSError as e:
            print(f"Error removing shortcut: {e}", file=sys.stderr)
            # Fallback attempt with PowerShell just in case of permission issues
            ps_shortcut_path = shortcut_path.replace("'", "''")
            ps_command = f"Remove-Item -Path '{ps_shortcut_path}' -Force -ErrorAction SilentlyContinue"
            return _run_command([sys.executable, "-NoProfile", "-NonInteractive", "-Command", ps_command], verbose=False)
        except Exception as e:
             print(f"Unexpected error removing shortcut: {e}", file=sys.stderr)
             return False
    else:
        print("Shortcut not found, no removal needed.")
        return True

def _cleanup_scheduled_tasks():
    """Removes all OOTB user logon scheduled tasks (legacy cleanup)."""
    print("Attempting legacy cleanup of OOTB user logon scheduled tasks...")
    # Use -like operator and wildcard
    # Need _TASK_NAME_PREFIX defined at module level
    command = f"""
    $tasks = Get-ScheduledTask | Where-Object {{ $_.TaskName -like '{_TASK_NAME_PREFIX}*' }}
    if ($tasks) {{
        Write-Host "Found $($tasks.Count) legacy OOTB logon tasks to remove."
        $tasks | Unregister-ScheduledTask -Confirm:$false -ErrorAction SilentlyContinue
        Write-Host "Legacy OOTB logon task removal attempted."
    }} else {{
        Write-Host "No legacy OOTB logon tasks found to remove."
    }}
    """
    # Use the generic _run_command helper, specifying powershell.exe
    _run_command(['powershell.exe', '-NoProfile', '-NonInteractive', '-Command', command], check_errors=False, verbose=False)

def install_and_start():
    """Installs and starts the Guard Service."""
    print(f"Attempting to install service: '{_SERVICE_NAME}' ('{_SERVICE_DISPLAY_NAME}')")
    # Step 1: Run the Python script to register the service class with SCM
    install_success = False
    try:
        python_exe = sys.executable
        service_script = get_service_module_path()
        # Quote paths
        python_exe_quoted = f'"{python_exe}"' if " " in python_exe else python_exe
        service_script_quoted = f'"{service_script}"' if " " in service_script else service_script
        # Use list for subprocess
        install_cmd = [sys.executable, service_script, '--startup', 'auto', 'install']
        print(f"Executing registration command: {' '.join(install_cmd)}")
        # We need to check output/return code carefully
        result = subprocess.run(install_cmd, capture_output=True, text=True, check=False, encoding='utf-8')
        if result.stdout: print(f"  Registration STDOUT: {result.stdout.strip()}")
        if result.stderr: print(f"  Registration STDERR: {result.stderr.strip()}")
        # Check common success/already-installed messages or just return code 0?
        # win32serviceutil often returns 0 even if service exists. Let's assume 0 is okay.
        if result.returncode == 0:
            print("Service registration command executed (might indicate success or already installed).")
            install_success = True
        else:
            print(f"Service registration command failed (Exit Code {result.returncode}).", file=sys.stderr)
            install_success = False

    except FileNotFoundError as e:
         print(f"Error finding Python or service script for registration: {e}", file=sys.stderr)
         install_success = False
    except Exception as e:
        print(f"Unexpected error during service registration: {e}", file=sys.stderr)
        install_success = False

    if install_success:
        print(f"\nRegistration command finished. Attempting to start service using 'sc start'...")
        time.sleep(2) # Give SCM time
        # Step 2: Use sc start
        start_cmd = ['sc', 'start', _SERVICE_NAME]
        start_success = _run_command(start_cmd, check_errors=False) # Don't fail script if start fails

        # Optional: Query status after attempting start
        time.sleep(3) # Wait a bit longer
        query_cmd = ['sc', 'query', _SERVICE_NAME]
        query_result = _run_command(query_cmd, capture_output=True, check_errors=False, verbose=False)
        service_running = False
        if query_result and query_result.stdout:
            if "RUNNING" in query_result.stdout:
                service_running = True
                print(f"Service '{_SERVICE_NAME}' confirmed running.")
            else:
                 print(f"Service '{_SERVICE_NAME}' status check returned:\n{query_result.stdout.strip()}")
        else:
            print("Warning: Could not query service status after start attempt.")

        if start_success and service_running:
            print(f"\nService '{_SERVICE_NAME}' installed/updated and started successfully.")
            # Step 3: Create startup shortcut only if service started
            print("Creating startup shortcut...")
            _create_startup_shortcut()
        elif start_success and not service_running:
            print(f"\nService '{_SERVICE_NAME}' installed/updated. 'sc start' command succeeded but service is not in RUNNING state.", file=sys.stderr)
            print(" Check logs or try starting manually.", file=sys.stderr)
        else: # start_success was False
             print(f"\nService '{_SERVICE_NAME}' installed/updated but 'sc start' command failed.", file=sys.stderr)
             print(f" Check output above, service logs ('C:\ProgramData\OOTBGuardService\guard_post_mode.log'), or Windows Event Viewer.", file=sys.stderr)
    else:
        # This path is taken if the initial registration command failed critically
        print(f"\nService '{_SERVICE_NAME}' registration failed critically. See errors above.", file=sys.stderr)

def stop_and_remove():
    """Stops and removes the Guard Service and associated resources."""
    print(f"Attempting to remove Startup shortcut...")
    _remove_startup_shortcut()

    print(f"\nAttempting to stop service using 'sc stop'...")
    # Run stop first, ignore errors (check_errors=False)
    # run_service_command(['stop'], check_errors=False)
    stop_cmd = ['sc', 'stop', _SERVICE_NAME]
    _run_command(stop_cmd, check_errors=False)
    time.sleep(3) # Give service time to stop

    # Optional: Check if stopped
    query_cmd = ['sc', 'query', _SERVICE_NAME]
    query_result = _run_command(query_cmd, capture_output=True, check_errors=False, verbose=False)
    service_exists = True # Assume it exists unless query fails specifically
    if query_result:
        if query_result.stderr and ("failed" in query_result.stderr.lower() or "does not exist" in query_result.stderr.lower()):
            service_exists = False
            print("Service does not appear to exist before removal attempt.")
        elif query_result.stdout and "STOPPED" in query_result.stdout:
            print("Service confirmed stopped.")
        elif query_result.stdout:
            print(f"Warning: Service state after stop attempt: {query_result.stdout.strip()}")
    else:
        print("Warning: Could not query service state after stop attempt.")

    print(f"\nAttempting to remove service using 'sc delete'...")
    # remove_success = run_service_command(['remove']) # Check if removal command itself failed
    delete_cmd = ['sc', 'delete', _SERVICE_NAME]
    delete_success = _run_command(delete_cmd, check_errors=False) # Ignore error if not found

    # Always attempt task cleanup, even if service removal had issues
    _cleanup_scheduled_tasks()

    if delete_success:
        # Check if it really doesn't exist now
        time.sleep(1)
        query_result_after = _run_command(query_cmd, capture_output=True, check_errors=False, verbose=False)
        if query_result_after and query_result_after.stderr and ("failed" in query_result_after.stderr.lower() or "does not exist" in query_result_after.stderr.lower()):
            print(f"\nService '{_SERVICE_NAME}' stopped (if running), removed successfully. Startup shortcut and logon tasks cleanup attempted.")
        else:
            print(f"\nService '{_SERVICE_NAME}' stop attempted. 'sc delete' command ran but service might still exist. Please check manually.", file=sys.stderr)
            print(f" Startup shortcut and logon tasks cleanup attempted.", file=sys.stderr)
    else:
        # This might happen if sc delete failed for permission reasons etc.
        print(f"\n'sc delete {_SERVICE_NAME}' command failed to execute properly.", file=sys.stderr)
        print(f" Startup shortcut and logon tasks cleanup attempted.", file=sys.stderr)
        print(f" Ensure the service was stopped first, or check permissions.", file=sys.stderr)

if __name__ == '__main__':
     # Allow calling functions directly for testing if needed
     print("This script provides service management commands.")
     print("Use 'ootb-install-service' or 'ootb-remove-service' as Administrator.") 