import configuration
import requests
import data

def post_new_user(body):
    return requests.post(configuration.URL_SERVICE + configuration.CREATE_USER_PATH,
                         json=body,
                         headers=data.headers)

def post_new_kit(body,headers):
    return requests.post(configuration.URL_SERVICE + configuration.KITS_PATH,
                         json=body,
                         headers=headers,
                         )
