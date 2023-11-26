import scrapy
from bookscrap.items import BookItem
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class GetdirsSpider(scrapy.Spider):
    name = "getDirs"
    allowed_domains = ["goodreads.com"]

    def start_requests(self):
        file = open("/home/darmasrmz/DAAD/data-analysys-apps/h3_scrapy/bookscrap/books_urls.txt", 'r')
        book_urls = file.readlines()
        for url in book_urls:
            yield scrapy.Request(url=url[:-1], callback=self.parse_book)

    def parse_book(self, response):
        title = response.css('h1.Text__title1::text').get()
        authors = response.css('span.ContributorLink__name::text').get()
        self.driver = webdriver.Chrome()
        self.driver.get(response.url)
        try:
            self.driver.find_element(By.XPATH, '//button[@aria-label="Close"]').click()
        except:
            pass
        try:
            self.driver.find_element(By.XPATH, '//button[@aria-label="Book details and editions"]').click()
        except:
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//button[@aria-label="Book details and editions"]').click()
        time.sleep(3)
        try:
            isbn = self.driver.find_element(By.XPATH, '//div[@class="DescListItem"]//dt[text()="ISBN"]//following-sibling::dd/div[@class="TruncatedContent"]/div[@class="TruncatedContent__text TruncatedContent__text--small"]').text.split(' ', 1)[0]
        except:
            isbn = None
        try:
            publisher = self.driver.find_element(By.XPATH, '//div[@class="DescListItem"]//dt[text()="Published"]//following-sibling::dd/div[@class="TruncatedContent"]/div[@class="TruncatedContent__text TruncatedContent__text--small"]').text.split('by ', 1)[1]
        except:
            publisher = None
        try:
            publication_date = self.driver.find_element(By.XPATH, '//div[@class="DescListItem"]//dt[text()="Published"]//following-sibling::dd/div[@class="TruncatedContent"]/div[@class="TruncatedContent__text TruncatedContent__text--small"]').text.split('by', 1)[0]
        except:
            publication_date = None
        sales_rank = None
        try:
            pages = self.driver.find_element(By.XPATH, '//div[@class="DescListItem"]//dt[text()="Format"]//following-sibling::dd/div[@class="TruncatedContent"]/div[@class="TruncatedContent__text TruncatedContent__text--small"]').text.split(' ', 1)[0]
        except:
            pages = None
        try:
            ebook_price = self.driver.find_element(By.XPATH, '//button[@class="Button Button--buy Button--medium Button--block"]').text.split('$', 1)[1]
        except:
            ebook_price = None
        related = self.driver.find_element(By.XPATH, '//ul[@aria-label="Top genres for this book"]').text.replace('\n',' - ').split('...', 1)[0]
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
        self.driver.quit()
