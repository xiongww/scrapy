"""
StatsMailer extension sends an email when a spider finishes scraping.

Use STATSMAILER_RCPTS setting to enable and give the recipient mail address
"""

from scrapy import signals
from scrapy.mail import MailSender
from scrapy.conf import settings
from scrapy.exceptions import NotConfigured

class StatsMailer(object):

    def __init__(self, stats):
        self.recipients = settings.getlist("STATSMAILER_RCPTS")
        if not self.recipients:
            raise NotConfigured
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.stats)
        crawler.connect(o.stats_spider_closed, signal=signals.stats_spider_closed)
        return o
        
    def stats_spider_closed(self, spider, spider_stats):
        mail = MailSender()
        body = "Global stats\n\n"
        body += "\n".join("%-50s : %s" % i for i in self.stats.get_stats().items())
        body += "\n\n%s stats\n\n" % spider.name
        body += "\n".join("%-50s : %s" % i for i in spider_stats.items())
        mail.send(self.recipients, "Scrapy stats for: %s" % spider.name, body)
