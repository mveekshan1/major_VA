import subprocess
import re
import pygetwindow as gw

def open_application(app_name):
    """
    Opens the specified application.
    It tries to find the application by its name and then launches it.
    """
    if not app_name:
        return "Please specify an application to open."
    try:
        # The 'start' command can launch applications by their name or path.
        # It's a built-in command in the Windows shell.
        subprocess.run(["start", "", app_name], shell=True, check=True)
        return f"Successfully started {app_name}."
    except subprocess.CalledProcessError:
        return f"Could not find or open the application named '{app_name}'. Please check the name or provide a full path."
    except Exception as e:
        return f"An unexpected error occurred while trying to open {app_name}: {e}"

def close_application(app_name):
    """
    Closes the specified application using taskkill.
    """
    if not app_name:
        return "Please specify an application to close."
    
    # Adding '.exe' if not present can help, but be careful not to mis-target.
    if not app_name.endswith('.exe'):
        app_name += '.exe'
        
    try:
        # Use /F to force-kill the process. Use /IM to specify the image name.
        # Use /T to terminate any child processes.
        result = subprocess.run(
            ["taskkill", "/F", "/IM", app_name, "/T"],
            capture_output=True, text=True, check=True
        )
        if "SUCCESS" in result.stdout:
            return f"{app_name} has been closed."
        else:
            # This part might not be reached if check=True is used, as non-zero exits will raise CalledProcessError
            return f"Failed to close {app_name}. It might not be running or you may not have permission."
    except subprocess.CalledProcessError as e:
        if "not found" in e.stderr:
            return f"The application '{app_name}' is not currently running."
        return f"Error closing {app_name}: {e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def list_installed_applications():
    """
    Lists installed applications on Windows using WMIC.
    """
    try:
        # WMIC is a command-line interface for Windows Management Instrumentation.
        # It can be used to query system information.
        cmd = "wmic product get name"
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, shell=True)
        
        # The output from wmic can be messy, with extra whitespace.
        apps = [line.strip() for line in result.stdout.splitlines() if line.strip() and line.strip().lower() != "name"]
        
        if not apps:
            return "Could not retrieve a list of installed applications."
        
        return "Here are the installed applications:\n" + "\n".join(sorted(apps))
    except subprocess.CalledProcessError:
        return "Failed to execute WMIC. This feature may require administrative privileges."
    except FileNotFoundError:
        return "WMIC is not available on this system."
    except Exception as e:
        return f"An error occurred while listing installed applications: {e}"


def list_running_applications():
    """
    Lists running applications (processes) using tasklist.
    """
    try:
        # tasklist is a command-line tool that provides a list of currently running processes.
        cmd = 'tasklist /v /fo csv | findstr /i "apps"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        
        # The output of tasklist can be parsed as CSV. We are interested in the window title, 
        # which is more user-friendly than the process name.
        running_apps = []
        for line in result.stdout.strip().split('\n'):
            parts = line.strip().split('","')
            if len(parts) > 8:
                window_title = parts[8].strip('"')
                if window_title != "N/A":
                    running_apps.add(window_title)
        
        if not running_apps:
            return "No running applications with windows were found."
            
        return "Currently running applications with active windows:\n" + "\n".join(sorted(list(running_apps)))
    except subprocess.CalledProcessError:
        # If the findstr command returns no matches, it exits with an error, so we handle that.
        return "No running applications with active windows were found."
    except Exception as e:
        return f"An error occurred while listing running applications: {e}"

def switch_application(app_name):
    """
    Switches focus to a running application window that matches the given name.
    """
    if not app_name:
        return "Please specify an application to switch to."
        
    try:
        # pygetwindow allows for controlling application windows.
        # We get all windows and try to find one that contains the app_name in its title.
        windows = gw.getWindowsWithTitle(app_name)
        
        if windows:
            # Activate the first window found.
            target_window = windows[0]
            if not target_window.isActive:
                target_window.activate()
            # Some applications need a moment to come to the foreground
            target_window.maximize()
            return f"Switched to {app_name}."
        else:
            # If no exact match, try a partial match (case-insensitive)
            all_titles = gw.getAllTitles()
            for title in all_titles:
                if app_name.lower() in title.lower():
                    window_to_activate = gw.getWindowsWithTitle(title)[0]
                    if not window_to_activate.isActive:
                        window_to_activate.activate()
                    window_to_activate.maximize()
                    return f"Switched to {title}."
            return f"No running application found with the name '{app_name}'."
            
    except Exception as e:
        return f"An error occurred while switching applications: {e}"
