import random
# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html


class RandomUserAgentMiddleware:
    def __init__(self, user_agent_list):
        self.user_agent_list = user_agent_list

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

    @classmethod
    def from_crawler(cls, crawler):
        s = crawler.settings
        return cls(s.get('USER_AGENT_LIST'))
