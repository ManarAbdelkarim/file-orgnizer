import argparse
import logging
import os
from abc import ABC, abstractmethod
from typing import Dict



class FileOrganizer(ABC):
    def __init__(self, folder_path: str):
        self.folder_path = folder_path

    def check_folder_existence(self) -> bool:
        """
        This method checks if the specified folder path exists and is a
            directory.
        :returns: bool
        """
        if not os.path.exists(self.folder_path):
            logging.error("The specified folder path does not exist.")
            return False
        return True

    def check_folder_is_directory(self) -> bool:
        """
        This method checks if the specified path is a
            directory.
        :returns: bool
        """
        if not os.path.isdir(
                self.folder_path):
            logging.error("The specified path is not a directory.")
            return False
        return True

    @staticmethod
    def check_file_has_extension(file_name: str) -> bool:
        """
        this method checks if the file has an extension
        :param file_name: (str) The name of the file.
        :returns: bool
        """
        if not "." in file_name:
            logging.error(f"File '{file_name}' has no extension.")
            return False
        return True

    @staticmethod
    def check_file_extension_is_allowed(file_name: str, extensions: []) -> bool:
        """this method Checks if the file has a valid extension
        :param extensions: (list) list of allowed extensions
        :param file_name: (str) The name of the file.
        :returns: bool
        """
        # Get the file extension
        _, file_extension = os.path.splitext(file_name)

        if file_extension not in extensions:
            logging.error(f"File '{file_name}' extension is not allowed.")
            return False
        return True

    @abstractmethod
    def group_files(self) -> None:
        pass

class FileOrganizerByFirstWord(FileOrganizer):
    def __init__(self, folder_path: str ):
        super().__init__(folder_path)

    def extract_first_word_from_filename(self, file_name: str) -> str:
        """
        This static method is responsible for extracting the first word from the
            file name.
        :param file_name: (str) The name of the file.
        :returns: str
        """
        language: [None| str] = None
        has_extension = self.check_file_has_extension(file_name)
        is_text_file = self.check_file_extension_is_allowed(file_name,
                                                            ['.txt'])
        if has_extension and is_text_file:
            # Extract the first word from the file name by
            # splitting at the first "-"
            language, _ = file_name.split("-")
        return language


    def group_files(self) -> None:
        """
        This method is responsible for creating sub-folders based on their
            first word in the file name.
        :returns: None
        """
        if (not self.check_folder_existence() or
                not self.check_folder_is_directory()):
            return

        # Create a dictionary to track language folders
        language_folders: Dict[str, str] = {}

        for file_name in os.listdir(self.folder_path):
            try:
                language = self.extract_first_word_from_filename(file_name)
                if language:
                    # Create the sub-folder if it doesn't exist
                    if language not in language_folders:
                        sub_folder_path = os.path.join(self.folder_path,
                                                       language)
                        os.makedirs(sub_folder_path, exist_ok=True)
                        language_folders[language] = sub_folder_path

                    # Move the file to the respective language folder
                    src_path = os.path.join(self.folder_path, file_name)
                    dest_path = os.path.join(language_folders[language],
                                             file_name)
                    os.rename(src_path, dest_path)

            except Exception as e:
                # Log the actual error message from the caught exception
                logging.error(f"{file_name} [ERR]: {str(e)}")

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

    if enable_logging:
        # Initialize the logging if enabled
        log_filename = ".file_organizer_log.log"  # Hidden error log file
        logging.basicConfig(filename=log_filename,
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s [%(levelname)s]: %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

    organizer = FileOrganizerByFirstWord(folder_path)
    organizer.group_files()

if __name__ == "__main__":
    main()
