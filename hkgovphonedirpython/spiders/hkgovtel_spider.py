import scrapy
import re

from hkgovphonedirpython.items import Govperson

def hasphonetable(response):
    return len(response.css(".row td")) > 0

class HkTelDirSpider(scrapy.Spider):
    name = "hkgovtel"
    start_urls = ["http://tel.directory.gov.hk/index_ENG.html?accept_disclaimer=yes"]
    
    def parse(self, response):
        departments = response.css("#tbl_dept_list a::text").extract()
        departments = map(lambda x: re.sub('\s+', ' ', x.strip().replace('\n', '').replace('\r', '')), departments)
        for idhref, href in enumerate(response.css("#tbl_dept_list a::attr(href)").extract()):
            url = response.urljoin(href)
            request = scrapy.Request(url, callback=self.parsepage)
            request.meta['topdepartment'] = departments[idhref]
            yield request

    def parsepage(self, response):
        if hasphonetable(response):
            h1rownodes = response.css(".row, h1")
            basedepartment = " - ".join(h1rownodes[0].css("::text").extract())
            topdepartment = response.meta['topdepartment']
            department = basedepartment
            h1rownodes = h1rownodes[1:]
            for h1row in h1rownodes:
                if h1row.extract()[0:4] == "<h1>":                    
                    department = " - ".join([basedepartment, " - ".join(h1row.css("::text").extract()[1:])])
                else:
                    rowdetails = map(lambda td: td.css("::text").extract(), h1row.css("td")) 
                    item = Govperson()
                    item['name'] = rowdetails[0][0]
                    item['title'] = rowdetails[1][0]
                    if rowdetails[2] != []:
                        item['tel'] = rowdetails[2][0]
                    if rowdetails[3] != []:
                        item['email'] = "@".join(re.findall(r"= \'(.*?)\';", rowdetails[3][0]))
                    item['department'] = department
                    item['topdepartment'] = topdepartment
                    yield item
            
        somelinks = response.css("#tbl_dept_list a::attr(href)").extract()
        morelinks = response.css("#dept_list_lv2_outline a::attr(href)").extract()
        links = somelinks + morelinks
        somelinkstext = response.css("#tbl_dept_list a::text").extract()
        morelinkstext = response.css("#dept_list_lv2_outline a::text").extract()
        linkstext = somelinkstext + morelinkstext
        for idlink, link in enumerate(links):
            url = response.urljoin(link)
            request = scrapy.Request(url, callback=self.parsepage)
            request.meta['topdepartment'] = response.meta['topdepartment']
            yield request
