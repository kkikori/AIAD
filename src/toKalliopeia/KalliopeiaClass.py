import simplejson as json
import requests


class KalliopeiaClass():
    def __init__(self, url):
        self.url = url
        self.f_token = None

    def _send(self, endpoint, type, data=None, token=None):
        uri = self.url + endpoint
        data = json.dumps(data)
        headers = {
            'Content-Type': 'application/json'
        }
        if token:
            headers['Authorization'] = "Bearer " + token
        else:
            headers['Authorization'] = "Bearer " + self.f_token

        if type.lower() == 'get':
            return requests.get(uri, headers=headers).json()
        elif type.lower() == 'post':
            return requests.post(uri, data, headers=headers).json()
        else:
            raise ValueError("type '" + token + "' is not defined.")

    def get_access_token(self, name, password):
        request_data = {
            'name': name,
            'password': password
        }
        response = self._send(endpoint='login', data=request_data, type='post')
        return response['token']

    def load_thread(self, thread_i):
        en_p = "threads/" + str(thread_i)
        return self._send(endpoint=en_p, type="get")

    def load_threads(self):
        return self._send(endpoint="threads", type="get")

    def load_users(self):
        return self._send(endpoint="users", type="get")

    def load_user(self, uname):
        users = self.load_users()
        for user in users:
            if user["name"] == uname:
                en_p = "users" + str(user["id"])
                return self._send(endpoint=en_p, type="get")
        raise ValueError("Kalliopeia's user '" + uname + "' is not defined.")

    def create_post(self, data):
        self._send(endpoint="posts", data=data, type="post")

    def create_user(self, data):
        self._send(endpoint="signup", data=data, type="post")

    def _get_thi_list(self):
        threads = self.load_threads()

        thi_list = []
        for thread in threads:
            thi_list.append(thread["id"])
        return thi_list

    def get_threads_data(self):
        thi_list = self._get_thi_list()
        threads_data=[]
        for th_i in thi_list:
            threads_data.append(self.load_thread(thread_i=th_i))
        return threads_data

    def _get_ui_list(self):
        users = self.load_users()
        ui_list = []
        for user in users:
            ui_list.append(user["id"])
        return ui_list

    def get_users_data(self):
        ui_list = self._get_ui_list()

        users_data = []
        for ui in ui_list:
            users_data.append(self.load_user(ui))
        return users_data

    def read_user_id(self,name):
        users = self.load_users()
        for user in users:
            if user["name"] == name:
                return user["id"]

        raise ValueError("Kalliopeia's user '" + name + "' is not defined.")
