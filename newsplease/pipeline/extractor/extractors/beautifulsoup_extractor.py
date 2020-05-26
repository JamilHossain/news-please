from copy import deepcopy

from bs4 import BeautifulSoup

from .abstract_extractor import AbstractExtractor
from ..article_candidate import ArticleCandidate


class ReadabilityExtractor(AbstractExtractor):
    """This class implements Readability as an article extractor. Readability is
    a subclass of Extractors and newspaper.Article.

    """

    def __init__(self):
        self.name = "beautifulsoup"

    def extract(self, item):
        """Creates an readability document and returns an ArticleCandidate containing article title and text.

        :param item: A NewscrawlerItem to parse.
        :return: ArticleCandidate containing the recovered article data.
        """
        
        description = None
        doc = BeautifulSoup(item['spider_response'].body,'html.parser')
        article = doc.find_all('article')
        if article:
            description = article[0].get_text()

        f = open("log.log","a")
        f.write("BeautifulSoup: \r\n")
        if description is not None:
            f.write(description)
        f.write("\r\n")
        if self._text(item) is not None:
            f.write("TEXT: " + self._text(item))
        f.close()
        
        text = self._text(item)
        if text is None:
           text = description

        article_candidate = ArticleCandidate()
        article_candidate.extractor = self._name
        #article_candidate.title = doc.short_title()
        article_candidate.description = description
        article_candidate.text = text
        article_candidate.topimage = self._topimage(item)
        article_candidate.author = self._author(item)
        article_candidate.publish_date = self._publish_date(item)
        article_candidate.language = self._language(item)

        return article_candidate
