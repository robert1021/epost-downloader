import os
from xlsx_builder import XlsxBuilder
from styling import Styling
from enums import VTPReceiveLogFields, VTPTrackLogFields
from constants import GREEN_FILL_COLOR, RED_FILL_COLOR


class VTPLogParser:

    def __init__(self, log_folder_path):
        self.log_folder_path = log_folder_path

    @staticmethod
    def get_log_rows(log_file_path: str):
        with open(log_file_path) as file:
            rows = [(line.strip().split("|") if line.strip().split("|")[-1] != "" else line.strip().split("|")[:-1]) for line in file]
        return rows

    @staticmethod
    def get_log_dict(log_file_path: str):
        """
        Parses a log file and returns a dictionary containing log messages.

        :param log_file_path: The path to the log file to be parsed.
        :return: A dictionary where keys are message IDs and values are lists of message components.
        """
        with open(log_file_path) as file:
            lines = [line.strip() for line in file]

        messages_dict = {}
        for message in lines:
            split_line = message.split("|")
            message_id = split_line.pop(0)

            if split_line[-1] == "":
                split_line.pop(len(split_line) - 1)

            if message_id not in messages_dict:
                messages_dict[message_id] = []

            messages_dict[message_id].append(split_line)

        return messages_dict

    @staticmethod
    def get_log_lines(log_file_path: str):
        with open(log_file_path) as file:
            lines = [line.strip() for line in file]

        return lines

    def get_most_recent_log(self, log_type: str):
        """
        Get the most recent log file containing the log type in its name.

        :param log_type: The type of log to search for.
        :return: The path to the most recent file containing the log type in its name.
        """
        files = [file for file in os.listdir(self.log_folder_path) if
                 os.path.isfile(os.path.join(self.log_folder_path, file)) and f"{log_type}" in file]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(self.log_folder_path, x)), reverse=True)
        return os.path.join(self.log_folder_path, files[0])

    def get_recent_logs(self, log_type: str, number_of_logs: int) -> list[str]:
        """
        Retrieve the most recent log files of a specified type.

        :param log_type: The type of log files to retrieve.
        :param number_of_logs: The number of recent log files to retrieve.
        :return: A list of paths to the most recent log files.
        """
        files = [file for file in os.listdir(self.log_folder_path) if
                 os.path.isfile(os.path.join(self.log_folder_path, file)) and f"{log_type}" in file]
        files.sort(key=lambda x: os.path.getmtime(os.path.join(self.log_folder_path, x)), reverse=True)
        return [os.path.join(self.log_folder_path, file) for file in files[:number_of_logs]]

    def get_vtp_track_valid_message_ids(self, number_of_logs: int) -> list:
        track_log_paths = self.get_recent_logs("tracking", number_of_logs)
        message_ids = {}

        for track_log in track_log_paths:
            rows = self.get_log_rows(track_log)
            if rows:
                for row in rows:
                    message_ids.setdefault(row[0], "")

        return list(message_ids.keys())

    def verify_access_token(self) -> bool:
        exception_log = self.get_most_recent_log("exception")
        exception_lines = self.get_log_lines(exception_log)

        for line in exception_lines:
            if "invalid access token" in line.lower():
                return False
        return True

    def verify_vtp_receive_successful(self) -> bool:
        exception_log = self.get_most_recent_log("exception")
        exception_lines = self.get_log_lines(exception_log)
        return False if exception_lines else True

    def verify_no_messages_to_download(self, number_of_logs: int) -> bool:
        """
        Verify if there are no messages to download based on the specified number of logs.

        :param number_of_logs: The number of recent log files to retrieve.
        :return: True if there are no messages to download for all specified logs, False otherwise.
        """
        receive_log_paths = self.get_recent_logs("receive", number_of_logs)
        no_message_to_download_paths = []

        for receive_log in receive_log_paths:
            rows = self.get_log_rows(receive_log)
            if rows:
                if rows[0][6] == "You have no messages to download":
                    no_message_to_download_paths.append(receive_log)

        return True if len(no_message_to_download_paths) == number_of_logs else False

    def create_excel(self, log_file_path: str):
        """
        Create an Excel file based on the provided log file path.

        :param log_file_path: The path to the log file.
        """
        xlsx_builder = XlsxBuilder()

        headers = None
        if "tracking" in log_file_path.lower():
            headers = VTPTrackLogFields.get_values()

        elif "receive" in log_file_path.lower():
            headers = VTPReceiveLogFields.get_values()

        log_rows = self.get_log_rows(log_file_path)
        log_rows.insert(0, headers)

        xlsx_builder.add_sheet("Log", log_rows)
        xlsx_builder.save(os.path.basename(log_file_path.replace(".log", ".xlsx")))

    def create_excel_from_recent_logs(self, log_type: str, number_of_logs: int):
        """
        Create an Excel file based on the most recent log files of a certain type.

        :param log_type: The type of log files to use.
        :param number_of_logs: The number of recent log files to use.
        """
        log_paths = self.get_recent_logs(log_type, number_of_logs)
        xlsx_builder = XlsxBuilder()

        headers = None
        if log_type.lower() == "tracking":
            headers = VTPTrackLogFields.get_values()

        elif log_type.lower() == "receive":
            headers = VTPReceiveLogFields.get_values()

        rows = []
        for log in log_paths:
            rows.extend(self.get_log_rows(log))

        rows.insert(0, headers)
        sheet_name = "Log"
        filename = f"{log_type}_log.xlsx"
        # Create Excel file
        xlsx_builder.add_sheet(sheet_name, rows)
        xlsx_builder.save(filename)
        # Style sheet
        styling = Styling(filename)
        styling.apply_basic_styling(sheet_name)

        if log_type.lower() == "receive":
            for idx, row in enumerate(rows):
                if row[6] == "Success":
                    styling.color_row(sheet_name, GREEN_FILL_COLOR, idx + 1, idx + 1)
                elif row[6] == "Failure":
                    styling.color_row(sheet_name, RED_FILL_COLOR, idx + 1, idx + 1)
