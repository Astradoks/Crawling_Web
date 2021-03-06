import scrapy
from typing_crawling.items import TypingCrawlingItem
from scrapy.selector import Selector

class TypingWordsSpider(scrapy.Spider):
    name = 'typing_words'
    allowed_domains = ["1000mostcommonwords.com"]
    start_urls = ['https://1000mostcommonwords.com/']

    def parse(self, response):
        links = response.css('p > a::attr(href)').extract()
        yield scrapy.Request(links[0], callback=self.parse_english_words)
        for link in links:
            yield scrapy.Request(link, callback=self.parse_words)
    
    def parse_words(self, response):
        words = []
        for x in range(2,1002):
            words.append(Selector(response).xpath('..//tbody/tr['+ str(x) +']/td[2]/text()').extract_first())
        item = TypingCrawlingItem()
        item['language'] = Selector(response).xpath('..//tbody/tr[1]/td[2]/strong/text()').extract_first()
        item['words'] = words
        yield item

    def parse_english_words(self, response):
        words = []
        for x in range(2,1002):
            words.append(Selector(response).xpath('..//tbody/tr['+ str(x) +']/td[3]/text()').extract_first())
        item = TypingCrawlingItem()
        item['language'] = 'English'
        item['words'] = words
        yield item