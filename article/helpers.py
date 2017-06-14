from article.models import ArticleType
from tools.json_parsers import ParseError


class ArticleDictParsers:

    @staticmethod
    def article_parser(obj: int):
        if not obj:
            raise ParseError("Article does not exist")
        if not isinstance(obj, int):
            raise ParseError("Article is not an int")
        return ArticleType.objects.get(id=obj)