import base64
import datetime
from urllib.parse import urlencode
import requests

class SpotifyAPI:
    TOKEN_URL = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.access_token_expires = datetime.datetime.now()
        self.access_token_did_expire = True

    def get_client_credentials(self):
        if not all([self.client_id, self.client_secret]):
            raise ValueError("You must set client_id and client_secret")
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode()).decode()
        return client_creds_b64

    def get_token_headers(self):
        return {"Authorization": f"Basic {self.get_client_credentials()}"}

    def get_token_data(self):
        return {"grant_type": "client_credentials"}

    def perform_auth(self):
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        response = requests.post(self.TOKEN_URL, data=token_data, headers=token_headers)

        if response.status_code not in range(200, 299):
            raise ValueError("Could not authenticate client.")
        
        data = response.json()
        access_token = data.get('access_token')
        expires_in = data.get('expires_in', 0)
        expires = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)

        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < datetime.datetime.now()
        return True

    def get_access_token(self):
        if self.access_token_did_expire or self.access_token is None:
            self.perform_auth()
        return self.access_token

    def get_resource_header(self):
        return {"Authorization": f"Bearer {self.get_access_token()}"}

    def get_resource(self, resource_type, lookup_id):
        endpoint = f"https://api.spotify.com/v1/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        return self._make_request(endpoint, headers)

    def base_search(self, query_params):
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}&limit=40"
        return self._make_request(lookup_url, headers)

    def _make_request(self, url, headers):
        response = requests.get(url, headers=headers)
        return response.json() if response.status_code in range(200, 299) else {}

    def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
        if query is None:
            raise ValueError("A query is required")
        
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k, v in query.items()])
        
        if operator and operator_query and operator.lower() in ["or", "not"]:
            operator = operator.upper()
            if isinstance(operator_query, str):
                query = f"{query} {operator} {operator_query}"
        
        query_params = urlencode({"q": query, "type": search_type.lower()})
        return self.base_search(query_params)

