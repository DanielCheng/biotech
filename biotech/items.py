# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BiotechItem(Item):
    # define the fields for your item here like:
    # name = Field()
    href = Field()
    businessSummary = Field()
    #business names
    bnames = Field()
    leaders = Field()

    id = Field()
    number = Field()
    name = Field()
    rss = Field()
    country = Field()
    state = Field()
    status = Field()
    addr0 = Field()
    addr1 = Field()
    addr2 = Field()
    addr3 = Field()
    phone = Field()
    fax = Field()
    #market cap
    cap = Field()
    red = Field()
    ticker = Field()
    ratings = Field()
    statements0 = Field()
    statements1 = Field()
    fiscalYearEnd = Field()
    lastAudit = Field()
    auditors = Field()
    auditOpinion = Field()
    publicFillings = Field()
    secFillings = Field()
    sic1code = Field() 
    sic1name = Field() 
    sic2code = Field() 
    sic2name = Field() 
    sic3code = Field() 
    sic3name = Field() 
    sic4code = Field() 
    sic4name = Field() 
    sic5code = Field() 
    sic5name = Field() 
    naics1code = Field()
    naics1name = Field()
    naics2code = Field()
    naics2name = Field()
    naics3code = Field()
    naics3name = Field()
    naics4code = Field()
    naics4name = Field()
    naics5code = Field()
    naics5name = Field()
    
    def initAll(self): 
        for k,name in self.allKeyToNames():
            self[k] = ""

    def allKeyToNames(self):
        keyNameList=[
                ('number','Number'),
                ('name','Company Name'),
                ('rss','RSS'),
                ('country','Country'),
                ('state','State/Province'),
                ('status','Active/Inactive'),
                ('addr0','Company'),
                ('addr1','Address1'),
                ('addr2','Address2'),
                ('addr3','Address3'),
                ('phone','Phone'),
                ('fax','Fax'),
                ('ticker','Ticker'),
                ('cap','Market Cap'),
                ('red','Red Remarks'),
                ('businessSummary',"Business Summary"),
                ('ratings','Financial Ratings'),
                ('statements0','Latest Financial Statements'),
                ('statements1','Latest Financial Statements'),
                ('fiscalYearEnd','Fiscal Year End'),
                ('lastAudit','last Audit time'),
                ('auditors','Auditors'),
                ('auditOpinion','Audit Opinion'),
                ('publicFillings','Public Filings'),
                ('secFillings','SEC Filings'),
                ('sic1code','SIC1-code'),
                ('sic1name','SIC1-name'),
                ('sic2code','SIC2-code'),
                ('sic2name','SIC2-name'),
                ('sic3code','SIC3-code'),
                ('sic3name','SIC3-name'),
                ('sic4code','SIC4-code'),
                ('sic4name','SIC4-name'),
                ('sic5code','SIC5-code'),
                ('sic5name','SIC5-name'),
                ('naics1code','NAICS1-code'),
                ('naics1name','NAICS1-name'),
                ('naics2code','NAICS2-code'),
                ('naics2name','NAICS2-name'),
                ('naics3code','NAICS3-code'),
                ('naics3name','NAICS3-name'),
                ('naics4code','NAICS4-code'),
                ('naics4name','NAICS4-name'),
                ('naics5code','NAICS5-code'),
                ('naics5name','NAICS5-name'),
        ]
        return keyNameList

class CompanyLinkItem(Item):
    pass
