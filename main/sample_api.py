
import requests


G_URL = "https://www.facebook.com"
#G_URL = "https://www.baidu.com"

class API(object):
    
    def __init__(self,url):
        self.url = url

    def status(self):
        """
         possible return values
         200
         302
         500
        """
        try:
            resp = requests.get(self.url)
            return resp.status_code
        except:
            return "Error"


class ProductionClass(object):

    def __init__(self):
        pass

    # CASE 1, Very  simple function doing nothing.
    def method(self, key):
        temp = {'1':1,'2':2,'3':3}
        return temp[key]

    #CASE 2 : Simple API Call ( GET/POST), Tested with/without mocking method
    def get_url_status_message(self):

        api_status = API(G_URL).status()
        #other_attr = API(G_URL).other_attr
        if api_status == 200:
            return "ok"
        elif api_status == 302:
            return "redirection"
        elif api_status == 500:
            return "Error"
        elif api_status == "Error":
            return "Network"
        else:
            return "UNKNOWN"


    # CASE 3 : Mocking the entire response object
    def get_status_obj_from_requests(self, call_type):

        if call_type == "GET":
            get_resp = requests.get(G_URL)
            return get_resp.status_code

        elif call_type == "POST":
            post_resp = requests.post(G_URL)
            return post_resp.status_code

        else:
            return 404

    # CASE 4 : Side Effect, Mocking exception
    def get_status_obj_from_requests_side_effect(self, call_type):

        if call_type == "GET":
            try:
                get_resp = requests.get(G_URL)
                return get_resp.status_code
            except:
                return 404


        elif call_type == "POST":
            try:
                post_resp = requests.post(G_URL)
                return post_resp.status_code
            except:
                return 404

        else:
            return 404


# U=API(G_URL)
# print(U.status())











