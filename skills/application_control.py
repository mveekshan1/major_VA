import os
import subprocess
import pygetwindow as gw
import re

# Pre-compiled regex for better performance
app_name_pattern = re.compile(
    r'\b(open|close|run|launch|start|terminate|kill|exit|switch to|focus on|move to|activate|bring)\s+(.+)',
    re.IGNORECASE
)

def extract_app_name(command: str) -> str | None:
    """Extracts the application name from a command string using regex."""
    match = app_name_pattern.search(command)
    if match:
        # Return the second group, which is the app name
        app_name = match.group(2).strip()
        # Basic standardization
        return app_name.replace("the ", "").replace("application", "").replace("app", "").strip()
    return None

def open_app(command: str) -> str:
    """Opens an application based on the command."""
    app_name = extract_app_name(command)
    if not app_name:
        return "Could not determine which application to open. Please be more specific."
    try:
        # Use os.startfile for a non-blocking call on Windows
        os.startfile(f"C:\\Windows\\System32\\{app_name}.exe")
        return f"Opening {app_name}."
    except FileNotFoundError:
        try:
            # Fallback for apps not in System32
            subprocess.Popen([app_name])
            return f"Opening {app_name}."
        except (FileNotFoundError, OSError):
            return f"Sorry, I couldn't find or open the application named '{app_name}'."
    except Exception as e:
        return f"An unexpected error occurred while trying to open {app_name}: {e}"

def close_app(command: str) -> str:
    """Closes a running application."""
    app_name = extract_app_name(command)
    if not app_name:
        return "Could not determine which application to close. Please be more specific."

    # Standardize to process name (e.g., "Google Chrome" -> "chrome.exe")
    if not app_name.endswith('.exe'):
        app_name += '.exe'

    try:
        # Forcefully terminate the process. /F for force, /IM for image name.
        result = subprocess.run(
            ['taskkill', '/F', '/IM', app_name],
            capture_output=True, text=True, check=True
        )
        if "SUCCESS" in result.stdout:
            return f"{app_name.replace('.exe', '')} has been closed."
        else:
            # This case might happen if taskkill reports success but with a different message
            return f"Attempted to close {app_name.replace('.exe', '')}."
    except subprocess.CalledProcessError as e:
        # CalledProcessError is raised for non-zero exit codes.
        # This typically means the process wasn't found.
        if "not found" in e.stderr:
            return f"Application '{app_name.replace('.exe', '')}' is not currently running."
        else:
            return f"Failed to close {app_name.replace('.exe', '')}. Reason: {e.stderr}"
    except Exception as e:
        return f"An error occurred while trying to close {app_name.replace('.exe', '')}: {e}"

def list_running_apps() -> str:
    """Lists all currently running applications visible to the user."""
    try:
        windows = gw.getAllTitles()
        running_apps = [win for win in windows if win]  # Filter out empty titles
        if not running_apps:
            return "No applications are currently running."
        return "Running applications:\n" + "\n".join(f"- {app}" for app in running_apps)
    except Exception as e:
        return f"An error occurred while listing running applications: {e}"

def list_installed_apps() -> str:
    """Lists installed applications using WMIC."""
    try:
        # WMIC is a powerful command-line tool for system administration.
        # 'product get name' retrieves the names of installed products.
        result = subprocess.run(
            ['wmic', 'product', 'get', 'name'],
            capture_output=True, text=True, check=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        output = result.stdout.strip()
        if not output or "Name" not in output:
            return "Could not retrieve the list of installed applications."

        # Clean up the raw output from WMIC
        apps = [line.strip() for line in output.split('\n') if line.strip() and line.strip() != "Name"]
        if not apps:
            return "No installed applications found."

        return "Installed applications:\n" + "\n".join(f"- {app}" for app in apps)
    except FileNotFoundError:
        return "WMIC command not found. This feature is only available on Windows Pro/Enterprise."
    except subprocess.CalledProcessError as e:
        return f"Failed to list installed applications. Error: {e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def switch_to_app(command: str) -> str:
    """Switches focus to a running application window."""
    app_name = extract_app_name(command)
    if not app_name:
        return "Could not determine which application to switch to. Please be more specific."

    try:
        # Get all windows that match the app_name (case-insensitive)
        windows = gw.getWindowsWithTitle(app_name)
        if not windows:
            # Try a partial match if no exact match is found
            all_windows = gw.getAllWindows()
            target_window = next((win for win in all_windows if app_name.lower() in win.title.lower()), None)
            if not target_window:
                return f"No application window with a title containing '{app_name}' is currently open."
            windows = [target_window]

        # Activate the first found window
        target_window = windows[0]
        if target_window.isMinimized:
            target_window.restore()
        target_window.activate()
        return f"Switched to {target_window.title}."
    except Exception as e:
        return f"An error occurred while switching applications: {e}"