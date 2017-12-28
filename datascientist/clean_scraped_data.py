import os
import json
import re
from lxml import html
import pandas as pd


def clean_page(page):
    HTML_TAGS_TO_REMOVE = [
        r'<\/?p(?: \w+="[\w.:%&;@#$,\?]+"){0,7}>',
        r'<\/?h\d>',
        r'<\/?b>',
        r'<\/?i>',
        r'<\/?u>',
        r'<\/?ul>',
        r'<\/?li>',
        r'<br ?\/?>',
        r'&nbsp;'
    ]

    regex_pattern = r'(?:{})'.format('|'.join(HTML_TAGS_TO_REMOVE))
    page_cleaned = re.sub(regex_pattern, ' ', page)
    page_cleaned = re.sub(r'[?.!]', '.', page_cleaned)
    page_cleaned = page_cleaned.lower() \
        .replace('\xa0', ' ')\
        .replace(r'</li>', '.')

    return page_cleaned


def parse_descr_from_page(page):
    KEYWORDS = [
        'requirements',
        'description',
        'role',
        'requirements',
        'education',
        'qualifications',
        'job title',
        'what you',
        'who we',
        'position summary',
        'background'
    ]

    contains_predicate = ' or '.join('contains(text(),"{}")'.format(kw) for kw in KEYWORDS)
    descr_xpath = '//div[{pred}]//text()'.format(pred=contains_predicate)

    tree = html.fromstring(page)
    job_descr = ''.join(tree.xpath(descr_xpath))

    return job_descr



def main():
    SCRAPE_DIR = r'C:\Users\rmdelgad\Documents\repos\ryans_projects\datascientist\data\scraped\20171226'
    scrape_files = os.listdir(SCRAPE_DIR)

    for sf in scrape_files:
        print('Processing {}'.format(sf))
        with open(os.path.join(SCRAPE_DIR, sf), 'r') as f:
            scrape_dict = json.load(f)

        page_raw = scrape_dict['body']
        page_cleaned = clean_page(page_raw)
        job_descr = parse_descr_from_page(page_cleaned)

        cleaned_dict = {
            'description': job_descr,
            'company': scrape_dict['company'],
            'title': scrape_dict['title'],
            'url': scrape_dict['job_url']
        }

        CLEANED_DIR = r'C:\Users\rmdelgad\Documents\repos\ryans_projects\datascientist\data\cleaned\20171226'
        with open(os.path.join(CLEANED_DIR, sf), 'w') as f:
            json.dump(cleaned_dict, f)


if __name__ == '__main__':
    main()