import scrapy


class ShoesSpider(scrapy.Spider):
    name = "shoes"
    allowed_domains = ["matchesfashion.com"]
    start_urls = [
        'https://www.matchesfashion.com/womens/shop/shoes?pageOffset={}',
        'https://www.matchesfashion.com/mens/shop/shoes?pageOffset={}']

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept-Language':
        'en-US,en;q=0.5',
        'Referer': 'https://www.matchesfashion.com'
    }
    page = 0

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url.format(0), headers=self.headers, callback=self.parse)

    def parse(self, response):
        shoes_list = response.xpath('//div[@class="css-1kxonj9"]')
        for shoe in shoes_list:
            item_link = shoe.xpath('.//a/@href').extract()[0]

            yield scrapy.Request(
                response.urljoin(item_link),
                headers=self.headers,
                callback=self.parse_details
            )


    def parse_details(self, response):
        yield {
            "title": response.xpath('.//span[@data-testid="ProductMainDescription-name"]/text()').get(),
            "url": response.url,
            # "price_full": 
            # "price_drop":
            "img_url": response.xpath('.//img[@class="iiz__img "][1]/@src').get(),
            "category": response.xpath('.//a[@data-testid="ViewAllPills-related-category-link"]').extract(),
        }

