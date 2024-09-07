import os
import glob

def delete_all_files_in_directories(directories):
    try:
        for directory in directories:
            if os.path.exists(directory) and os.path.isdir(directory):
                files = glob.glob(os.path.join(directory, "*"))
                for file_path in files:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Файл {file_path} был удален.")
                    else:
                        print(f"{file_path} не является файлом.")
            else:
                print(f"{directory} не является допустимой директорией.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")