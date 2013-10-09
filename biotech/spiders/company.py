from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from biotech.items import BiotechItem
from scrapy.http import Request
import urlparse
import re

class CompanySpider(CrawlSpider):
    name = 'company'
    allowed_domains = ['crmz.com']
    start_urls = ['http://www.crmz.com/Directory/Industry221.htm']
    #start_urls = ['http://www.crmz.com/Directory/Industry803.htm']


    rules = (
        Rule(SgmlLinkExtractor(allow=()), follow=False),
    )
    def parse_ticker(self,response):
        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        cap = hxs.select("//tr//td[text()='Market Cap:']/following-sibling::td//text()").extract()
        if cap:
            #change the bad \xa0 to space
            cap = cap[0].replace(u'\xa0', u' ').strip()
            # if cap == 0 maybe something goes wrong with the company
            print "Market Cap",cap
        else: 
            cap = None
        item['cap'] = cap
        yield item

    def parse_company(self, response):
        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        #packing phone
        name = item['name']
        phone = hxs.select("//td[text()='%s']/../..//td[@align='LEFT']/text()"%name).extract()
        if phone:
            phone = phone[0]
            phone = phone.lstrip("Phone:").lstrip()
            item['phone'] = phone
        #packing address
        adds=hxs.select("//td[text()='%s']/../..//td[@align='CENTER'][@class='Bold']/text()"%name).extract()
        item["addr0"] = name
        i = 0
        for a in adds:
            i+=1
            a = a.replace(u'\xa0',u' ').strip()
            a = a.encode('ascii', 'ignore')
            item['addr%d'%i] = a

        #packing fax
        fax = hxs.select("//td[text()='Fax Number:']/following-sibling::td/text()").extract()
        if fax:
            item['fax'] = fax[0]

        #packing red remarks
        redTexts = hxs.select("//td[@class='BoldRed']/text()").extract()
        if redTexts:
            item['red']=" ".join(redTexts)

        #packing businessSummary
        businessSummary = hxs.select("//span[text()='Business Summary']/following-sibling::table//td")
        if len(businessSummary) >= 2:
            businessSummary = businessSummary[1].select("text()").extract()
            if businessSummary:
                businessSummary = businessSummary[0].encode('ascii', 'ignore').strip()
                item['businessSummary'] = businessSummary

        item['bnames'] = hxs.select("//span[text()='Business Names']/following-sibling::table//td[@align='LEFT']/text()").extract()

        #packing financial statements
        fs0=hxs.select("//a[text()='Annual Financials']/@href").extract()
        if fs0:
            item['statements0'] = self.extendHref(fs0[0],response)
        fs1=hxs.select("//a[text()='Quarterly Financials']/@href").extract()
        if fs1:
            item['statements1'] = self.extendHref(fs1[0],response)

        #Industry
        indCaptions=hxs.select("//td[text()='Industry']/../following-sibling::tr//td/text()").extract()
        indNames = hxs.select("//td[text()='Industry']/../following-sibling::tr//td//a/text()").extract()
        sicTailIndex = len(indNames)
        if "NAICS" in indCaptions:
            sicTailIndex = indCaptions.index("NAICS") - 1
        item["SIC"] = indNames[:sicTailIndex]
        item["NAICS"] = indNames[sicTailIndex:]

        #leaders
        titleNames=hxs.select("//span[text()='Officers and Directors']/following-sibling::table//td[@align='LEFT']/text()").extract()
        tnTuple=zip(titleNames[0::2],titleNames[1::2])
        item['leaders']=[ ":".join((x,y)) for x,y in tnTuple]

        #packing ratings
        ratingRefs=hxs.select("//td[text()='Financial Ratings:']/..//a/@href").extract() 
        ratings = []
        for href in ratingRefs:
            ratings.append(self.extendHref(href,response))
        item['ratings'] = " ".join(ratings)

        #packing ticker
        tickerhref = hxs.select("//td[text()='Ticker: ']//a/@href").extract()
        if tickerhref:
            tickerhref = tickerhref[0]
            #remove extra thing in href
            tickerhref = tickerhref.replace("javascript:window.location='","")
            tickerhref = tickerhref.strip("'")
            tickerhref = urlparse.urljoin(response.url, tickerhref)
            item['ticker'] = tickerhref
            request = Request(tickerhref,self.parse_ticker)
            request.meta['item'] = item
            yield request
        else:
            #no ticker, no set Market capacity
            #just yield. because these fields already initialized
            yield item
        

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        #i['domain_id'] = hxs.select('//input[@id="sid"]/@value').extract()
        #i['name'] = hxs.select('//div[@id="name"]').extract()
        #i['description'] = hxs.select('//div[@id="description"]').extract()
        ts=hxs.select("//tr[@valign='TOP'][@bgcolor='White']")
        print "start scrapy"
        #count companies
        sels = []
        for t in hxs.select("//a"):
            href = t.select('@href').extract()
            name = t.select('text()').extract()

            if not href:
                continue
            href = href[0]
            #add domain to href
            href = urlparse.urljoin(response.url, href)
            #packing RSS
            if not name:
                #rss is special, it doesn't have text, so have to process here
                if "NewsFeedXML" in href:
                    item['rss'] = href
                continue
            name = name[0]
            if "/ReportPreview" in href:
                if 'item' in locals().keys():
                    request = Request(item['href'],self.parse_company)
                    request.meta['item'] = item
                    yield request
                item = BiotechItem()
                #initialize all Fields with default value ""
                item.initAll()
                id = re.findall('BusinessId=(\d+)',href)
                if not id:
                    continue
                id = id[0]
                #packing company name
                item['name'] = name.strip()
                #packing href
                item['href'] = href.strip()
                item['id'] = id.strip()

                #Number
                numTd=t.select('../preceding-sibling::td/text()')
                if numTd:
                    num=numTd[0].extract()
                    num=num.strip('.')
                    #packing index number
                    item['number'] = num

                #item['status'] = "Active"
                #if t.select("@class").extract():
                #    item['status'] = "Inactive"

            elif "Country" in href:
                #packing country
                item['country'] = name
            elif "State" in href:
                #packing state/province
                item['state'] = name

        #yield the last item
        request = Request(item['href'],self.parse_company)
        request.meta['item'] = item
        yield request

    def extendHref(self,tickerhref,response):
        tickerhref = tickerhref.replace("javascript:window.location='","")
        tickerhref = tickerhref.strip("'")
        tickerhref = urlparse.urljoin(response.url, tickerhref)
        return tickerhref

