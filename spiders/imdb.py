import scrapy


class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv=250']

    def parse(self, response):
        movies = response.css('tbody.lister-list > tr > td.titleColumn')
        for movie in movies:
            title = movie.css('a::text').get()
            href = movie.css('a::attr(href)').get()
            link = 'https://www.imdb.com' + href
            print(title, link)