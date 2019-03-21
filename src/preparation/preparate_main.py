import csv
import datetime as dt

import preparation


def _time_seikei(time_s):
    year = int(time_s[0:4])
    month = int(time_s[5:7])
    day = int(time_s[8:10])
    hour = int(time_s[11:13])
    minute = int(time_s[14:16])
    second = int(time_s[17:19])
    micro_sec = int(time_s[20:25])

    return dt.datetime(year, month, day, hour, minute, second, micro_sec)


def _has_premise(thread, Post_list):
    # ポストごとにどこから関連を受けているか格納
    for pi in thread.pi_list:
        post = Post_list[pi]
        for list_si, sentence in enumerate(post.sentences):
            if not sentence.related_to:
                continue
            if sentence.related_to in post.si_list:
                relate_si = post.si_list.index(sentence.related_to)
                Post_list[pi].sentences[relate_si].has_premise.append(sentence.id)
            else:
                relate_pi = post.reply_to_id
                relate_si = Post_list[relate_pi].si_list.index(sentence.related_to)
                Post_list[relate_pi].sentences[relate_si].has_claim.append(sentence.id)
        return


def _preparate_users(users):
    # 1回以上投稿しているユーザのリストを返す
    User_list = {}
    for usr in users:
        pi_list = []
        for post in usr["posts"]:
            pi_list.append(post["id"])

        new_user = preparation.UserClass(ui=usr["id"], name=usr["name"], \
                                         display_name=usr["display_name"], role=usr["role"], \
                                         pi_list=pi_list)
        if len(new_user.pi_list) > 0:
            User_list[usr["name"]] = new_user
    return User_list


def _preparate_per_thread(original_th, Post_list):
    pi_list = []
    for o_p in original_th["posts"]:
        sentences = []
        si_list = []

        t_posted = _time_seikei(o_p["updated_at"])
        for sentence in o_p["sentences"]:
            new_s = preparation.SentenceClass(si=sentence["id"], body=sentence["body"],
                                              related_to=sentence["related_to"],
                                              component_type=sentence["component_type"])
            sentences.append(new_s)
            si_list.append(new_s.id)
            t_sen = _time_seikei(sentence["updated_at"])
            if t_posted < t_sen:
                t_posted = t_sen

        new_p = preparation.PostClass(pi=o_p["id"], \
                                      created_at=_time_seikei(o_p["created_at"]), \
                                      updated_at=t_posted, \
                                      body=o_p["body"], \
                                      reply_to_id=o_p["in_reply_to_id"], \
                                      user=o_p["user"]["name"], \
                                      sentences=sentences, \
                                      si_list=si_list, \
                                      belong_th_i=original_th["id"]
                                      )
        pi_list.append(new_p.id)
        Post_list[new_p.id] = new_p
    thread = preparation.ThreadClass(original_th["id"], original_th["title"], pi_list, pi_list[-1])
    _has_premise(thread, Post_list)
    return thread


def _previous_qs(Post_list, User_list, f_individual=None):
    # 過去に問いかけしたデータを読み込む
    if not f_individual.exists():
        print("[FILE ERROR]", f_individual, "is not found.")
        return

    with f_individual.open("r") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            usr_name = Post_list[int(row[0])].user
            User_list[usr_name].previousQ_list.append(int(row[0]))


def preparate_main(fn_paths, Kalliopeia):
    # データをとってくる
    threads = Kalliopeia.get_threads_data()
    users = Kalliopeia.get_users_data()

    # スレッドクラスのリストを用意
    Threads_list = {}
    Post_list = {}
    for thread in threads:
        Threads_list[thread["id"]] = _preparate_per_thread(thread, Post_list)

    # ユーザリストを用意
    User_list = _preparate_users(users)

    # 過去の問いかけリストを用意
    _previous_qs(Post_list=Post_list, User_list=User_list, f_individual=fn_paths["INDIVIDUAL_Q"])

    return Threads_list, Post_list, User_list
