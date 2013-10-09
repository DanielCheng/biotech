# Scrapy settings for biotech project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'biotech'

SPIDER_MODULES = ['biotech.spiders']
NEWSPIDER_MODULE = 'biotech.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'biotech (+http://www.yourdomain.com)'
ITEM_PIPELINES = {
'biotech.pipelines.BiotechPipeline': 300,
}
