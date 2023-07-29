# one-k-files

The File Organizer is a Python script that helps you organize text files into sub-folders based on the first word in their file names. It accepts a folder path containing the text files and, optionally, enables logging to keep track of any issues encountered during the organization process.

## Features

- Organizes text files into sub-folders based on their first word in the file name.
- Supports logging with various log levels (ERROR, WARNING, INFO) when enabled.
- Logs are saved in a hidden .file_organizer_log.log file in the script's directory.

## Requirements

- Python 3

## Usage

1. Clone the repository:

git clone ```git@github.com:ManarAbdelkarim/one-k-files.git```

cd one-k-files

2. Run the script with the folder path containing the text files:

```python main.py <folder_path>```

3. Optional: Enable logging with the `-l` or `--logging` flag:

4. The script will create sub-folders in the specified folder based on the first word of the file names. It will then move the files into their respective sub-folders.

## Example

Let's say you have a folder named `text_files` with the following files:

- arabic-1.txt
- arabic-2.txt
- english-1.txt
- english-2.txt

Running the script:

```python main.py files -l```

After execution, the `files` folder will be organized into sub-folders as follows:

- arabic
  - arabic-1.txt
  - arabic-2.txt
- english
  - english-1.txt
  - english-2.txt