import os
import requests
from requests.auth import HTTPBasicAuth

ES_HOST = os.environ.get("ES_SCARLETT_HOST")
ES_USER = os.environ.get("ES_SCARLETT_USER")
ES_PASSWORD = os.environ.get("ES_SCARLETT_PASSWORD")
ES_INDEX = os.environ.get("ES_SCARLETT_INDEX")
URL = ES_HOST + ES_INDEX


def index(_type, event):
    """

    :param type:
    :param event:
    :return:
    """
    INDEX_URL = URL + "/{}/".format(_type)
    res = requests.post(INDEX_URL + event['id'], json=event, auth=HTTPBasicAuth(ES_USER, ES_PASSWORD))
    if not res.ok:
        print event
        print res, res.content
        print '------'
