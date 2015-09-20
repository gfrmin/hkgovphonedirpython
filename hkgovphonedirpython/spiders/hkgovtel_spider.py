import scrapy

from hkgovphonedirpython.items import Govperson

def hasphonetable(response):
    print len(response.css(".row td")), "rows"
    return len(response.css(".row td")) > 0

class HkTelDirSpider(scrapy.Spider):
    name = "hkgovtel"
#    allowed_domains = ["http://tel.directory.gov.hk/"]
    start_urls = ["http://tel.directory.gov.hk/index_ENG.html?accept_disclaimer=yes"]
    
    def parse(self, response):
        for href in response.css("#tbl_dept_list a::attr(href)").extract():
            url = response.urljoin(href)
            yield scrapy.Request(url, callback=self.parsepage)

    def parsepage(self, response):
        if hasphonetable(response):
            h1rowtdnodes = response.css(".row td, h1").extract()
            phonetablec = []
            department = ""
            for node in h1rowtdnodes:
                if node[0:4] == "<h1>":
                    for idx, val in enumerate(phonetablec):
                        if idx % 4 == 0:
                            try:
                                item = Govperson()
                                item['name'] = tobepassed[0]
                                item['title'] = tobepassed[1]
                                item['tel'] = tobepassed[2]
                                item['email'] = tobepassed[3]
                                item['department'] = department
                                print "item: ", item
                                yield item
                            except NameError:
                                pass
                            tobepassed = [val]
                        else:
                            tobepassed += [val]
                    department = node
                    phonetablec = []
                else:
                    phonetablec = phonetablec + [node]
                    
            for idx, val in enumerate(phonetablec):
                if idx % 4 == 0:
                    try:
                        item = Govperson()
                        item['name'] = tobepassed[0]
                        item['title'] = tobepassed[1]
                        item['tel'] = tobepassed[2]
                        item['email'] = tobepassed[3]
                        item['department'] = department
                        print "item: ", item
                        yield item
                    except NameError:
                        pass
                    tobepassed = [val]
                else:
                    tobepassed += [val]

            try:
                item = Govperson()
                item['name'] = tobepassed[0]
                item['title'] = tobepassed[1]
                item['tel'] = tobepassed[2]
                item['email'] = tobepassed[3]
                item['department'] = department
                print "item: ", item
                yield item
            except NameError:
                pass
            
        somelinks = response.css("#tbl_dept_list a::attr(href)").extract()
        morelinks = response.css("#dept_list_lv2_outline a::attr(href)").extract()
        links = somelinks + morelinks
        for link in links:
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parsepage)
