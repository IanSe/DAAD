import scrapy
from bookscrap.items import BookItem
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class GetdirsSpider(scrapy.Spider):
    name = "getDirs"
    allowed_domains = ["goodreads.com"]
    list = '/list/best_of_year/2019?id=131403.Best_Books_of_2019'
    bUrl = "https://www.goodreads.com"
    cUrl = bUrl + list
    start_urls = [cUrl]

    def getBooks(self, response):
        title = response.css('h1.Text__title1::text').get()
        authors = response.css('span.ContributorLink__name::text').get()
        driver = webdriver.Chrome()
        driver.get(response.url)
        try:
            driver.find_element(By.XPATH, '//button[@aria-label="Close"]').click()
        except:
            pass 
        try:
            driver.find_element(By.XPATH, '//button[@aria-label="Book details and editions"]').click()
        except:
            time.sleep(1)
            driver.find_element(By.XPATH, '//button[@aria-label="Book details and editions"]').click()
        time.sleep(3)
        try:
            isbn = driver.find_element(By.XPATH, '//div[@class="DescListItem"]//dt[text()="ISBN"]//following-sibling::dd/div[@class="TruncatedContent"]/div[@class="TruncatedContent__text TruncatedContent__text--small"]').text.split(' ', 1)[0]
        except:
            isbn = None
        try:
            publisher = driver.find_element(By.XPATH, '//div[@class="DescListItem"]//dt[text()="Published"]//following-sibling::dd/div[@class="TruncatedContent"]/div[@class="TruncatedContent__text TruncatedContent__text--small"]').text.split('by ', 1)[1]
        except:
            publisher = None
        try:
            publication_date = driver.find_element(By.XPATH, '//div[@class="DescListItem"]//dt[text()="Published"]//following-sibling::dd/div[@class="TruncatedContent"]/div[@class="TruncatedContent__text TruncatedContent__text--small"]').text.split('by', 1)[0]
        except:
            publication_date = None
        sales_rank = None
        try:
            pages = driver.find_element(By.XPATH, '//div[@class="DescListItem"]//dt[text()="Format"]//following-sibling::dd/div[@class="TruncatedContent"]/div[@class="TruncatedContent__text TruncatedContent__text--small"]').text.split(' ', 1)[0]
        except:
            pages = None
        try:
            ebook_price = driver.find_element(By.XPATH, '//button[@class="Button Button--buy Button--medium Button--block"]').text.split('$', 1)[1]
        except:
            ebook_price = None
        related = driver.find_element(By.XPATH, '//ul[@aria-label="Top genres for this book"]').text.replace('\n',' - ').split('...', 1)[0]
        book_item = BookItem()
        book_item['isbn'] = isbn
        book_item['title'] = title
        book_item['authors'] = authors
        book_item['publisher'] = publisher
        book_item['publication_date'] = publication_date
        book_item['sales_rank'] = sales_rank
        book_item['pages'] = pages
        book_item['ebook_price'] = ebook_price
        book_item['related'] = related
        yield book_item
        driver.quit()

    def parse(self, response):
        books = response.xpath('//tr[@itemscope]')
        urls = [None] * 10
        count = 0
        for book in books:
            if(count < 10):
                urls[count] =  book.css('a.bookTitle').attrib['href']
                count += 1
        bUrl = "https://www.goodreads.com"
        for url in urls:
            yield scrapy.Request(url=bUrl+url, callback=self.getBooks)
