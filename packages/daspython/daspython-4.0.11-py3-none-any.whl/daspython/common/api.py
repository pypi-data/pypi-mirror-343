import json
import requests
from datetime import datetime
from abc import ABC
from daspython.common.response import HasItems, HasTotal


class Response(HasTotal, HasItems):
    pass


class Token():
    r'''Base class to keep the user's Token and some shared info like: base url.'''

    api_url_base = ''
    api_token = ''
    headers = {'Content-Type': 'application/json'}
    username = ''
    password = ''
    check_https = True


class ApiMethods(ABC):
    '''Abstract class with shared REST methods like: GET, POST, PUT and DELETE.'''

    token: Token = None
    api_url: str = None

    def __init__(self, token: Token):
        '''
        Parameters
        -----------        
        token: Token
            An instace of DasAuth class after you are authenticated.\n\r
            Example:\n\r
            auth = DasAuth('DAS url', 'Your user name', 'Your password')\n\r
            auth.authenticate()
        '''
        if (token is None or token.api_token is None):
            raise ValueError(
                'Invalid credentials. Please check your username and password.')

        self.token = token

    def download_file(self, url) -> bool:
        api_url = f'{self.token.api_url_base}{url}'
        # Timeout set to 10 minutes
        response = requests.get(
            url=api_url, headers=self.token.headers, verify=self.token.check_https, timeout=60 * 10)

        if (response.status_code != 200):
            return False
        else:
            now = datetime.now()
            open(
                f"digital-objects-{now.strftime('%d-%m-%Y_%H-%M-%S')}.zip", "wb").write(response.content)
            return True

    def get_data(self, url, request):
        '''
        Represents the GET method.

        Parameters
        -----------
        url : str
            Given endpoint that accepts a GET method.
        request: any
            Request object with the parameters that will be converted to a query string.        
        '''

        api_url = f'{self.token.api_url_base}{url}'

        if request != None:
            req_dict = None
            if (isinstance(request, dict)):
                req_dict = request
            else:
                req_dict = request.__dict__

            for x in req_dict:
                if req_dict[x] != None:
                    api_url += f'&{x}={req_dict[x]}'

        response = requests.get(
            url=api_url, headers=self.token.headers, verify=self.token.check_https)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return self._get_error_message(response=response)

    def get_file(self, url, request, file_path):
        api_url = f'{self.token.api_url_base}{url}'

        if request != None:
            req_dict = None
            if (isinstance(request, dict)):
                req_dict = request
            else:
                req_dict = request.__dict__

            for x in req_dict:
                if req_dict[x] != None:
                    api_url += f'&{x}={req_dict[x]}'

        response = requests.get(
            url=api_url, headers=self.token.headers, verify=self.token.check_https)

        with open(file_path, 'wb') as file:
            file.write(response.content)

        return response.content

    def post_json_data(self, url, json_data):

        api_url = f'{self.token.api_url_base}{url}'

        response = requests.post(
            api_url, headers=self.token.headers, data=json_data, verify=self.token.check_https)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return self._get_error_message(response=response)

    def post_data(self, url, body):
        '''
        Represents the POST method.

        Parameters
        a
        url : str
            Given endpoint that accepts a POST method.
        body: any
            Request object with the parameters that will be converted to the body's post.        
        '''
        api_url = f'{self.token.api_url_base}{url}'
        data = None

        if (isinstance(body, dict)):
            data = json.dumps(body)
        else:
            data = json.dumps(body.__dict__)

        response = requests.post(
            api_url, headers=self.token.headers, data=data, verify=self.token.check_https)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return self._get_error_message(response=response)

    def post_grahpql_data(self, json_data):

        api_url = f'{self.token.api_url_base}/graphql'

        response = requests.post(
            api_url, headers=self.token.headers, json=json_data, verify=self.token.check_https)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return self._get_error_message(response=response)

    def put_data(self, url, body):
        '''
        Represents the PUT method.

        Parameters
        -----------
        url : str
            Given endpoint that accepts a PUT method.
        body: any
            Request object with the parameters that will be converted to the body's post.        
        '''
        api_url = f'{self.token.api_url_base}{url}'
        data = json.dumps(body.__dict__)
        response = requests.put(
            api_url, headers=self.token.headers, data=data, verify=self.token.check_https)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return self._get_error_message(response=response)

    def delete_data(self, url):
        '''
        Represents the DELETE method.

        Parameters
        -----------
        url : str
            Given endpoint that accepts a PUT method.
        body: any
            Request object with the parameters that will be converted to the body's post.        
        '''
        api_url = f'{self.token.api_url_base}{url}'
        response = requests.delete(
            url=api_url, headers=self.token.headers, verify=self.token.check_https)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return self._get_error_message(response=response)

    def _get_entries_response(self, response: any) -> Response:
        if (response == None):
            return None

        if (response.get('result') == None):
            return None

        result = Response()

        result.total = response['result'].get('totalCount', 0)

        if (result.total == 0):
            return None

        if (response['result'].get('items')[0].get('entries') != None):
            result.items = response['result'].get('items')[0].get('entries')
            return result

        if (response['result'].get('items')[0].get('entry') != None):
            result.items = list(
                map(lambda item: item['entry'], response['result'].get('items')))
            return result

        result.items = response['result'].get('items')
        return result

    def _get_error_message(self, response: any) -> str:
        if (response == None):
            return None

        if (not response is None and not response.content is None):
            return json.loads(response.content.decode('utf-8'))

        return None

