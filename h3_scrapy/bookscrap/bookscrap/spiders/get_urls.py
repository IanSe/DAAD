import scrapy

class get_url(scrapy.Spider):
    name = "geturl"
    allowed_domains = ["goodreads.com"]

    def start_requests(self):
        urls = [
            '/list/best_of_year/2013"?id=27345.Best_Books_Published_in_2013',
            '/list/best_of_year/2014"?id=47649.Best_Books_of_2014',
            '/list/best_of_year/2015"?id=86673.Best_Books_of_2015',
            '/list/best_of_year/2016"?id=95160.Best_Books_of_2016',
            '/list/best_of_year/2017"?id=107026.Best_Books_of_2017',
            '/list/best_of_year/2018?id=119307.Best_Books_of_2018',
            '/list/best_of_year/2019?id=131403.Best_Books_of_2019',
            '/list/best_of_year/2020?id=143444.Best_Books_of_2020',
            '/list/best_of_year/2021?id=157516.Best_Books_of_2021',
            '/list/best_of_year/2022?id=171064.Best_Books_of_2022',
            '/list/best_of_year/2023?id=183940.Best_Books_of_2023'
        ]
        base_url = "https://www.goodreads.com"
        for url in urls:
            yield scrapy.Request(url=f'{base_url}{url}', callback=self.parse)

    def parse(self, response):
        books = response.xpath('//tr[@itemscope]')
        urls = [None] * 10
        count = 0
        for book in books:
            if(count < 10):
                urls[count] =  book.css('a.bookTitle').attrib['href']
                count += 1

        file = open("./books_urls.txt", 'a')
        bUrl = "https://www.goodreads.com"
        for url in urls:
            file.write(f"{bUrl}{url}\n")