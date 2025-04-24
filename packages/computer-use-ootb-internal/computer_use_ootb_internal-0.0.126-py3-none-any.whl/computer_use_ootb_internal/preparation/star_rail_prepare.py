# src/computer_use_ootb_internal/preparation/star_rail_prepare.py
import time
import platform
import subprocess # Added for taskkill
import webbrowser
import logging # Use logging instead of print for better practice

# Set up logging for this module if needed, or rely on root logger
log = logging.getLogger(__name__)

def run_preparation(state):
    """
    Performs environment preparation specific to Star Rail on Windows.
    Closes existing Edge browsers and opens the specified URL in a new Edge instance.
    """
    if platform.system() != "Windows":
        log.info("Star Rail preparation skipped: Not running on Windows.")
        return

    log.info("Star Rail preparation: Starting environment setup on Windows...")
    url = "https://sr.mihoyo.com/cloud/#/" # Consider making this configurable later
    browser_opened = False
    try:
        # Attempt to close existing Microsoft Edge processes
        log.info("Attempting to close existing Microsoft Edge processes...")
        try:
            # /F forces termination, /IM specifies image name
            result = subprocess.run(['taskkill', '/F', '/IM', 'msedge.exe'], 
                                    capture_output=True, text=True, check=False)
            if result.returncode == 0:
                log.info("Successfully sent termination signal to msedge.exe processes.")
            elif "not found" in result.stderr.lower() or "not found" in result.stdout.lower():
                 log.info("No running msedge.exe processes found to close.")
            else:
                 log.warning(f"taskkill command finished with return code {result.returncode}. Output: {result.stdout} Stderr: {result.stderr}")
            time.sleep(2) # Give processes time to close
        except FileNotFoundError:
            log.error("Error: 'taskkill' command not found. Make sure it's in the system PATH.")
        except Exception as e:
            log.error(f"Error occurred while trying to close Edge: {e}", exc_info=True)


        # Use only webbrowser.open
        log.info(f"Attempting to open {url} using webbrowser.open()...")
        if webbrowser.open(url):
            log.info(f"Successfully requested browser to open {url} via webbrowser.open().")
            browser_opened = True
            time.sleep(5) # Wait time for the browser to potentially load the page
        else:
            log.warning("webbrowser.open() returned False, indicating potential failure.")
            # No need to error out completely if browser *request* failed, 
            # but it's unlikely the rest of the process would work.

        if not browser_opened:
             log.error("Failed to confirm browser opening via webbrowser.open().")

        # Removed pyautogui click logic

        log.info("Star Rail preparation completed (browser opened).")

    except Exception as e:
        log.error(f"Error during Star Rail preparation: {e}", exc_info=True)
    # No finally block needed anymore as pyautogui failsafe is removed 