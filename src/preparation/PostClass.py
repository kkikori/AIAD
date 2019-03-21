# 投稿のクラス
class PostClass():
    def __init__(self, pi, created_at, body, reply_to_id, user, belong_th_i, updated_at=None, sentences=None,
                 si_list=None):
        self.id = pi
        self.created_at = created_at

        self.updated_at = updated_at

        self.body = body
        if not reply_to_id["Valid"]:
            self.reply_to_id = None
        else:
            self.reply_to_id = reply_to_id["Int64"]
        self.user = user
        if not sentences:
            self.sentences = []
        else:
            self.sentences = sentences
        if not si_list:
            self.si_list = []
        else:
            self.si_list = si_list

        self.belong_th_i = belong_th_i
