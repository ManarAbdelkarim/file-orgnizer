import argparse
import datetime
import logging
import os
from typing import Dict


def extract_first_word_from_filename(file_name: str) -> str:
    """
    This method is responsible for extracting the first word from the
        file name.
    :param file_name: (str) The name of the file.
    :returns: str
    """
    # Check if the file has an extension
    if not "." in file_name:
        logging.error(f"File '{file_name}' has no extension.")
        return None

    # Get the file extension
    _, file_extension = os.path.splitext(file_name)

    # Check if the file has a valid extension (in this case, ".txt")
    if file_extension != ".txt":
        logging.error(f"File '{file_name}' is not a '.txt' file.")
        return None

    # Extract the first word from the file name by splitting at the first "-"
    language, _ = file_name.split("-")
    return language


class FileOrganizer:
    def __init__(self, folder_path: str):
        self.folder_path = folder_path

    def check_folder_existence(self) -> bool:
        """
        This method checks if the specified folder path exists and is a
            directory.
        :returns: bool
        """
        if not os.path.exists(self.folder_path) or not os.path.isdir(
                self.folder_path):
            logging.error("The specified folder path does not exist.")
            return False
        return True

    def group_files_by_first_word(self) -> None:
        """
        This method is responsible for creating sub-folders based on their
            first word in the file name.
        :returns: None
        """
        if not self.check_folder_existence():
            return

        # Create a dictionary to track language folders
        language_folders: Dict[str, str] = {}

        for file_name in os.listdir(self.folder_path):
            try:
                language = extract_first_word_from_filename(file_name)
                if language:
                    # Create the sub-folder if it doesn't exist
                    sub_folder_path = os.path.join(self.folder_path, language)
                    if language not in language_folders:
                        os.makedirs(sub_folder_path, exist_ok=True)
                        language_folders[language] = sub_folder_path

                    # Move the file to the respective language folder
                    src_path = os.path.join(self.folder_path, file_name)
                    dest_path = os.path.join(language_folders[language],
                                             file_name)
                    os.rename(src_path, dest_path)

            except Exception as e:
                # Log the actual error message from the caught exception
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                err = f'[{time}] {file_name} [ERR]: {str(e)}\n'
                logging.error(err)

        if language_folders:
            logging.info(
                "Files have been grouped into sub-folders based on first "
                "names successfully.")
        else:
            logging.info(
                "No files to group. The folder is empty of text files or "
                "all files are already organized.")


def main():
    parser = argparse.ArgumentParser(
        description="Organize text files into sub-folders based on "
                    "language names.")
    parser.add_argument("folder_path",
                        nargs="?",
                        default="files",
                        help="Path to the folder containing the text files. "
                             "Default is 'files'.")
    parser.add_argument("-l", "--logging",
                        action="store_true",
                        help="Enable error logging in the error_log file. "
                             "By default, error logging is disabled.")


    args = parser.parse_args()
    folder_path = args.folder_path
    enable_logging = args.logging

    if not os.path.exists(folder_path):
        logging.error("The specified folder path does not exist.")
        return

    if enable_logging:
        # Initialize the logging if enabled
        log_filename = ".file_organizer_log.log"  # Hidden error log file
        logging.basicConfig(filename=log_filename,
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s [%(levelname)s]: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

    organizer = FileOrganizer(folder_path)
    organizer.group_files_by_first_word()

if __name__ == "__main__":
    main()
