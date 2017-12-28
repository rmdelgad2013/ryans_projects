import os
from datetime import datetime
import json
import re
from urllib.parse import urljoin
import requests
import scrapy
from lxml import html


class IndeedSpider(scrapy.Spider):
    name = 'indeed'

    def start_requests(self):

        # Figure out how many jobs there are with an initial request & parse
        initial_url = 'https://www.indeed.com/q-data-scientist-jobs.html'
        response = requests.get(initial_url)
        page = response.content.decode('utf-8')
        jobcnt_pattern = r'Page \d of ((?:\d{1,3}\,?){1,})'
        job_count = int(re.search(jobcnt_pattern, page).group(1).replace(',', ''))

        # Build the URLs to scrape
        ROOT_URL = 'https://www.indeed.com/jobs?q=data+scientist&start={}'
        urls = [ROOT_URL.format(i * 10) for i in range(job_count // 10)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.scrape_job_page)


    def scrape_job_page(self, response):

        # Parse out the job titles, links, and companies
        page = response.body
        tree = html.fromstring(page)
        ROOT_URL = 'https://www.indeed.com/'
        job_links = [urljoin(ROOT_URL, href) for href in tree.xpath('//a[@data-tn-element="jobTitle"]/@href')]
        job_titles = tree.xpath('//a[@data-tn-element="jobTitle"]/@title')
        job_companies = [company for company in tree.xpath('//span[@class="company"]//text()') if company.strip()]

        # Scrape the job listing pages
        for link, title, company in zip(job_links, job_titles, job_companies):
            yield scrapy.Request(url=link, callback=self.save_file,
                                 meta={'title': title,
                                       'company': company})


    def save_file(self, response):

        company = re.sub(r'[^\w]', '', response.meta['company'])
        title = re.sub(r'[^\w]', '', response.meta['title'])

        SCRAPE_DATE = datetime.now()
        scrape_dict = {
            'scrape_date': SCRAPE_DATE.strftime('%Y-%m-%d'),
            'body': response.body.decode('utf-8'),
            'job_url': response.url,
            'company': company,
            'title': title
        }

        SCRAPE_PATH = r'C:\Users\rmdelgad\Documents\repos\ryans_projects\datascientist\data\scraped'


        filename = '{company}_{jobtitle}_{date}.json'.format(company=company, jobtitle=title,
                                                             date=SCRAPE_DATE.strftime('%Y%m%d%H%M%S%f'))

        filepath = os.path.join(SCRAPE_PATH, filename)
        try:
            with open(filepath, 'w') as f:
                json.dump(scrape_dict, f)
        except:
            import pdb; pdb.set_trace()

        print('Saved file {}'.format(filepath))