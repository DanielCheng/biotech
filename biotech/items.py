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
    capUnit = Field()
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
    title1 = Field()
    name1 = Field()
    age1 = Field()
    titleDate1 = Field()
    startDate1 = Field()
    title2 = Field()
    name2 = Field()
    age2 = Field()
    titleDate2 = Field()
    startDate2 = Field()
    title3 = Field()
    name3 = Field()
    age3 = Field()
    titleDate3 = Field()
    startDate3 = Field()
    title4 = Field()
    name4 = Field()
    age4 = Field()
    titleDate4 = Field()
    startDate4 = Field()
    title5 = Field()
    name5 = Field()
    age5 = Field()
    titleDate5 = Field()
    startDate5 = Field()
    bname1 = Field()
    bname2 = Field()
    bname3 = Field()
    bname4 = Field()
    bname5 = Field()
    numOfEmployees = Field()
    shares = Field()
    shareholders = Field()
    taxId = Field()
    stockEx = Field()
    newsDate1 = Field()
    news1 = Field()
    newsDate2 = Field()
    news2 = Field()
    newsDate3 = Field()
    news3 = Field()
    
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
                ('capUnit','Market Cap Unit'),
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
                ('title1','Title1'),
                ('name1','Name1'),
                ('age1','Age1'),
                ('titleDate1','titleDate1'),
                ('startDate1','startDate1'),
                ('title2','Title2'),
                ('name2','Name2'),
                ('age2','Age2'),
                ('titleDate2','titleDate2'),
                ('startDate2','startDate2'),
                ('title3','Title3'),
                ('name3','Name3'),
                ('age3','Age3'),
                ('titleDate3','titleDate3'),
                ('startDate3','startDate3'),
                ('title4','Title4'),
                ('name4','Name4'),
                ('age4','Age4'),
                ('titleDate4','titleDate4'),
                ('startDate4','startDate4'),
                ('title5','Title5'),
                ('name5','Name5'),
                ('age5','Age5'),
                ('titleDate5','titleDate5'),
                ('startDate5','startDate5'),
                ('bname1','Business Name1'),
                ('bname2','Business Name2'),
                ('bname3','Business Name3'),
                ('bname4','Business Name4'),
                ('bname5','Business Name5'),
                ('numOfEmployees','Number of Employees'),
                ('shares','Outstanding Shares:'),
                ('shareholders','Shareholders:'),
                ('taxId','Federal Tax Id:'),
                ('stockEx','Stock Exchange:'),
                ('newsDate1',"News Date 1"),
                ('news1',"News 1"),
                ('newsDate2',"News Date 2"),
                ('news2',"News 2"),
                ('newsDate3',"News Date 3"),
                ('news3',"News 3"),
        ]
        return keyNameList

class CompanyLinkItem(Item):
    pass
