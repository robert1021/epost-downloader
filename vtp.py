import subprocess
from pathlib import Path


class VTP:

    def __init__(self, epost_token, epost_vtp_folder_path):
        self.epost_token = epost_token
        self.epost_vtp_folder_path = epost_vtp_folder_path

    def __vtp_api_command(self, vtp_task: str) -> str:
        client_protocols = "TLSv1.2"

        # Paths
        home_dir = self.epost_vtp_folder_path
        jvm_command_path = Path(home_dir, "jvm", "jre1.8.0_101", "bin", "java")
        class_path = str(home_dir) + r"\lib\*"
        # flags
        class_path_flag = f'-classpath "{class_path}"'
        dvtp_home_flag = f"-DVTP_HOME={str(home_dir)}"
        dclient_protocols_flag = f'-Djdk.tls.client.protocols="{client_protocols}"'

        return f"{jvm_command_path} {dclient_protocols_flag} {class_path_flag} {dvtp_home_flag} epost.connect.vtp.{vtp_task} -a {self.epost_token} "

    def receive(self, beginning_date: str, ending_date: str, download_all: bool, download_path: str, show_window=False):
        # flags
        start_date_flag = f"-beg {beginning_date}" if beginning_date != "" else ""
        end_date_flag = f"-end {ending_date}" if ending_date != "" else ""
        download_message_flag = "-all" if download_all is True else ""
        tdir_flag = f"-tdir {download_path}"
        # command
        command = f"{self.__vtp_api_command('VtpReceive')} {start_date_flag} {end_date_flag} {download_message_flag} {tdir_flag}"
        startupinfo = subprocess.STARTUPINFO()
        if not show_window:
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   startupinfo=startupinfo)
        return process

    def send(self, message_subject: str, message_body: str, recipient: str, additional_file_attachment: str = None, show_window=False):
        # flags
        subject_flag = f"-s {message_subject}"
        body_flag = f"-m {message_body}"
        recipient_flag = f"-to {recipient}"
        attachment_flag = "" if additional_file_attachment is None else f"-att {additional_file_attachment}"
        # command
        command = f"{self.__vtp_api_command('VtpSend')} {subject_flag} {body_flag} {recipient_flag} {attachment_flag}"
        startupinfo = subprocess.STARTUPINFO()
        if not show_window:
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   startupinfo=startupinfo)
        return process

    def track(self, beginning_date: str, ending_date: str, show_window=False):
        # flags
        start_date_flag = f"-beg {beginning_date}" if beginning_date != "" else ""
        end_date_flag = f"-end {ending_date}" if ending_date != "" else ""
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # command
        command = f"{self.__vtp_api_command('VtpTrack')} {start_date_flag} {end_date_flag}"
        startupinfo = subprocess.STARTUPINFO()
        if not show_window:
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                   startupinfo=startupinfo)
        return process
