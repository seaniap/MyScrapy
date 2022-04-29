import scrapy

class WorldmeterSpider(scrapy.Spider):
    name = 'worldmeter'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['http://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        #title = response.xpath('//h1/text()').get()
        countries = response.xpath('//td/a')

        for country in countries:
            country_name = country.xpath(".//text()").get()
            link = country.xpath(".//@href").get()
            # absolute_url
            # absolute_url = f'http://www.worldometers.info/{link}'
            # absolute_url = response.urljoin(link)

            #yield scrapy.Request(url=absolute_url)

            # reletive_url
            yield response.follow(url=link, callback=self.parse_country, meta={'country':country_name})

        # title //h1
        # response.xpath('//h1/text()').get()
        # response.xpath('//td/a/text()').getall()
        # /world-population/china-population/

        #(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr

    def parse_country(self, response):
        # response.xpath('(//table[@class="table table-striped table-bordered table-hover table-condensed table-list"])[1]/tbody/tr')
        country = response.request.meta['country']
        rows = response.xpath('(//table[contains(@class,"table")])[1]/tbody/tr')
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()

            yield {
                'country':country,
                'year':year,
                'population':population
            }


