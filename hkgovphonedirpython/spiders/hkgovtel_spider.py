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
        departments = response.css("#tbl_dept_list a::text").extract()
        for idhref, href in enumerate(response.css("#tbl_dept_list a::attr(href)").extract()):
            url = response.urljoin(href)
            request = scrapy.Request(url, callback=self.parsepage)
            request.meta['topdepartment'] = departments[idhref]
            yield request

    def parsepage(self, response):
        if hasphonetable(response):
            h1rowtdnodes = response.css(".row td, h1").extract()
            basedepartment = h1rowtdnodes[0]
            topdepartment = response.meta['topdepartment']
            department = basedepartment
            h1rowtdnodes = h1rowtdnodes[1:]
            phonetablec = []
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
                                item['topdepartment'] = topdepartment
                                print "item: ", item
                                yield item
                            except NameError:
                                pass
                            tobepassed = [val]
                        else:
                            tobepassed += [val]
                    department = basedepartment + "<br>" + node
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
                        item['topdepartment'] = topdepartment
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
                item['topdepartment'] = topdepartment
                print "item: ", item
                yield item
            except NameError:
                pass
            
        somelinks = response.css("#tbl_dept_list a::attr(href)").extract()
        morelinks = response.css("#dept_list_lv2_outline a::attr(href)").extract()
        links = somelinks + morelinks
        somelinkstext = response.css("#tbl_dept_list a::text").extract()
        morelinkstext = response.css("#dept_list_lv2_outline a::text").extract()
        linkstext = somelinkstext + morelinkstext
        for idlink, link in enumerate(links):
            url = response.urljoin(link)
            yield scrapy.Request(url, callback=self.parsepage)
