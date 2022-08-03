import ast
import json
import os
import argparse
from datetime import datetime

UPDATED_FILE_NAME = "log_upgrade_os_data_mergeDevOS"
PREFIX_FILE_NAME = "log_upgrade_os_data_devOS"
PREFIX_FILE_PATH = "/tmp/logs_"


def add_content_in_file(content, file_name, file_path):
    try:
        file_config = open(f"{file_path}/{file_name}", "w", encoding="utf8")
        with file_config:
            file_config.write(content)
            file_config.close()
    except Exception as exc:
        raise Exception(str(exc)) from exc


def read_content_in_file(file_name, file_path):
    config_file = open(f"{file_path}/{file_name}", encoding="utf8")
    with config_file:
        file_content = config_file.read()
        config_file.close()
    return file_content


def merge_content_for_aws_application(file_path):
    files_in_dir = os.listdir(file_path)
    modified_file_name = UPDATED_FILE_NAME + "_" + datetime.today().strftime('%Y-%m-%d-%H-%M-%S') + ".log"
    content_1, content_2, updated_list = None, None, []
    print(f"files present in directory --> {files_in_dir}")
    for file_name in files_in_dir:
        if file_name.startswith(PREFIX_FILE_NAME):
            if not content_1:
                content_1 = ast.literal_eval(read_content_in_file(file_name, file_path))
            else:
                content_2 = ast.literal_eval(read_content_in_file(file_name, file_path))
                break

    # to find out long list/array among the two list of data
    if len(content_2) > len(content_1):
        updated_content_2 = content_1
        updated_content_1 = content_2
    else:
        updated_content_1 = content_1
        updated_content_2 = content_2
    # merge the data into a new list/array
    for index, value in enumerate(updated_content_1):
        if len(updated_content_2) >= index+1:
            value.update(updated_content_2[index])
        updated_list.append(value)
    add_content_in_file(json.dumps(updated_list), modified_file_name, file_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server_ip", required=True)
    args = parser.parse_args()
    #path = "C:/my_workspace/fetch_data_from_database/learning_python"
    file_path = PREFIX_FILE_PATH + args.server_ip
    merge_content_for_aws_application(file_path)
