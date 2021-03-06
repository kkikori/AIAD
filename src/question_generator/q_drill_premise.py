import re
import sys
import random
import simplejson as json

r_question = r"\?$|？$"


def _read_templates(fn):
    if not fn.is_file():
        print("[file error]", fn, "is not found.")
        sys.exit()
    f = fn.open("r")
    jsonData = json.load(f)
    f.close()

    return jsonData


def _make_rmsg(sbody, templates):
    r_msg = ""
    r_msg += random.choice(templates["cushions"])
    r_msg += random.choice(templates["templates"])
    r_msg += "\n"
    return r_msg.replace("<s>", sbody)


# 閾値的に決めている部分
def _check_thresholder(s, threshold):
    if re.search(r_question, s.body):
        print("No.", s.id, "sentence", " is judged to be question sentence.")
        return False

    word_num = len((s.body).split())
    if word_num < threshold["word_underline"]:
        print("No.", s.id, "sentence", " is too short!")
        return False
    if len(s.has_premise) > threshold["has_premise_overline"]:
        print("No.", s.id, "sentence", "has enough premise already.")
        return False
    return True


def _bond_last_word(post, si):
    before_s = post.sentences[si - 1]
    if before_s.body[-1] == ",":
        return True
    return False


def _check_bond(post, target_si):
    bond_si_list = []

    before_si = target_si
    while before_si > 0:
        if _bond_last_word(post, before_si):
            bond_si_list.append(before_si - 1)
        else:
            break
        before_si -= 1

    bond_si_list.append(target_si)

    s_num = len(post.sentences)
    after_si = target_si + 1
    while after_si < s_num:
        if _bond_last_word(post, after_si):
            bond_si_list.append(after_si)
        else:
            break
        after_si += 1
    return sorted(list(set(bond_si_list)))


def drill_premise_q(post, si, s, f_temp):
    temps = _read_templates(f_temp)

    target_s = _check_thresholder(s, temps["threshold"])
    if not target_s:
        return False

    si_list = _check_bond(post, si)

    sbody = ""
    for si in si_list:
        sbody += post.sentences[si].body

    return _make_rmsg(sbody, temps)
