# -*- coding: utf-8 -*-
import scrapy
import csv


class A58comSpider(scrapy.Spider):
    name = '58com'
    #allowed_domains = ['58.com']
    #start_urls = ['http://58.com/']
    def start_requests(self):
        yield scrapy.Request('http://wh.58.com/',callback=self.parse_chuzu)

    def parse_chuzu(self,response):
        chuzu=response.xpath('//a[@tongji_tag="pc_home_dh_zf"]/@href').extract_first()
        yield scrapy.Request(response.urljoin(chuzu),callback=self.parse)


    def parse(self, response):

        li=response.xpath("//li/div[@class='des']/h2/a/@href").extract()
        for url in li:
            yield scrapy.Request(response.urljoin(url),callback=self.parser_house_info)

        next_page = response.xpath("//a[@class='next']/@href").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page,callback=self.parse)


    def parser_house_info(self,response):
        phone = response.xpath('//span[@class="house-chat-txt"]/text()').extract_first()
        rent_money = response.xpath('//b[@class="f36"]/text()').extract_first()
        rent_type = response.xpath('//span[@class="c_333"]/text()').extract_first()
        base_info = response.xpath('//ul[@class="f14"]/li')
        tmp = {}
        for li in base_info:
            tmp_list = li.xpath('span/text()').extract()
            if len(tmp_list) >= 2 and len(tmp_list[0])>0 and len(tmp_list[1])>0:
                tmp[tmp_list[0]]=tmp_list[1]
        yield {
            "phone":phone,
            "rent_money":rent_money,
            "rent_type":rent_type,
            "base_info":tmp,
        }
