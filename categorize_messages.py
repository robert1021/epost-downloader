import os
import shutil
from utilities import get_folder_name, generate_word_doc_message, get_file_without_id, parse_txt_message, \
    get_message_id, is_hc_email, is_ghost_message, get_file_size_formatted, attempt_rename, generate_unique_folder_name, attempt_delete_folder
import time


class CategorizeMessages:
    """
    Categorizes messages in a folder based on the message type.
    ----------------------------------------------------------------
    Attributes
        path: str
            The path of the folder containing the messages.
    ----------------------------------------------------------------
    Methods
        categorize_files()
            Categorizes the files in the folder based on the message type.
    """

    def __init__(self, path: str, valid_message_ids: list = None):
        self.path = path
        self.valid_message_ids = valid_message_ids
        self.ghost_path = os.path.join(self.path, "ghost")
        self.hc_path = os.path.join(self.path, "hc")

    def categorize_files(self):
        """
        Categorizes the files in the folder
        """
        files = [file for file in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, file))]
        file_count = len(files)
        count = 0

        file_list = []
        for file in files:

            if count == file_count:
                break

            message_id = str(get_message_id(file))
            folder_name = get_folder_name(file)
            source_file_path = os.path.join(self.path, file)
            target_folder_path = os.path.join(self.path, folder_name)
            message_data_dict = None
            is_ghost = False
            is_hc = False
            # -------------------- .txt file is modified and converted to .docx file --------------------
            if not file.endswith("_message.txt"):
                file_list.append(f"{get_file_without_id(file)} ({get_file_size_formatted(source_file_path)})")

            else:
                message_data_dict = parse_txt_message(source_file_path)
                source_file_path = generate_word_doc_message(message_data_dict, file_list, self.path)
                time.sleep(0.1)
                os.remove(os.path.join(self.path, file))
                file_list = []
                is_hc = is_hc_email(message_data_dict["message owner"])

                if self.valid_message_ids is not None and len(self.valid_message_ids) > 0:
                    is_ghost = is_ghost_message(message_id, self.valid_message_ids)

            # -------------------- Moving the file to the appropriate folder --------------------

            if not os.path.exists(target_folder_path):
                os.makedirs(target_folder_path)
                time.sleep(0.1)

            shutil.move(source_file_path,
                        os.path.join(target_folder_path, get_file_without_id(os.path.basename(source_file_path))))
            time.sleep(0.1)

            # # Rename target folder to conventional name
            if not file_list and message_data_dict is not None:

                if is_hc:
                    if not os.path.exists(self.hc_path):
                        os.makedirs(self.hc_path)
                        time.sleep(0.1)

                    folder_name = generate_unique_folder_name(self.hc_path, message_data_dict["conventional name"])
                    attempt_rename(target_folder_path, os.path.join(self.hc_path, folder_name), 3)

                elif is_ghost:
                    if not os.path.exists(self.ghost_path):
                        os.makedirs(self.ghost_path)
                        time.sleep(0.1)

                    folder_name = generate_unique_folder_name(self.ghost_path, message_data_dict["conventional name"])
                    attempt_rename(target_folder_path, os.path.join(self.ghost_path, folder_name), 3)

                else:
                    folder_name = generate_unique_folder_name(self.path, message_data_dict["conventional name"])
                    attempt_rename(target_folder_path, os.path.join(self.path, folder_name), 3)

            time.sleep(0.1)
            count += 1

    def categorize_folders(self):
        """
        Organizes and moves folders based on their names.
        """
        folders = [folder for folder in os.listdir(self.path) if os.path.isdir(os.path.join(self.path, folder))]

        for folder in folders:
            if "ghost" not in folder.lower() and "hc" not in folder.lower():
                folder_path = os.path.join(self.path, folder)
                new_folder_name = folder.split(",")[0].split("-")[1]
                new_folder_path = os.path.join(self.path, new_folder_name)

                if not os.path.exists(new_folder_path):
                    os.mkdir(new_folder_path)

                shutil.move(folder_path, new_folder_path)
                time.sleep(0.1)

            elif "ghost" in folder.lower():
                ghost_folders = [ghost_folder for ghost_folder in os.listdir(self.ghost_path) if
                                 os.path.isdir(os.path.join(self.ghost_path, ghost_folder))]

                for item in ghost_folders:
                    new_folder_name = item.split(",")[0].split("-")[1]
                    new_folder_path = os.path.join(self.path, new_folder_name, "ghost")

                    if not os.path.exists(new_folder_path):
                        os.makedirs(new_folder_path)

                    shutil.move(os.path.join(self.ghost_path, item), new_folder_path)
                    time.sleep(0.1)

            elif "hc" in folder.lower():
                hc_folders = [hc_folder for hc_folder in os.listdir(self.hc_path) if
                              os.path.isdir(os.path.join(self.hc_path, hc_folder))]

                for item in hc_folders:
                    new_folder_name = item.split(",")[0].split("-")[1]
                    new_folder_path = os.path.join(self.path, new_folder_name, "hc")

                    if not os.path.exists(new_folder_path):
                        os.makedirs(new_folder_path)

                    shutil.move(os.path.join(self.hc_path, item), new_folder_path)
                    time.sleep(0.1)

        # Delete hc and ghost folders from self.path if they exist to clean up
        if os.path.exists(self.ghost_path):
            attempt_delete_folder(self.ghost_path)

        if os.path.exists(self.hc_path):
            attempt_delete_folder(self.hc_path)
