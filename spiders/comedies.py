from scrapy import Request, Spider

class ComediesSpider(Spider):
    """
    a) el puesto
    b) el título
    c) el director
    d) los actores
    e) el número de reseñas de usuarios y de críticos
    """
    name = 'comedies'
    allowed_domains = ['www.imdb.com']
    initial_url = 'https://www.imdb.com'
    start_urls = [initial_url + '/search/title/?genres=comedy']
    
    def __init__(self):
        self.counter = 0

    def parse(self, response):
        movies = response.css('.lister-list > .lister-item > .lister-item-content')
        for movie in movies:
            index = movie.css('.lister-item-index::text').get()
            title = movie.css('.lister-item-header > a::text').get()
            p = movie.xpath('p[3]')
            p = p.css('::text').extract()
            directors = []
            are_directors = True
            actors = []
            for x in p:
                x = x.strip()
                if (are_directors):
                    if (x == 'Directors:' or x == ',' or x == 'Director:' or x == '|' or x == ''):
                        pass
                    elif (x == 'Stars:'):
                        are_directors = False
                    else:
                        directors.append(x)
                else:
                    if (x == ',' or x == ''):
                        pass
                    else:
                        actors.append(x)
            href = movie.css('.lister-item-header > a::attr(href)').get()
            link = self.initial_url + href
            movie = {
                "index": index,
                "title": title,
                "directors": directors,
                "actors": actors,
                "link": link
            }
            yield response.follow(link, cb_kwargs={'movie': movie}, callback=self.parse_movie)
            
        new_page_url = self.initial_url + response.css('.next-page::attr(href)').get()
        if new_page_url and self.counter < 2:
            self.counter += 1
            yield response.follow(new_page_url, callback=self.parse)
            
    def parse_movie(self, response, movie):
        movieInfo = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]')
        movieStars = movieInfo.css('span::text').extract()
        movie['stars'] = movieStars[0]
        yield movie
        