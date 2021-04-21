import requests
from bs4 import BeautifulSoup
from django.utils.text import slugify

from scrapper.models import Movie


class ScrapperIMDB(object):
    def __init__(self):
        self.url = 'https://www.imdb.com/chart/top/'
        self.html = None
        self.data = []

    def get_html(self):
        if not self.html:
            response = requests.get(self.url)
            self.html = response.text
        return self.html

    def parser_html(self):
        self.soup = BeautifulSoup(self.html, 'html.parser')
        list_tr = self.soup.select('.lister-list tr')

        for tr in list_tr:
            item = self.clean_data(tr, 'td', 'class')
            if item:
                self.data.append(item)
        return self.data

    def clean_titlecolumn(self, value):
        if not value:
            return {}
        r = [x.strip() for x in value.split('\n') if x.strip()]
        return {'name': r[1], 'year': int(slugify(r[-1]))}

    def clean_ratingcolumn_imdbrating(self, value):
        if not value:
            return 0
        print(value)
        return float(value.strip())

    def clean_data(self, parent_element, css_selector: str, attr_key: str):
        elements = parent_element.select(css_selector)
        item = {}
        for element in elements:
            key = slugify(element.attrs[attr_key]).replace('-', '_')
            clean_method = getattr(self, 'clean_{}'.format(key), None)
            item[key] = clean_method(element.text) if clean_method else element.text
        return item

    def save_data(self, data):
        for item in data:
            Movie.objects.update_or_create(
                name=item.get('titlecolumn').get('name'),
                defaults={
                    'year': item.get('titlecolumn').get('year'),
                    'rating': item.get('ratingcolumn_imdbrating'),
                })

    def run(self):
        self.get_html()
        data = self.parser_html()
        self.save_data(data)
