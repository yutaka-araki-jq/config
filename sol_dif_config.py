import glob
import yaml
import pandas
import os


def main():
    # コンフィグ読み込み
    dir_list = []
    file_list = []
    yml_file_list = glob.glob("*.yml")
    dir_path = "./" 
    for current_dir, sub_dirs, files_list in os.walk(dir_path): 
        dir_list.append(format(current_dir))
        file_list.append(format(files_list))
    print(dir_list)
    print(file_list)
    #config = load_yml_config(yml_file_list)
    #task_group_list = get_task_group_list(config)

    # C言語ファイルへ書き出す文字列を生成
   #task_group_table = create_task_group_table(config, task_group_list)
    #task_table = create_task_table(config, task_group_list)

    # TBD:C言語ファイル書き出し
    #print(task_group_table)
    #print(task_table)


def load_yml_config(yml_file_list):
    """yamlファイル群を１つの辞書として取り込む

    Args:
        yml_file_list (list): 取り込むyamlファイルのリスト

    Returns:
        dict: yamlファイル群の情報を辞書に変換した結果
    """
    for i, file in enumerate(yml_file_list):
        with open(file, "r") as yml:
            if i == 0:
                config_integ = yaml.safe_load(yml)
            else:
                config_single = yaml.safe_load(yml)
                config_integ.update(config_single)
    return config_integ


def get_task_group_list(config):
    """コンフィグの辞書からタスクグループ名(key)のリストを取得する

    Args:
        config (dict)): コンフィグの辞書

    Returns:
        list: タスクグループ名のリスト
    """
    task_group_list = config.keys()
    return task_group_list


def create_task_group_table(config, task_group_list):
    """タスクグループテーブルを生成する

    Args:
        config (dict): コンフィグの辞書
        task_group_list (list): タスクグループ名のリスト

    Returns:
        str: タスクグループテーブル（C言語ファイル書き出し用）
    """
    task_group_table = ""
    task_group_table += "\n----------[CAST_D_SCHDL_TASK_GROUP_TABLE]----------\n"

    for task_group in task_group_list:

        # 辞書の各Valueを文字型で取得
        priority = str(config[task_group]["priority"])
        core = str(config[task_group]["core"])
        task_num = str(len(config[task_group]["task_list"]))
        next_task_group = str(config[task_group]["next_task_group"])

        # アライメント調整
        task_group_table += (task_group + ",").ljust(20) + "\t"
        task_group_table += (priority + ",").ljust(20) + "\t"
        task_group_table += (core + ",").ljust(20) + "\t"
        task_group_table += (task_num + ",").ljust(20) + "\t"
        task_group_table += (next_task_group + ",").ljust(20) + "\n"

    return task_group_table


def create_task_table(config, task_group_list):
    """タスクテーブルを作成する

    Args:
        config (dict): コンフィグの辞書
        task_group_list (list): タスクグループ名のリスト

    Returns:
        str: タスクテーブル（C言語ファイル書き出し用）
    """
    task_table = ""

    for task_group in task_group_list:

        task_table += (
            "\n----------[CAST_D_SCHDL_TASK_TABLE_"
            + str(task_group).upper()
            + "]----------\n"
        )

        for task_list in config[task_group]["task_list"]:
            for task in task_list.keys():

                # 辞書の各Valueを文字型で取得
                event_flag = str(hex(task_list[task]["event_flag"]))
                cycle_division = str(task_list[task]["cycle_division"])

                # アライメント調整
                task_table += (task + ",").ljust(20) + "\t"
                task_table += (event_flag + ",").ljust(20) + "\t"
                task_table += (cycle_division + ",").ljust(20) + "\n"

    return task_table


main()
