import datetime as dt
import simplejson as json
import csv
import question_generator


# 時間とかの条件を読み込む
def _setting(fn):
    f = fn.open("r")
    jsonData = json.load(f)
    thresholds = {}

    thresholds["t_user"] = dt.timedelta(minutes=int(jsonData["threshold_t_user"]))
    thresholds["c_user"] = int(jsonData["threshold_c_user"])
    #thresholds["t_thread"] = dt.timedelta(minutes=int(jsonData["threshold_t_thread"]))
    #thresholds["c_thread"] = int(jsonData["threshold_c_thread"])

    f_name = jsonData["facilitator"]["name"]
    surpervisors = jsonData["supervisors"]

    # 閾値群,ファシリテータのユーザ名,管理者(問いかけ対象外のユーザ名リスト)
    return thresholds, f_name, surpervisors


# ファイシリテータへの返信だったら、Trueを返す
# スレッドの親投稿だったら、Trueを返す
# それ以外はFalse
def _exception_checker(target_pi, POSTS, f_name):
    target_post = POSTS[target_pi]
    # 親投稿かどうかの判定
    if not target_post.reply_to_id:
        return True

    # ファシリテータへの返信か判定
    reply_to = POSTS[target_post.reply_to_id]
    if reply_to.user == f_name:
        return True
    return False


# 2箇所に発言内容を保存する
def _save_and_call_q(pi, si, q_body, fn_postapi, f_save):
    # save to file
    add_row = [pi, si, q_body]
    with f_save.open("a") as f:
        writer = csv.writer(f, lineterminator='\n')  # 行末は改行
        writer.writerow(add_row)
    f.close()

    # api attack
    save_q = {"body": q_body, "in_reply_to_id": pi}

    fn = str(pi) + ".json"
    f = (fn_postapi / fn).open("w")
    json.dump(save_q, f, indent=2, ensure_ascii=False)
    f.close()

    return


def q_generator_main(POSTS, USERS, f_paths, now_time):
    # 閾値の設定
    thresholds, f_name, supervisors = _setting(f_paths["SETTING"])

    # ユーザごとに問いかけするかどうか判定
    for name_u, user in USERS.items():
        # ファシリテータ,管理者は除く
        if (name_u in supervisors) or name_u == f_name:
            continue

        # ユーザの最新の投稿が対象
        target_pi = user.pi_list[-1]

        # 構造解析器により注釈がつけられていない場合（時刻で判定）
        if (not POSTS[target_pi].created_at < POSTS[target_pi].updated_at):
            if len(user.pi_list) < 2:
                continue
            target_pi = user.pi_list[-2]

        # 問いかけ対象外を弾く
        if _exception_checker(target_pi, POSTS, f_name):
            continue

        target_si, q_body = question_generator.to_individual_q(user=user, post=POSTS[target_pi], now_time=now_time, \
                                                          f_paths=f_paths, thresholds=thresholds)
        if q_body:
            _save_and_call_q(target_pi, target_si, q_body, f_paths["POST_API"], f_paths["INDIVIDUAL_Q"])

    return
