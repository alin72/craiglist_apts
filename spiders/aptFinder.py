
import scrapy
from craiglist_apts.items import CraiglistAptsItem
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class AptfinderSpider(scrapy.Spider):
	name = "craig"
	allowed_domains = ["craiglist.org"]
	base_url = "http://newyork.craigslist.org/search/que/abo?"
	start_urls = (
		'http://newyork.craigslist.org/search/que/abo?max_price=1200',
	)

	def parse(self, response):
		postings = response.xpath(".//p[contains(@data-repost-of,'')]")
		listOfLocations = (postings.xpath("//span[@class='pnr']/*/text()").extract())
		for i in range (0,len(postings)-1):
			item = CraiglistAptsItem()
			item["craigID"]=postings[i].xpath("@data-pid").extract()
			
			temp = postings[i].xpath("span[@class='txt']")
			temp2 = temp.xpath("span[@class='l2']")

			info = temp.xpath("span[@class='pl']")

			item["title"]= info.xpath("a/span[@id='titletextonly']/text()").extract()
			item["date"] = info.xpath("time/@title").extract()
			item["link"] = info.xpath("a/@href").extract()

			item["link"]=["http://newyork.craigslist.org"+i for i in item["link"]]
			item["price"] = temp2.xpath("span[@class='price']/text()").extract()
			item["area"] = temp2.xpath("span[@class='pnr']/small/text()").extract()
			
			if not ("ridgewood" and "astoria" and "brooklyn") in [posts.lower() for posts in listOfLocations]:
				yield item
		