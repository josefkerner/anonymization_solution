from linkedin_scraper import Person, actions,Job
from selenium import webdriver
import base64
from datetime import datetime
from rec_service.extraction_service.extraction_service import ExtractionService
from rec_service.utils.connectors.cacheManager import CacheManager
import re
class LinkinScraper(ExtractionService):

    def __init__(self):
        self.email = "kerner.jo@gmail.com"
        self.password = "JosefKerner51"
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        #options.add_argument('--remote-debugging-port=9222')
        self.driver = webdriver.Chrome(options=options)
        actions.login( driver=self.driver,email=self.email, password=self.password)
        self.cache_manager = CacheManager()

    def get_duration(self, from_date, to_date):
        '''
        Will return duration in years and months
        if to_date is "Present" will return duration till now
        :param from_date: string of month and year
        :param to_date: string of month and year or "Present"
        :return:
        '''
        from_date_dt = datetime.strptime(from_date, '%b %Y')
        if to_date == "Present":
            to_date_dt = datetime.now()
        else:
            to_date_dt = datetime.strptime(to_date, '%b %Y')
        duration = to_date_dt - from_date_dt
        duration_years_month = f"{duration.days // 365} years, {duration.days % 365 // 30} months"
        return duration_years_month

    def parse_profile(self, li_profile:str):
        exp_strings = []
        person = Person(li_profile, driver=self.driver, scrape=True)
        for exp in person.experiences:
            exp_string = f"""
                    title: {exp.position_title},
                    duration: {self.get_duration(from_date=exp.from_date, to_date=exp.to_date)},
                    company: {exp.institution_name},
                    description: {exp.description},
                    """
            exp_strings.append(exp_string)

        exp_strings = ';'.join(exp_strings)

        print(person.educations)
        ed_strings = []
        for ed in person.educations:
            ed_string = f"""
                    degree: {ed.degree},
                    duration: f"{ed.from_date} - {ed.to_date}",
                    school: {ed.institution_name},
                    description: {ed.description},
                    """
            ed_strings.append(ed_string)
        ed_strings = ';'.join(ed_strings)

        cv = f"""
                name: {person.name},
                experiences: {exp_strings},
                educations: {ed_strings},
                """
        result = cv.replace('\\n ', '')
        result = re.sub(' {2,}', ' ', result)
        return result

    def parse_job(self, link: str) -> str:
        job = Job(link, driver=self.driver, scrape=True)
        job_text = f"""
                company: {job.company},
                title: {job.job_title},
                location: {job.location},
                description: {job.job_description},
                
        """
        return job_text


    def extract_text(self,file:str):
        '''

        :param file: base64 encoded url
        :return:
        '''
        file = base64.b64decode(file)
        link = file.decode()

        text = self.cache_manager.get_linkedin_content_from_cache(link=link,
                                                           filter_date=True)
        if text is not None:
            return text

        if 'jobs' in link:
            text = self.parse_job(link)
        else:
            text = self.parse_profile(link)

        return text



