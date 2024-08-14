import re
import os
import shutil

import docx
import dateutil.parser
import datetime
from federal_calendar import FederalCalendar
from datetime import datetime
from datetime import timedelta
import time
from docx.enum.style import WD_STYLE_TYPE
from docx.shared import Pt
from docx.shared import Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from win32api import GetSystemMetrics
import sys


def get_screen_size():
    return GetSystemMetrics(0), GetSystemMetrics(1)


def update_user_chrome_preferences(disable_crash_popup: bool = True):
    """
    Updates user chrome preference file.

    :param disable_crash_popup: Will enable / disable crash pop-up that restores session.
    """
    filepath = fr'C:\Users\{os.getlogin()}\AppData\Local\Google\Chrome\User Data\Default\Preferences'

    # Update file
    with open(filepath, 'r+', encoding='utf-8') as file:
        # read entire content of file into memory
        content = file.read()
        # Change preferences
        if disable_crash_popup:
            content = re.sub(r'"exit_type":"Crashed"', r'"exit_type":"Normal"', content)
        elif not disable_crash_popup:
            content = re.sub(r'"exit_type":"Normal"', r'"exit_type":"Crashed"', content)

        # Return pointer to top of file
        file.seek(0)
        # Clear
        file.truncate()
        # Write updated content
        file.write(content)


def add_content_to_word_doc(document, content,
                            font_name='Calibri', font_size=11, line_spacing=1.15, space_before=0, space_after=8,
                            align='left', left_indent=0.0, keep_together=True, keep_with_next=False,
                            page_break_before=False,
                            widow_control=False, set_bold=False, set_italic=False, set_underline=False,
                            set_all_caps=False,
                            style_name=""):
    alignment_dict = {'justify': WD_PARAGRAPH_ALIGNMENT.JUSTIFY,
                      'center': WD_PARAGRAPH_ALIGNMENT.CENTER,
                      'centre': WD_PARAGRAPH_ALIGNMENT.CENTER,
                      'right': WD_PARAGRAPH_ALIGNMENT.RIGHT,
                      'left': WD_PARAGRAPH_ALIGNMENT.LEFT}

    paragraph = document.add_paragraph(content)
    paragraph.style = document.styles.add_style(style_name, WD_STYLE_TYPE.PARAGRAPH)
    font = paragraph.style.font
    font.name = font_name
    font.size = Pt(font_size)
    font.bold = set_bold
    font.italic = set_italic
    font.all_caps = set_all_caps
    font.underline = set_underline
    paragraph_format = paragraph.paragraph_format
    paragraph_format.alignment = alignment_dict.get(align.lower())
    paragraph_format.left_indent = Inches(left_indent)
    paragraph_format.space_before = Pt(space_before)
    paragraph_format.space_after = Pt(space_after)
    paragraph_format.line_spacing = line_spacing
    paragraph_format.keep_together = keep_together
    paragraph_format.keep_with_next = keep_with_next
    paragraph_format.page_break_before = page_break_before
    paragraph_format.widow_control = widow_control


def generate_date_range(start_date: str, end_date: str) -> list[str]:
    """
    Generate a list of dates within the specified range.

    :param start_date: The start date of the range in the format "MM/DD/YYYY".
    :param end_date: The end date of the range in the format "MM/DD/YYYY".
    :return: A list of dates within the specified range in the format "MM/DD/YYYY".
    """
    start = datetime.strptime(start_date, "%m/%d/%Y")
    end = datetime.strptime(end_date, "%m/%d/%Y")
    generated_dates = [(start + timedelta(days=x)).strftime("%m/%d/%Y") for x in range(0, (end - start).days + 1)]
    return generated_dates


def get_timestamp() -> str:
    """
    Gets the current timestamp in the format 'YYYYMMDD-HHMMSS'.

    :return: A string representing the current timestamp in the format 'YYYYMMDD-HHMMSS'.
    """
    return time.strftime("%Y%m%d-%H%M%S")


def has_downloaded_file_pattern(filename: str):
    """
    Checks if the concerned file name has the same pattern of files downloaded by VTP

    :param filename: name of the concerned file
    :return: boolean on whether matches the pattern or not
    """
    pattern = re.compile(r"^[0-9]{5,7}-[0-9]{5,7}[_|-].+$", re.IGNORECASE)
    return pattern.match(filename)


def is_downloaded_message_file(filename: str):
    """
    Checks if the concerned file is a message file downloaded by VTP

    :param filename: name of the concerned file
    :return: boolean on whether matches the pattern or not
    """
    # Could be expanded to check the content as well, and not just rely on the file name
    pattern = re.compile(r"^[0-9]{5,7}-[0-9]{5,7}_message.txt$", re.IGNORECASE)
    return pattern.match(filename)


def get_expected_message_filename(conversation_id: int, message_id: int) -> str:
    """
    Provides the expected name of the message file associated to this message when downloaded

    :param conversation_id: ID of the ePost Connect conversation
    :param message_id: ID of the ePost Connect message
    :return: expected name of the message file
    """
    return f"{conversation_id}-{message_id}_message.txt"


def get_conversation_id(filename: str) -> int:
    """
    Gets the conversation ID of the downloaded file

    :param filename: name of the downloaded file
    :return: conversation ID in integer
    """
    return int(filename.split("-")[0])


def get_message_id(filename: str) -> int:
    """
    Gets the message ID of the downloaded file

    :param filename: name of the downloaded file
    :return: message ID in integer
    """
    return int(re.split("-|_", filename)[1])


def get_attachment_info(attachment_filename: str):
    """
    Gets the attachment ID and name of the downloaded attachment file

    :param attachment_filename: name of the downloaded file
    :return: list of attachment ID and name
    """
    filename_split = re.split("-|_", attachment_filename, 3)
    return int(filename_split[2]), filename_split[3]


def get_folder_name(filename: str) -> str:
    folder_name = filename.split("_")[0]

    if folder_name.count("-") > 1:
        folder_name = "-".join(folder_name.split("-")[:2])

    return folder_name


def parse_txt_message(message_path: str) -> dict:
    """
    Parses a text message file and extracts relevant information.

    :param message_path: The path to the text message file to parse.
    :return: dict: A dictionary containing the parsed information with the following keys:
            - 'conversation id' (int): The ID of the conversation.
            - 'message id' (int): The ID of the message.
            - 'message owner' (str): The owner of the message.
            - 'message participants' (str): The participants of the message.
            - 'conversation title' (str): The title of the conversation.
            - 'company code' (int): The code of the company related to the conversation.
            - 'date sent' (str): The date and time the message was sent (in string format).
            - 'date expires' (str): The date and time the message expires (in string format).
            - 'conventional name' (str): A conventional name for the message based on company code and sent date.
            - 'message body' (str): The body of the message.
    """
    # Parse the message file
    with open(message_path, "r") as messageFile:
        message_lines = messageFile.readlines()
        line_index = 0
        for line in message_lines:
            if line.lower().startswith("conversation id"):
                conversation_id = int(line.split(":", 1)[1].strip())
            elif line.lower().startswith("message id"):
                message_id = int(line.split(":", 1)[1].strip())
            elif line.lower().startswith("message owner"):
                message_owner = line.split(":", 1)[1].strip()
            elif line.lower().startswith("participants"):
                message_participants = line.split(":", 1)[1].strip()
            elif line.lower().startswith("conversation name"):
                conversation_title = line.split(":", 1)[1].strip()
                company_code = int(conversation_title[:5])
            elif line.lower().startswith("sent"):
                sent_datetime_str = line.split(":", 1)[1].strip()
                sent_datetime = dateutil.parser.parse(sent_datetime_str)
            elif line.lower().startswith("expires"):
                expiry_datetime_str = line.split(":", 1)[1].strip()
                expiry_datetime = dateutil.parser.parse(expiry_datetime_str)
            elif line.startswith("-----------------"):
                message_body = "".join(message_lines[line_index + 1:])
                break
            line_index += 1

    fed_cal = FederalCalendar()
    conventional_name = str(company_code) + "-" + fed_cal.get_business_date(sent_datetime).strftime(
        "%b %d, %Y") + " - " + sent_datetime.strftime("%H%M%S")

    # Get the business date to label on the file
    message_word_doc_date_label = fed_cal.get_business_date(sent_datetime)
    new_filename = f"epost-{message_word_doc_date_label}.docx"

    return {
        "conversation id": conversation_id,
        "message id": message_id,
        "message owner": message_owner,
        "message participants": message_participants,
        "conversation title": conversation_title,
        "company code": company_code,
        "date sent": sent_datetime,
        "date sent str": sent_datetime_str,
        "date expires": expiry_datetime_str,
        "conventional name": conventional_name,
        "message body": message_body,
        "new filename": new_filename
    }


def generate_word_doc_message(message_data: dict, attachments: list, save_folder: str) -> str:
    """
    Generates the Word document version of the categorized message based on the template requested by SASD team

    :param message_data:
    :param attachments: A list of file names representing attachments to be included in the Word document.
    :param save_folder:
    :return: The path to the newly generated Word document.
    """
    message_word_doc = docx.Document()
    add_content_to_word_doc(message_word_doc
                            ,
                            f"{message_data['message owner']} ({message_data['company code']})"
                            , set_bold=True
                            , style_name="MessageOwner"
                            )
    add_content_to_word_doc(message_word_doc
                            , f"Sent: {message_data['date sent str']}"
                            , left_indent=3.6
                            , space_after=6
                            , style_name="SentTimestamp"
                            )
    add_content_to_word_doc(message_word_doc
                            , f"Expired: {message_data['date expires']}"
                            , left_indent=3.6
                            , space_after=18
                            , style_name="ExpiryTimestamp"
                            )
    add_content_to_word_doc(message_word_doc
                            , message_data["message body"]
                            , style_name="MessageBody"
                            )
    add_content_to_word_doc(message_word_doc
                            , f"Attachments [{len(attachments)} files]:"
                            , set_bold=True
                            , style_name="AttachmentsTitle"
                            )
    for i, att in enumerate(attachments):
        add_content_to_word_doc(message_word_doc
                                ,
                                f"●  {att}"
                                , space_after=0
                                , style_name=f"AttachmentItem-{i}"
                                )

    new_message_path = os.path.join(save_folder, message_data["new filename"])
    message_word_doc.save(new_message_path)
    return new_message_path


def is_hc_email(email: str) -> bool:
    """
    Check if the given email address belongs to Health Canada.

    :param email: The email address to be checked.
    :return: True if the email address belongs to Health Canada, False otherwise.
    """
    if email.endswith("@hc-sc.gc.ca"):
        return True

    return False


def is_ghost_message(message_id: str, valid_message_ids: list) -> bool:
    """
    Check if a message ID is a ghost message, i.e., if it's not included in the list of valid message IDs.

    :param message_id: The ID of the message to be checked.
    :param valid_message_ids: A list of valid message IDs.
    :return: True if the message ID is a ghost message, False otherwise.
    """
    if message_id not in valid_message_ids:
        return True

    return False


def get_file_without_id(file: str) -> str:
    """
    Extracts the portion of the file name after the first underscore ('_').

    :param file: The file name.
    :return: The portion of the file name after the first underscore, or the original file name if no underscore is present.
    """
    return file.split("_", maxsplit=1)[1] if file.find("_") != -1 else file


def get_message_count_from_downloads_folder(download_path: str) -> int:
    """
    Count the number of message files in the specified folder, excluding ghost messages.

    :param download_path: The path to the folder containing message files.
    :return: The number of message files found in the folder.
    """
    messages = [file for file in os.listdir(download_path) if
                os.path.isfile(os.path.join(download_path, file)) and file.endswith("_message.txt")]

    return len(messages)


def get_file_size_kilobytes(file_path: str) -> float:
    """
    Get the size of a file in kilobytes.

    :param file_path: The path to the file.
    :return: Size of file in kilobytes (KB).
    """
    return float(f"{(os.path.getsize(file_path) / 1024):.2f}")


def get_file_size_megabytes(file_path: str) -> float:
    """
    Get the size of a file in megabytes.

    :param file_path: The path to the file.
    :return: Size of file in megabytes (MB).
    """
    return float(f"{((os.path.getsize(file_path) / 1024) / 1024):.2f}")


def get_file_size_gigabytes(file_path: str) -> float:
    """
    Get the size of a file in gigabytes.

    :param file_path: The path to the file.
    :return: Size of file in gigabytes (GB).
    """
    return float(f"{(((os.path.getsize(file_path) / 1024) / 1024) / 1024):.2f}")


def get_file_size_formatted(file_path: str) -> str:
    file_size = os.path.getsize(file_path)

    if file_size / 1024 < 1000:
        return f"{(file_size / 1024):.2f} KB"

    elif (file_size / 1024) / 1024 < 1000:
        return f"{((file_size / 1024) / 1024):.2f} MB"

    else:
        return f"{(((file_size / 1024) / 1024) / 1024):.2f} GB"


def attempt_rename(source: str, destination: str, amount: int):
    """
    Attempt to rename a file or directory from `source` to `destination`.

    :param source: The current path of the file or directory to be renamed.
    :param destination: The new path where the file or directory should be renamed to.
    :param amount: Number of attempts to rename (retry attempts).

    Raises:
        Exception: If renaming fails after all retry attempts.
    """
    success = False

    for i in range(amount):
        try:
            os.rename(source, destination)
            success = True
            break
        except:
            time.sleep(3)

    if not success:
        raise Exception("Rename has failed.")


def get_count_similar_folder_names(path: str, folder_name: str) -> int:
    """
    Count the number of folders in the specified path that contain a similar folder name.

    :param path: The path of the directory to search.
    :param folder_name: The name of the folder to search for within other folder names.
    :return: The number of folders containing the specified folder name.
    """
    return len(
        [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder)) and folder_name in folder])


def generate_unique_folder_name(path: str, folder_name: str) -> str:
    """
    Generate a unique folder name based on the given folder name, ensuring it is unique within the specified path.

    :param path: The path where the folder will reside.
    :param folder_name: The base folder name to check for uniqueness.
    :return: A folder name that is unique within the path.
    """
    similar_count = get_count_similar_folder_names(path, folder_name)
    return folder_name if similar_count == 0 else f"{folder_name} ({similar_count})"


def get_frozen_status() -> bool:
    """
    Check if the current Python environment is frozen.

    :return: True if the environment is frozen (e.g., packaged into an executable), False otherwise.
    """
    if getattr(sys, "frozen", False):
        return True
    else:
        return False


def attempt_delete_folder(folder_path: str, retry=10, wait=3):
    """
    Attempts to delete a folder with retries if the deletion fails.

    :param folder_path: Path to the folder to be deleted.
    :param retry: Number of retry attempts. Defaults to 10
    :param wait: Delay in seconds between retries. Defaults to 3.

    Raises:
        Exception: If folder deletion fails after the specified number of retries.
    """
    success = False

    for i in range(0, retry):
        try:
            shutil.rmtree(folder_path)
            success = True
            break
        except:
            time.sleep(wait)

    if not success:
        raise Exception("Folder delete has failed.")
