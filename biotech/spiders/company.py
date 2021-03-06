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
    #Mobile Homes
    start_urls = ['http://www.crmz.com/Directory/Industry221.htm']
    #Biotechnology companies
    #Biotechnology scraping will take a long time, because there are 2508 company information
    #so use Mobile Homes for demo
    #start_urls = ['http://www.crmz.com/Directory/Industry803.htm']

    rules = (
        Rule(SgmlLinkExtractor(allow=()), follow=False),
    )
    
    #parse stock page
    def parse_ticker(self,response):
        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        cap = hxs.select("//tr//td[text()='Market Cap:']/following-sibling::td//text()").extract()
        if cap:
            #change the bad \xa0 to space
            cap = cap[0].replace(u'\xa0', u' ').strip()
            cs = cap.split()
            #ignore no unit capacity
            if len(cs) == 2:
                item['cap']=cs[0]
                item['capUnit'] = cs[1]
            # if cap == 0 maybe something goes wrong with the company
            print "Market Cap",cap
        yield item

    def parse_company(self, response):
        '''
            parse company page, extract a lot of information here 
            if there are ticker url to the company's stock page, yield a Request, let scrapy crawl              the url.
        '''
        hxs = HtmlXPathSelector(response)
        item = response.meta['item']
        #packing phone
        name = item['name']
        phone = hxs.select("//td[@align='LEFT']/text()").extract()
        if phone:
            phone = phone[0]
            phone = phone.lstrip("Phone:").lstrip()
            item['phone'] = phone
        #packing address
        adds=hxs.select('//td[@align="CENTER"][@class="Bold"]/text()').extract()
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
            redTexts = [ l.strip().replace('\r',' ') for l in redTexts ]
            redTexts = [ l.strip().replace('\n',' ') for l in redTexts ]
            item['red']=" ".join(redTexts)

        #packing businessSummary
        businessSummary = hxs.select("//span[text()='Business Summary']/following-sibling::table//td")
        if len(businessSummary) >= 2:
            businessSummary = businessSummary[1].select("text()").extract()
            if businessSummary:
                businessSummary = businessSummary[0].encode('ascii', 'ignore').strip()
                businessSummary = businessSummary.replace('\t',' ')
                item['businessSummary'] = businessSummary.replace('\r',' ')

        bnames = hxs.select("//span[text()='Business Names']/following-sibling::table//td[@align='LEFT']/text()").extract()
        i = 1
        for bn in bnames:
            #maximium 5 business name are packed
            if i > 5: continue
            item["bname%d"%i] = bn.encode('ascii', 'ignore').strip()
            i+=1
        
        #packing financial statements
        fs0=hxs.select("//a[text()='Annual Financials']/@href").extract()
        if fs0:
            item['statements0'] = self.extendHref(fs0[0],response)
        fs1=hxs.select("//a[text()='Quarterly Financials']/@href").extract()
        if fs1:
            item['statements1'] = self.extendHref(fs1[0],response)

        #packing Fiscal Year End
        fye=hxs.select("//td[text()='Fiscal Year End:']/following-sibling::td/text()").extract()
        if fye:
            item['fiscalYearEnd'] = fye[0]

        #packing lastAudit time
        lastAudit= hxs.select("//td[text()='Last Audit:']/following-sibling::td/text()").extract()
        if lastAudit:
            item['lastAudit'] = lastAudit[0]

        #packing Auditors
        auditors= hxs.select("//td[text()='Auditors:']/following-sibling::td/text()").extract()
        if auditors:
            item['auditors'] = auditors[0]

        #packing Audit Opinion
        auditOpinion = hxs.select("//td[text()='Audit Opinion:']/following-sibling::td/text()").extract()
        if auditOpinion:
            item['auditOpinion'] = auditOpinion[0]

        #packing public fillings
        publicFillings =hxs.select("//td[text()='Public Filings:']/following-sibling::td//a/@href").extract() 
        if publicFillings:
            for f in publicFillings:
                 item['publicFillings'] += self.extendHref(f,response) + " "

        #packing sec fillings
        secFillings = hxs.select("//td[text()='SEC Filings:']/following-sibling::td//a/@href").extract() 
        if secFillings:
            for s in secFillings:
                item['secFillings'] += self.extendHref(s,response) + " "


        #Industry: SIC and NAICS
        indCaptions=hxs.select("//td[text()='Industry']/../following-sibling::tr//td/text()").extract()
        indNames = hxs.select("//td[text()='Industry']/../following-sibling::tr//td//a/text()").extract()
        sicTailIndex = len(indNames)
        if "NAICS" in indCaptions:
            sicTailIndex = indCaptions.index("NAICS")
        for i in xrange(1,sicTailIndex):
            # maximium 5 code are packed
            if i > 5: continue
            item['sic%dcode'%(i)] = indCaptions[i]
            item['sic%dname'%(i)] = indNames[i-1]

        for i in xrange(sicTailIndex+1,len(indCaptions)):
            # maximium 5 code are packed
            if i-sicTailIndex > 5: continue
            item['naics%dcode'%(i-sicTailIndex)] = indCaptions[i]
            item['naics%dname'%(i-sicTailIndex)] = indNames[i-2]

        #packing Officers and Directors
        titleNames=hxs.select("//span[text()='Officers and Directors']/following-sibling::table//td/text()").extract()
        tnTuple=zip(titleNames[0::5],titleNames[1::5],titleNames[2::5],titleNames[3::5],titleNames[4::5])
        i=1
        for title,name,age,titleDate,startDate in tnTuple:
            item['title%d'%i] = title.encode('ascii', 'ignore')
            item['name%d'%i] = name.encode('ascii', 'ignore')
            item['age%d'%i] = age.encode('ascii', 'ignore')
            item['titleDate%d'%i] = titleDate.encode('ascii', 'ignore')
            item['startDate%d'%i] = startDate.encode('ascii', 'ignore')
            i+=1

        #packing number of employees
        noe = hxs.select("//td[text()='Number of Employees:']/following-sibling::td/text()").extract()
        if noe:
            item['numOfEmployees'] = noe[0]

        #packing outstanding shares
        shares = hxs.select("//td[text()='Outstanding Shares:']/following-sibling::td/text()").extract()
        if shares:
            item['shares'] = shares[0]

        #packing shareholders
        shareholders = hxs.select("//td[text()='Shareholders:']/following-sibling::td/text()").extract()  
        if shareholders:
            item['shareholders'] = shareholders[0]

        #packing taxId
        taxId = hxs.select("//td[text()='Federal Tax Id:']/following-sibling::td/text()").extract() 
        if taxId:
            item['taxId'] = taxId[0]

        #packing stock Exchange
        stockEx = hxs.select("//td[text()='Stock Exchange:']/following-sibling::td/text()").extract() 
        if stockEx:
            item['stockEx'] = stockEx[0]

        #packing news 
        newsDates = hxs.select("//span[text()='News Stories']/following-sibling::table//td[@align='RIGHT']/text()").extract()
        news = hxs.select("//span[text()='News Stories']/following-sibling::table//td//a")
        i=1
        for nd in newsDates:
            #maximium packing 3 news
            if i > 3: continue
            nd = nd.encode('ascii', 'ignore')
            if len(news) >= i:
                na = news[i]
                newsTitle = na.select('text()').extract()
                if newsTitle:
                    newsTitle = newsTitle[0].encode('ascii', 'ignore')
                else:
                    newsTitle = ""
                newsHref = na.select('@href').extract()
                if newsHref:
                    newsHref = self.extendHref(newsHref[0],response)
                else:
                    newsHref = ""

                item['newsDate%d'%i] = nd
                item['news%d'%i] = " ".join([newsTitle,newsHref])
            i += 1

        #packing ratings
        ratingRefs=hxs.select("//td[text()='Financial Ratings:']/..//a/@href").extract() 
        ratings = []
        for href in ratingRefs:
            ratings.append(self.extendHref(href,response))
        item['ratings'] = " ".join(ratings)

        #packing ticker
        tickerhref = hxs.select("//td[text()='Ticker: ']//a/@href").extract()
        ticker = hxs.select("//td[text()='Ticker: ']//a/text()").extract()
        if ticker:
            item['ticker'] = ticker[0]
        if tickerhref:
            tickerhref = tickerhref[0]
            #remove extra thing in href
            tickerhref = tickerhref.replace("javascript:window.location='","")
            tickerhref = tickerhref.strip("'")
            tickerhref = urlparse.urljoin(response.url, tickerhref)
            request = Request(tickerhref,self.parse_ticker)
            request.meta['item'] = item
            yield request
        else:
            #no ticker, no set Market capacity
            #just yield. because these fields already initialized
            yield item
        
    def parse(self, response):
        '''
            parse start url
            extract each company and their url
            yield a Request using their url, trigger scrapy crawl the url
        '''
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

                item['status'] = "Active"
                if t.select("@class").extract():
                    item['status'] = "Inactive"

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
        '''
            add domain of response to href
        '''
        tickerhref = tickerhref.replace("javascript:window.location='","")
        tickerhref = tickerhref.strip("'")
        tickerhref = urlparse.urljoin(response.url, tickerhref)
        return tickerhref

