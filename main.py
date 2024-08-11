# Handle issue with bottle.py in --noconsole flag with pyinstaller
try:
    import eel
except AttributeError:
    from io import StringIO
    import sys

    if sys.stdout is None:
        sys.stdout = StringIO()
    if sys.stderr is None:
        sys.stderr = StringIO()

import tkinter as tk
from tkinter import filedialog
import sys
from backend.logic import *
from utilities import get_screen_size
import signal
from config import *

eel.init('frontend', allowed_extensions=['.js', '.html'])


@eel.expose
def handle_exit(ar1, ar2):
    """
    Exits the program gracefully.

    :param ar1:
    :param ar2:
    """
    try:
        os.kill(get_epost_downloader_pid(), signal.SIGTERM)
    except:
        pass
    sys.exit(0)


@eel.expose
def handle_app_info() -> dict:
    """
    Retrieves and returns information about the application.

    :return: A dictionary containing information about the application, including name, version, and build date.
    """

    return {
        "name": app_name,
        "version": app_version,
        "build": f"Built on {app_build_date}"
    }


@eel.expose
def handle_open_filedialog() -> str:
    """
    Opens a dialog box to select a file and returns the path of the selected file.

    :return: The path of the selected file if a file is chosen, otherwise an empty string.
    """
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.iconify()
    file_path = filedialog.askopenfilename(initialdir="/",
                                           title="Select File",
                                           filetypes=[])
    root.destroy()
    if file_path:
        return file_path

    return ""


@eel.expose
def handle_open_directory() -> str:
    """
    Opens a dialog box to select a directory and returns the selected directory path.

    :return: The path of the selected directory if a directory is chosen, otherwise an empty string.
    """
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.iconify()
    directory = filedialog.askdirectory()
    root.destroy()
    if directory:
        return directory
    return ""


eel.start("templates/main.html", port=0, close_callback=handle_exit, jinja_templates="templates",
          size=get_screen_size())
