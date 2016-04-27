import scrapy
from imdb.items import ImdbItem
import logging

def remove_html(string):
    '''removes html tags to some extend from string.
    for example: <p><p>Hello</p></p> would not be cleaned
    completely'''
    import re
    try:
        return re.sub("<[^<]+?>", "", string).replace("\n", "")
    except TypeError:
        logging.info("remove_html: could not parse %s" %string)

class imdb_spider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ['http://www.imdb.com/s']
    start_urls = [
            "http://www.imdb.com/search/title?sort=boxoffice_gross_us&start=41351",
    ]
    def parse(self, response):
        for movie in response.css('tr.detailed'):
            p = movie.xpath
            item = ImdbItem()
            link = p('td[@class="image"]').xpath('a')
            item['uri'] = link.xpath('@href').extract_first()
            item['name'] = link.xpath('@title').extract_first()
            item['gross'] = p('td[@class="sort_col"]/text()').extract_first()
            title = p('td[@class="title"]')
            item['rating'] = title.xpath('div/div/@title').extract_first()
            item['desc'] = title.xpath('span[3]/text()').extract_first()
            item['duration'] = title.xpath('span[7]/text()').extract_first()
            credit = title.xpath('span[4]').extract_first()
            item['credit'] = remove_html(credit)
            item['genre'] = remove_html(title.xpath('span[5]').extract_first())
            yield item

        next_path = '//div[@class="leftright"]/div[2]/span/a[contains(text(), "Next")]/@href'
        next_page = response.xpath(next_path)
        if next_page:
            url = response.urljoin(next_page.extract()[0])
            logging.info("Going for %s" %url)
            yield scrapy.Request(url, self.parse, dont_filter=True)
