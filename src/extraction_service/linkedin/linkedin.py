from rec_service.extraction_service.extraction_service import ExtractionService
import requests
from rec_service.utils.secret.secret_manager import SecretManager
import base64
class LinkedIn(ExtractionService):
    def __init__(self):

        self.access_token = self.get_access_token()

    def get_access_token(self):
        client_id, client_secret = SecretManager().get_linkedin_secrets()

        url = 'https://www.linkedin.com/oauth/v2/accessToken'
        res = requests.post(
            url=url,
            data={
                'grant_type': 'client_credentials',
                'client_id': {client_id},
                'client_secret': {client_secret}

            },
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            verify=False
        )
        print(res.text)
        assert res.status_code == 200

    def extract_text(self,file:str) -> str:
        file = base64.b64decode(file)

        li_profile = file.decode()
        print(li_profile)
        profile_id = li_profile.split('/')[-2]
        return self.get_profile(profile_id=profile_id)

    def get_profile(self, profile_id):
        '''
        Will obtain profile
        :param profile_id:
        :return:
        '''
        headers = {'Authorization': f'Bearer {self.access_token}'}
        url = f'https://api.linkedin.com/v2/people/(id:{profile_id})'
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            return response.text
        else:
            raise ConnectionError(str(response.text))
