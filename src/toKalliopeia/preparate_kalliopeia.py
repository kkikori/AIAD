import simplejson as json
from .KalliopeiaClass import KalliopeiaClass

def preparate_kalliopeia(f_setting):
    f = f_setting.open("r")
    jsonData = json.load(f)
    toKalliopeia = KalliopeiaClass(jsonData["kalliopeia_url"])

    facilitator = jsonData["facilitator"]
    f_token = toKalliopeia.get_access_token(name=facilitator["name"],password=facilitator["password"])
    toKalliopeia.f_token = f_token

    return toKalliopeia