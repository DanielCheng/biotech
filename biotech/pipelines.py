# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html
import csv
import xlwt
from biotech.items import BiotechItem

class BiotechPipeline(object):
    def __init__(self):
        self.file = open("all_bio_tech_companies.csv",'wb')
        self.csvFile = csv.writer(self.file) 
        item = BiotechItem()
        self.csvFile.writerow([ name for k,name in item.allKeyToNames()])
    def process_item(self, item, spider):
        print "Company:", item['name'], item['cap'],item['rss']
        #self.csvFile.writerow([ item[i] for i in item.keys()])
        row = [ item[key] for key,name in item.allKeyToNames() ] 
        self.csvFile.writerow(row) 
        return item
