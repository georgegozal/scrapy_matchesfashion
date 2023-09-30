import scrapy
import re


class ShoesSpider(scrapy.Spider):
    name = "shoes"
    allowed_domains = ["matchesfashion.com"]
    start_urls = [
        'https://www.matchesfashion.com/womens/shop/shoes?pageOffset=0',
        'https://www.matchesfashion.com/mens/shop/shoes?pageOffset=0']

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'Accept-Language':
        'en-US,en;q=0.5',
        'Referer': 'https://www.matchesfashion.com'
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        if not response.xpath('//h1[contains(text(), "Shoes")]'):
            pass

        shoes_list = response.xpath('//div[@class="css-1kxonj9"]')
        for shoe in shoes_list:
            item_link = shoe.xpath('.//a/@href').extract()[0]

            yield scrapy.Request(
                response.urljoin(item_link),
                headers=self.headers,
                callback=self.parse_details,
                meta={"gender": self.get_gender(response)}
            )

        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            yield scrapy.Request(
                response.urljoin(next_page),
                headers=self.headers,
                callback=self.parse
            )

    def parse_details(self, response):
        yield {
            "title": response.xpath('.//span[@data-testid="ProductMainDescription-name"]/text()').get(),
            "url": response.url,
            # "price_full": 
            # "price_drop":
            "price": response.xpath('.//span[@data-testid="ProductPrice-billing-price"]/text()').get(),
            "image_url": self.fix_picture_url(response),
            "category": self.get_categories(response),
            "gender": response.request.meta.get("gender")
        }

    @staticmethod
    def get_categories(response):
        categories = response.xpath('.//a[@data-testid="ViewAllPills-related-category-link"]')
        category_list = [category.xpath('.//text()').get() for category in categories]
        return list(set(category_list))

    @staticmethod
    def fix_picture_url(response):
        url = response.xpath('.//img[@class="iiz__img "][1]/@src').get()
        fixed_url = f"https:{url}"
        return fixed_url

    @staticmethod
    def get_gender(response):
        gender_dict = {
            "mens": "Male",
            "womens": "Female"
        }
        gender = re.search(r'/(womens|mens)/', response.url).group(1)
        return gender_dict.get(gender)
