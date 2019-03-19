import simplejson as json


def _post_post(f, toKalliopeia):
    ff = f.open("r")
    jsonData = json.load(ff)
    data = {"body": jsonData["body"],
            "in_reply_to_id": jsonData["in_reply_to_id"]}
    toKalliopeia.create_post(data=data)


def post_qs_main(fn, token):
    # ファイルないの投稿をすべて投稿し、ファイルを空にする
    print("create_post")
    f_lists = list(fn.glob("*.json"))
    for f in f_lists:
        _post_post(f, token)
        f.unlink()
