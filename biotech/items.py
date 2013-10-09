# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class BiotechItem(Item):
    # define the fields for your item here like:
    # name = Field()
    href = Field()
    history = Field()
    #market cap
    cap = Field()
    #business names
    bnames = Field()
    #Industry of SIC
    SIC = Field()
    #Industry of NAICS
    NAICS = Field()
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
                ('cap','Market Cap'),
        ]
        return keyNameList

class CompanyLinkItem(Item):
    pass
