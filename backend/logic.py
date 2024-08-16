import subprocess
import eel
from vtp import VTP
from date_validation import *
from categorize_messages import CategorizeMessages
from vtp_log_parser import VTPLogParser
from enums import VTPReceiveLogFields, VTPTrackLogFields
from utilities import get_message_count_from_downloads_folder, check_path_for_files, generate_date_range
from web_scrape_messages import WebScrapeMessages
import os
import time
import threading
from config import vtp_path, logs_path, epost_connect_path
from constants import TRIAGE_FOLDER_PATH
import logging
import shutil

# Global to manage subprocess
epost_downloader_pid = None
# Global to manage thread
epost_downloader_thread_running = False
# Global to manage epost connect driver
epost_downloader_connect_driver = None
# Global to manage if the epost connect scrape failed
is_epost_downloader_connect_scrape_failed = False


def set_epost_downloader(pid):
    """
    Set the process ID of the epost downloader.

    :param pid: The process ID of the epost downloader.
    """
    global epost_downloader_pid
    epost_downloader_pid = pid


def get_epost_downloader_pid():
    """
    Get the process ID of the epost downloader.

    :return: The process ID of the epost downloader.
    """
    return epost_downloader_pid


def set_epost_downloader_thread_running(running: bool):
    """
    Set the status of the epost downloader thread.

    :param running: A boolean indicating whether the epost downloader thread is running or not.
    """
    global epost_downloader_thread_running
    epost_downloader_thread_running = running


def get_epost_downloader_thread_running():
    """
    Get the status of the epost downloader thread.

    :return: A boolean indicating whether the epost downloader thread is running or not.
    """
    return epost_downloader_thread_running


def run_subprocess_with_monitoring(process, update_ui: bool = True):
    """
    Run a subprocess while monitoring a condition.
    This function sets the epost downloader pid and then continuously monitors the provided subprocess
    until it terminates or a stop condition is met.

    :param process: A subprocess.Popen object representing the subprocess to be run and monitored.
    :param update_ui: (Optional) Boolean indicating whether to update the user interface during the process.
                      Defaults to True.
    """
    set_epost_downloader(process.pid)

    while True:
        # Check if the process has terminated
        return_code = process.poll()
        if return_code is not None:
            break

        # Check flag to determine whether to stop the program
        run_process = eel.getEpostDownloaderRunning()()
        if not run_process:
            process.terminate()
            set_epost_downloader_thread_running(False)
            break

        try:
            out, err = process.communicate(timeout=0.5)
        except subprocess.TimeoutExpired:
            out, err = None, None

        if out and update_ui:
            eel.handleUpdateTextAreaEpostDownloader(f"{out}\n")


def run_subprocess_epost_downloader_track(token: str, start_date: str, end_date: str, update_ui: bool = True):
    """
    Run a subprocess to track epost downloader progress.

    :param token: The token required for authentication.
    :param start_date: The start date for tracking.
    :param end_date: The end date for tracking
    :param update_ui: (Optional) Boolean indicating whether to update the user interface during the process.
                      Defaults to True.
    """
    vtp = VTP(token, vtp_path)
    track_process = vtp.track(start_date, end_date)
    run_subprocess_with_monitoring(track_process, update_ui=update_ui)


def run_subprocess_epost_downloader_receive(token: str, start_date: str, end_date: str, download_all: bool,
                                            update_ui: bool = True):
    """
    Run a subprocess to track epost downloader progress.

    :param token: The token required for authentication.
    :param start_date: The start date for receiving messages.
    :param end_date: The end date for receiving messages.
    :param download_all: Indicates whether to download all available messages.
    :param update_ui: (Optional) Boolean indicating whether to update the user interface during the process.
                      Defaults to True.
    """
    vtp = VTP(token, vtp_path)
    receive_process = vtp.receive(start_date, end_date, download_all, "downloads")
    run_subprocess_with_monitoring(receive_process, update_ui=update_ui)


def run_subprocesses_epost_downloader(token: str, start_date: str, end_date: str, download_all: bool):
    """
    Run subprocesses for epost downloader operations.

    This function initiates two subprocesses: one for tracking messages and one for receiving messages
    using the provided token, start date, end date, and download option. It handles exceptions and updates
    the user interface accordingly.

    :param token: The token required for authentication.
    :param start_date: The start date for receiving and tracking messages.
    :param end_date: The end date for receiving and tracking messages.
    :param download_all: Indicates whether to download all available messages.
    """
    try:
        run_subprocess_epost_downloader_track(token, start_date, end_date, update_ui=False)
        run_subprocess_epost_downloader_receive(token, start_date, end_date, download_all)
    except Exception as e:
        eel.handleUpdateTextAreaEpostDownloader(str(e) + "\n")
        eel.handleUpdateTextAreaEpostDownloader(
            "An error occurred. Please check the logs when the task is complete.\n")


def move_folders_to_triage():
    """
    Moves folders and their contents from the 'downloads' directory to the 'triage' folder.
    """
    other_path = TRIAGE_FOLDER_PATH

    folders = [folder for folder in os.listdir(os.path.join("downloads")) if
               os.path.isdir(os.path.join("downloads", folder))]

    for folder in folders:
        for item in os.listdir(os.path.join("downloads", folder)):
            if "ghost" not in item.lower() and "hc" not in item.lower():
                if not os.path.exists(os.path.join(other_path, folder)):
                    os.mkdir(os.path.join(other_path, folder))

                shutil.move(os.path.join("downloads", folder, item), os.path.join(other_path, folder))

            elif "ghost" in item.lower():
                if not os.path.exists(os.path.join(other_path, folder, item)):
                    os.mkdir(os.path.join(other_path, folder, item))

                ghost_folders = [ghost_folder for ghost_folder in os.listdir(os.path.join("downloads", folder, item)) if
                                 os.path.isdir(os.path.join("downloads", folder, item, ghost_folder))]

                for ghost_f in ghost_folders:
                    shutil.move(os.path.join("downloads", folder, item, ghost_f),
                                os.path.join(other_path, folder, item))

            elif "hc" in item.lower():
                if not os.path.exists(os.path.join(other_path, folder, item)):
                    os.mkdir(os.path.join(other_path, folder, item))

                hc_folders = [hc_folder for hc_folder in os.listdir(os.path.join("downloads", folder, item)) if
                              os.path.isdir(os.path.join("downloads", folder, item, hc_folder))]

                for hc_f in hc_folders:
                    shutil.move(os.path.join("downloads", folder, item, hc_f), os.path.join(other_path, folder, item))


def cleanup_downloads_folder():
    """
    Removes empty subdirectories from the "downloads" folder.
    """
    for folder in os.listdir("downloads"):
        folder_path = os.path.join("downloads", folder)
        if os.path.isdir(folder_path):
            if not check_path_for_files(folder_path):
                shutil.rmtree(folder_path)


@eel.expose
def run_epost_downloader(token, username, password, start_date, end_date, download_all: bool,
                         categorize_messages: bool, scrape_epost_connect: bool, move_messages_triage: bool):
    date_validation = DateValidation(start_date, end_date)

    if not date_validation.check_date_format():
        return "error - invalid date"

    if not date_validation.compare_date():
        return "error - invalid date"

    if date_validation.is_future_date():
        return "error - invalid date"

    if not os.path.isdir("downloads"):
        os.mkdir("downloads")

    if not os.path.isdir(epost_connect_path):
        return "error - missing epost folder"

    if not os.path.isdir(logs_path):
        os.makedirs(logs_path)

    is_downloader_issue = False
    log_parser = VTPLogParser(logs_path)
    date_list = generate_date_range(start_date, end_date)

    # Only scrape epost connect if the checkbox in the frontend is checked
    if scrape_epost_connect:
        if not os.path.isfile("chromedriver.exe"):
            return "error - missing chromedriver"

        # Reset globals
        global epost_downloader_connect_driver, is_epost_downloader_connect_scrape_failed
        epost_downloader_connect_driver = None
        is_epost_downloader_connect_scrape_failed = False

        if username == "" or password == "":
            return "error - invalid username or password"

        # Start the process of scraping messages from epost connect in a separate thread
        epost_connect_thread = threading.Thread(target=run_epost_connect_scrape, args=(username, password,))
        epost_connect_thread.start()

        # Stop the app from going any further until the epost scrape is done
        while epost_connect_thread.is_alive():
            is_running = eel.getEpostDownloaderRunning()()

            if not is_running:
                if epost_downloader_connect_driver is None:
                    return "error - issue with chromedriver"

                epost_downloader_connect_driver.quit()
                epost_downloader_connect_driver = None
                return "error - stopped"

            time.sleep(3)

        # Stop the app because something went wrong while running the epost connect scrape
        if is_epost_downloader_connect_scrape_failed:
            if epost_downloader_connect_driver is None:
                return "error - issue with chromedriver"

            epost_downloader_connect_driver.quit()
            epost_downloader_connect_driver = None
            return "error - epost connect scrape"

    # Run VTP track for the date range to be able to get count of unique message IDs
    eel.handleUpdateTextAreaEpostDownloader("-" * 75 + "\n")
    eel.handleUpdateTextAreaEpostDownloader(f"Running VTP Track to get list of valid message IDs\n")
    eel.handleUpdateTextAreaEpostDownloader("-" * 75 + "\n")

    run_subprocess_epost_downloader_track(token, start_date, end_date)
    time.sleep(3)
    # Needed to identify ghost messages and update the progress in the UI
    valid_track_ids = log_parser.get_vtp_track_valid_message_ids(1)

    # If there are no track IDs the epost downloader won't be able to update the progress in the UI or catch ghost
    # messages and something probably went wrong while running VTP Track on the date range.
    if valid_track_ids == 0:
        return "error"

    eel.handleUpdateTextAreaEpostDownloader(f"Valid IDs for the date range:\n {valid_track_ids}\n")

    # Start thread to check number of messages downloaded and update UI
    t1 = threading.Thread(target=update_epost_downloader_progress_user_interface)
    set_epost_downloader_thread_running(True)
    t1.start()

    for date in date_list:
        run_process = eel.getEpostDownloaderRunning()()

        if run_process:
            eel.handleUpdateTextAreaEpostDownloader("-" * 75 + "\n")
            eel.handleUpdateTextAreaEpostDownloader(f"Downloading files for {date}\n")
            eel.handleUpdateTextAreaEpostDownloader("-" * 75 + "\n")
            # Run VTP track and receive for a single day in the range
            run_subprocesses_epost_downloader(token, date, date, download_all)
        else:
            set_epost_downloader_thread_running(False)
            return "error - stopped"

        if not log_parser.verify_access_token():
            set_epost_downloader_thread_running(False)
            return "error - invalid access token"

        run_process = eel.getEpostDownloaderRunning()()
        if not run_process:
            set_epost_downloader_thread_running(False)
            return "error - stopped"

        if not log_parser.verify_vtp_receive_successful():
            is_downloader_issue = True
            eel.handleUpdateTextAreaEpostDownloader(
                "Something went wrong while downloading. Please check the logs when the task is complete.\n")

        time.sleep(5)

    set_epost_downloader_thread_running(False)

    if log_parser.verify_no_messages_to_download(len(date_list)):
        return "error - no messages to download"

    try:
        eel.handleUpdateTextAreaEpostDownloader("Adding logs\n")
        add_logs_user_interface(len(date_list))
        eel.handleUpdateTextAreaEpostDownloader("Adding logs was completed successfully\n")
    except:
        eel.handleUpdateTextAreaEpostDownloader("Adding logs failed\n")

    if categorize_messages:

        try:
            eel.handleUpdateTextAreaEpostDownloader("Categorizing files\n")
            categorize_messages_obj = CategorizeMessages("downloads", valid_message_ids=valid_track_ids)
            categorize_messages_obj.categorize_files()
            categorize_messages_obj.categorize_folders()
            eel.handleUpdateTextAreaEpostDownloader("Categorizing files was completed successfully\n")

        except Exception as e:
            eel.handleUpdateTextAreaEpostDownloader("Categorizing files failed\n")

            # Log error to a file.
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                filename="categorize_messages_exception.log",
                filemode="w"
            )
            logging.exception(e, exc_info=e)

            if is_downloader_issue:
                return "error - categorizing files and downloader issue"

            return "error - categorizing files"

    # Move the messages to the triage folder if the box is checked.
    if move_messages_triage:

        if not os.path.exists(TRIAGE_FOLDER_PATH):
            if is_downloader_issue:
                eel.handleUpdateTextAreaEpostDownloader("Triage folder not found and something went wrong during the "
                                                        "file download, it may be incomplete.\n")
                return "error - triage folder not found and downloader issue"
            else:
                eel.handleUpdateTextAreaEpostDownloader("Triage folder not found.\n")
                return "error - triage folder not found"

        try:
            eel.handleUpdateTextAreaEpostDownloader("Moving messages to the triage folder\n")
            move_folders_to_triage()
            time.sleep(3)
            cleanup_downloads_folder()
            eel.handleUpdateTextAreaEpostDownloader("Moving messages was completed successfully\n")

        except:

            if is_downloader_issue:
                eel.handleUpdateTextAreaEpostDownloader("Something went wrong while moving the messages to the triage "
                                                        "folder and during the file download, it may be incomplete.\n")
                return "error - issue moving messages to triage folder and downloader issue"
            else:
                eel.handleUpdateTextAreaEpostDownloader("Something went wrong while moving the messages to the triage "
                                                        "folder.\n")
                return "error - issue moving messages to triage folder"

    if is_downloader_issue:
        eel.handleUpdateTextAreaEpostDownloader("Something went wrong during the file download, it may be incomplete.\n")
        return "error - downloader issue"

    return "success"


@eel.expose
def export_receive_logs_excel(number_of_logs: int) -> str:
    """
    Exports receive logs to an Excel file.

    :param number_of_logs: The number of logs to include in the Excel file.
    :return: "success" if the operation succeeds, "error" otherwise.
    """
    try:
        log_parser = VTPLogParser(logs_path)
        log_parser.create_excel_from_recent_logs("receive", number_of_logs)
    except:
        return "error"

    return "success"


@eel.expose
def export_track_logs_excel(number_of_logs: int) -> str:
    """
    Exports tracking logs to an Excel file.

    :param number_of_logs: The number of logs to include in the Excel file.
    :return: "success" if the operation succeeds, "error" otherwise.
    """
    try:
        log_parser = VTPLogParser(logs_path)
        log_parser.create_excel_from_recent_logs("tracking", number_of_logs)
    except:
        return "error"

    return "success"


def add_logs_user_interface(number_of_logs: int):
    """
    Adds logs to tables in the Log tab of the epost downloader UI.

    :param number_of_logs: The number of recent log files to retrieve.
    """
    log_parser = VTPLogParser(logs_path)

    receive_log_paths = log_parser.get_recent_logs("receive", number_of_logs)
    track_log_paths = log_parser.get_recent_logs("tracking", number_of_logs)

    track_rows = []
    receive_rows = []
    for track_log, receive_log in zip(track_log_paths, receive_log_paths):
        track_rows.extend(log_parser.get_log_rows(track_log))
        receive_rows.extend(log_parser.get_log_rows(receive_log))

    eel.addTableToTabEpostDownloader("epostDownloaderReceiveLogTable", "VTP Receive Log",
                                     VTPReceiveLogFields.get_values(),
                                     receive_rows, number_of_logs)
    eel.addTableToTabEpostDownloader("epostDownloaderTrackLogTable", "VTP Track Log", VTPTrackLogFields.get_values(),
                                     track_rows, number_of_logs)


def update_epost_downloader_progress_user_interface():
    """
    Update the user interface with the progress of the epost downloader.

    Continuously updates the UI with the current message count from the downloads folder
    as long as the epost downloader thread is running.
    """
    while get_epost_downloader_thread_running():
        count = get_message_count_from_downloads_folder("downloads")
        eel.updateMessageCountEpostDownloader(count)
        time.sleep(1)


def run_epost_connect_scrape(username: str, password: str):
    """
    Scrapes the ePost Connect website for new messages and updates the UI.

    :param username: The username for logging into ePost Connect.
    :param password: The password for logging into ePost Connect.
    """
    global epost_downloader_connect_driver, is_epost_downloader_connect_scrape_failed

    eel.handleUpdateTextAreaEpostDownloader("-" * 75 + "\n")
    eel.handleUpdateTextAreaEpostDownloader(f"Scraping ePost Connect website for new messages\n")
    eel.handleUpdateTextAreaEpostDownloader("-" * 75 + "\n")

    try:
        web_scrape_messages = WebScrapeMessages(username, password)
        epost_downloader_connect_driver = web_scrape_messages.driver
        # Generate report of new messages in epost connect
        web_scrape_messages.scrape_new()
        is_epost_downloader_connect_scrape_failed = False
        eel.handleUpdateTextAreaEpostDownloader(f"ePost Connect scrape was completed successfully\n")
    except:
        is_epost_downloader_connect_scrape_failed = True
        eel.handleUpdateTextAreaEpostDownloader(f"ePost Connect scrape failed\n")
