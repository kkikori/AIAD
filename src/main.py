import sys
from pathlib import Path
import datetime as dt
import simplejson as json

import toKalliopeia
import preparation
import question_generator


def time_setting(f_path):
    if not f_path.is_file():
        print("[file error]", f_path.name, "is not found.")
        sys.exit()

    f = f_path.open("r")
    jsonData = json.load(f)
    t = dt.timedelta(minutes=int(jsonData["interval_time"]))
    return t


def preparate_file_paths():
    # ファイルパスの準備
    fn = Path("file_paths.json")
    if not fn.is_file():
        print("[file error]", fn.name, "is not found.")
        sys.exit()

    f_paths = {}
    f = fn.open("r")
    jsonData = json.load(f)

    for fgroup in jsonData:
        data_root = fgroup.pop("DATA_ROOT")
        root_path = Path(data_root)
        for fn, fp in fgroup.items():
            f_paths[fn] = root_path / fp
    return f_paths


def main(DEBUG):
    # 現在時刻の取得
    if DEBUG:
        t = "2016-12-13 05:46:42"
        now_time = dt.datetime.strptime(t, '%Y-%m-%d %H:%M:%S')
    else:
        # now_time = dt.datetime.now(pytz.utc)
        now_time = dt.datetime.now()
        n_str = now_time.strftime("%Y-%m-%dT%H:%M:%S")
        now_time = dt.datetime.strptime(n_str, "%Y-%m-%dT%H:%M:%S")
    print("now_time", now_time)

    # ファイルパスの準備
    f_paths = preparate_file_paths()

    # アクセストークンの準備,settingからの読み込み
    Kalliopeia= toKalliopeia.preparate_kalliopeia(f_setting=f_paths["SETTING"])

    # データ読み込み
    threadlist, postlist, userlist = preparation.preparate_main(f_paths, Kalliopeia)

    question_generator.q_generator_main(POSTS=postlist, USERS=userlist, f_paths=f_paths, now_time=now_time)


if __name__ == '__main__':
    args = sys.argv
    if len(args) > 1:
        debug = True
    else:
        debug = False
    main(DEBUG=debug)
