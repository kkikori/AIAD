import question_generator


def _judge_user_term(post, usr, now_time, thresholds):
    if (now_time - post.created_at) < thresholds["t_user"]:
        return False

    # 今まで一度も問いかけしていなかったら
    if len(usr.previousQ_list) == 0:
        return True

    # 最後に質問した投稿のid
    pq_i = usr.previousQ_list[-1]
    pq_idx = usr.pi_list.index(pq_i)

    if len(usr.pi_list) - 1 - pq_idx > thresholds["c_user"]:
        return True
    return False


def to_individual_q(user, post, now_time, f_paths, thresholds):
    # print("*" * 100)
    q_target = _judge_user_term(post=post, usr=user, now_time=now_time, thresholds=thresholds)
    if not q_target:
        print(user.name, " has much question by facilitator.")
        return False, False

    for si, s in enumerate(post.sentences):
        # print(s.body)
        if s.component_type != "CLAIM":
            continue

        q = question_generator.drill_premise_q(post, si, s, f_paths["DRILL_PREMISE"])
        # print("q", q)
        if q:
            print("  ********* Let's reply to", user.name, "!!    **************")
            print(q)
            return si, q

    return False, False
