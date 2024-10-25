import base64
from src.extraction_service.extraction_service import ExtractionService
import requests
import re
from bs4 import BeautifulSoup
class WebExtractionService(ExtractionService):
    def __init__(self):
        pass

    def parse_link(self,link):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        # Here the user agent is for Edge browser on windows 10. You can find your browser user agent from the above given link.
        r = requests.get(url=link, verify=False,
                         headers=headers)
        soup = BeautifulSoup(r.content, 'html5lib')
        return soup.find('body').prettify(encoding='utf-8')

    def extract_text(self, file: str) -> str:
        '''

        :param file:
        :return:
        '''
        file = base64.b64decode(file)

        link = file.decode()

        html = self.parse_link(link)
        #print(body_text)
        body_text = self.cleanhtml(html)
        return body_text

    def remove_script_code(self,data):
        '''
        Will remove javascript code
        :param data:
        :return:
        '''
        clean = r'<[ ]*script.*?\/[ ]*script[ ]*>'
        cleaned=  re.sub(clean, '', data, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))
        pattern = r'<[ ]*style.*?\/[ ]*style[ ]*>'  # mach any char zero or more times
        text = re.sub(pattern, '', cleaned, flags=(re.IGNORECASE | re.MULTILINE | re.DOTALL))
        return text
    def cleanhtml(self,raw_html):
        '''
        Will clean
        :param raw_html:
        :return:
        '''
        raw_html = str(raw_html)
        raw_html = raw_html.replace('\n','').replace('\t','').replace('\r','').replace('\n ','')

        raw_html_js = self.remove_script_code(raw_html)
        CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(CLEANR, '', raw_html_js)
        result = re.sub(' +', ' ', cleantext)
        result = str(result).replace('\n','').replace('\t','').replace('\r','').replace('\n ','')
        result = result.replace('\\n ','-')
        result = re.sub('-{2,}', ' ', result)

        return result

