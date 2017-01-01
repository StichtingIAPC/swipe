from django.utils import timezone
from django.db import models, transaction
from blame.models import Blame, ImmutableBlame
from article.models import ArticleType
from stock.models import StockChange, StockChangeSet, Stock, StockLabel
from stock.enumeration import enum
from tools.util import raiseif, raiseifnot
from crm.models import User
from money.models import Cost, CostField, AccountingGroup
from decimal import Decimal
from datetime import timedelta


class StockCountDocument(Blame):
    """
    The document collection all the counts of all the articles in the stock. The document is regarded as a diff
    from the previous stock count.
    """
    stock_change_set = models.ForeignKey(StockChangeSet, null=True)

    def save(self, **kwargs):
        # To ensure setting the time, this should not be done by Django/database as it is not reliable when
        # precision matters in time calculation which are crucial to the process.
        self.date_created = timezone.now()
        super(StockCountDocument, self).save()

    @staticmethod
    def get_discrepancies():
        """
        This function is important to the stock count. It generates a list of function where the stored count is not
        equal to the expected count as in the TemporaryArticleCount for the article. This is needed because of the
        Stock-lines that articles can be taken from. When there is a shortage of items, you need to be able to pick
        the Stock-lines from which to subtract the articles. This function indicates where differences, if any, are.
        After this, you should be able to puzzle how to solve any stock shortage.

        """
        # In practice, the system should be more automatic and lenient. It will suffice for now.
        raiseif(ArticleType.objects.count() != TemporaryArticleCount.objects.filter(checked=True).count(), UncountedError,
                "The number of ArticleTypes is not equal to the number of counted ArticleTypes")
        tacs = TemporaryArticleCount.objects.all()
        article_counts = {}
        for tac in tacs:
            article_counts[tac.article_type] = tac.count

        changes, stock_count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        counter_lines = TemporaryCounterLine.\
            get_all_temporary_counterlines_since_last_stock_count(stock_changes=changes,
                                                                  last_stock_count=stock_count)
        discrepancies = []
        for line in counter_lines:
            article_type = line.article_type
            diff = article_counts[article_type] - line.expected_count
            if diff != 0:
                discrepancies.append((article_type, diff))

        return discrepancies

    @staticmethod
    def create_stock_count(user: User):
        """
        Creates a stock count. This requires the following things:
        - all ArticleTypes are counted as in TemporaryArticleCount
        - For any discrepancies where the physical count of an ArticleType is lower than the expected count,
        enough valid DiscrepancySolution-s are offered to pick the correct StockLine-s to subtract the differing
        articles from.
        If the above conditions are met, the system will be able to create a StockCount with the relevant
        StockCountLines.
        :param user: The user who authorised the process
        :return:
        """
        discrepancies = StockCountDocument.get_discrepancies()

        solutions = DiscrepancySolution.objects.all().order_by('id')
        # Throw the solutions into dicts for easy comparison
        solution_dict = {}
        for solution in solutions:
            entry = solution_dict.get(solution.article_type, None)
            if entry:
                solution_dict[solution.article_type].append(solution)
            else:
                solution_dict[solution.article_type] = [solution]

        # Do we still need the original? I'm not sure so lets use a copy.
        discrepancies_left = discrepancies.copy()
        # Stock modifications to be done
        entries = []

        for article, difference in discrepancies_left:
            if difference > 0:
                sts = Stock.objects.filter(article=article, labelkey__isnull=True)
                if len(sts) == 1:
                    entries.append({'article': article,
                                    'book_value': sts[0].book_value,
                                    'count': difference,
                                    'is_in': True})
                else:
                    last_change = StockChange.objects.filter(article=article).last()  # type: StockChange
                    if last_change:
                        entries.append({'article': article,
                                        'book_value': last_change.book_value,
                                        'count': difference,
                                        'is_in': True})
                    else:
                        # An article was counted but something like it has never come in before.
                        # An elegant solution is probably possible but this situation seems incredibly unlikely
                        entries.append({'article': article,
                                        'book_value': Cost(amount=Decimal(0), use_system_currency=True),
                                        'count': difference,
                                        'is_in': True})
            elif difference < 0:
                matchings = solution_dict.get(article, None)  # type: list[DiscrepancySolution]
                if matchings:
                    to_be_solved = difference*-1
                    no_of_matchings = len(matchings)
                    i = 0
                    while to_be_solved > 0 and i < no_of_matchings:
                        match = matchings[i]
                        try:
                            st = Stock.objects.get(article=match.article_type, labeltype=match.stock_label,
                                                   labelkey=match.stock_key)
                            if st.count <= to_be_solved:
                                stock_change= {'article': article,
                                                'book_value': st.book_value,
                                                'count': st.count,
                                                'is_in': False}
                                if match.stock_label:
                                    stock_change['label'] = StockLabel.return_label(match.stock_label, match.stock_key)
                                entries.append(stock_change)
                                to_be_solved -= st.count
                            else:
                                stock_change = {'article': article,
                                                'book_value': st.book_value,
                                                'count': to_be_solved,
                                                'is_in': False}
                                if match.stock_label:
                                    stock_change['label'] = StockLabel.return_label(match.stock_label, match.stock_key)
                                entries.append(stock_change)
                                to_be_solved = 0
                            i += 1
                        except Stock.DoesNotExist:
                            raise SolutionError("Solution {} does not exist in Stock".format(match))
                    if to_be_solved > 0:
                        raise SolutionError("Not enough solutions for article {}".format(article))
                else:
                    raise SolutionError("No solutions where provided yet a negative discrepancy was found")
            else:
                raise FunctionError("The difference function indicated an error of 0 for {}. This is not possible".
                                    format(article))

        # If we are here, we can assume everything worked out ok

        counts = TemporaryArticleCount.get_count_dict()
        changes, count = TemporaryCounterLine.get_all_stock_changes_since_last_stock_count()
        mods = TemporaryCounterLine.get_all_temporary_counterlines_since_last_stock_count(changes, count)
        money_values = Stock.get_all_average_prices_and_amounts()
        # Let's save
        with transaction.atomic():
            doc = StockCountDocument(user_modified=user)
            doc.save()
            for mod in mods:
                physical = counts.get(mod.article_type, None)
                raiseif(physical is None, UncountedError, "ArticleType {} is uncounted".format(mod.article_type))
                avg_tuple = money_values.get(mod.article_type)
                if not avg_tuple:
                    avg = Cost(amount=Decimal(0), use_system_currency=True)
                else:
                    avg=avg_tuple[1]
                scl = StockCountLine(document=doc, article_type=mod.article_type, previous_count=mod.previous_count,
                                     in_count=mod.in_count, out_count=mod.out_count,
                                     physical_count=physical, average_value=avg, text=mod.article_type.name,
                                     accounting_group_id=mod.article_type.accounting_group_id)
                scl.save()
            change_set = StockChangeSet.construct(description="Stockchanges for Stock count", entries=entries,
                                                  enum=enum["stock_count"])
            # We now have a saved document. Lets set the stock change set for checking purposes
            doc.stock_change_set = change_set
            doc.save()
            change_set.date = doc.date_created+timedelta(milliseconds=10)
            change_set.save(indirect=True)
            return doc


class StockCountLine(models.Model):
    """
    A line on a stock count. Considers all changes that have happened to an article since the last stock count.
    Registers the difference between the expected value and the real value by storing the expected number and
    the physical count of the product. The expected value is previous_count+in_count-out_count
    """

    # The document which it
    document = models.ForeignKey(StockCountDocument)
    # The article type
    article_type = models.ForeignKey(ArticleType)
    # The amount present at a previous count(or 0 if there was no previous count for this product)
    previous_count = models.IntegerField()
    # How much entered the system since the previous count
    in_count = models.IntegerField()
    # How much exited the system since the previous count
    out_count = models.IntegerField()
    # How much is actually present
    physical_count = models.IntegerField()
    # NB: The expected count is 'previous_count + in_count - out_count' and this conforms to the database count
    # The average value per product over all the products in stock
    average_value = CostField()
    # The snapshot of the name of the ArticleType
    text = models.CharField(max_length=255)
    # The accounting group of the ArticleType for snapshotting
    accounting_group = models.ForeignKey(AccountingGroup)

    def __str__(self):
        if hasattr(self, 'document'):
            doc = str(self.document_id)
        else:
            doc = "None"
        if hasattr(self, 'article_type'):
            art = str(self.article_type_id)
        else:
            art = 'None'
        if hasattr(self, 'accounting_group'):
            acc = str(self.accounting_group)
        else:
            acc = 'None'
        return "Document: {}, ArticleType: {}, Previous: {}," \
               " In: {}, Out: {}, Physical: {}, Average value: {}, " \
               "Text: {}, Accounting group: {}".format(doc, art, self.previous_count, self.in_count, self.out_count,
                                                       self.physical_count, self.average_value, self.text, acc)

    def __eq__(self, other):
        if not isinstance(other, StockCountLine):
            return False
        else:
            return self.document_id == other.document_id and self.article_type_id == other.article_type_id and \
                self.previous_count == other.previous_count and self.in_count == other.in_count \
                and self.out_count == other.out_count and self.physical_count == other.physical_count and \
                self.average_value == other.average_value and self.text == other.text and \
                self.accounting_group_id == other.accounting_group_id


class DiscrepancySolution(models.Model):
    """
    A collection of solutions for discrepancies that reduce stock.
    The solutions for each article are used in order of primary key.
    """
    # The articleType to delete items from stock from
    article_type = models.ForeignKey(ArticleType)
    # The stocklabel string to potentially delete the articles from. null for stock
    stock_label = models.CharField(null=True, max_length=30)
    # The stocklabel key to potentially delete articles from
    stock_key = models.IntegerField(null=True)

    @staticmethod
    def remove_all_solutions():
        DiscrepancySolution.objects.all().delete()

    @staticmethod
    def remove_solution_for_article_type(article_type):
        raiseifnot(isinstance(article_type, ArticleType), TypeError, "article_type should be an ArticleType")
        DiscrepancySolution.objects.filter(article_type=article_type).delete()

    @staticmethod
    def add_solutions(discrepancy_solutions):
        """
        Adds solutions for discrepancies that have less than expected articles. These solutions are used in order,
        to subtract articles from.
        :param discrepancy_solutions: List[DiscrepancySolutions] Entered in order of importance for
        solving the discrepancy. There need to be enough for these to resolve all the shortages.
        :type discrepancy_solutions: list[DiscrepancySolution]
        """
        for ds in discrepancy_solutions:
            raiseifnot(isinstance(ds, DiscrepancySolution), TypeError, "ds should be a DiscrepancySolution")
            ds.save()

    def __str__(self):
        if hasattr(self, 'article_type'):
            art = self.article_type_id
        else:
            art = 'None'
        return "ArticleType: {}, LabelType: {}, LabelKey: {}".format(art, self.stock_label, self.stock_key)


class TemporaryCounterLine:
    """
    A line that is presented to the user of a Stock count. Contains information generated from the database
    """

    article_type = ArticleType()

    previous_count = 0

    in_count = 0

    out_count = 0

    expected_count = 0

    def __init__(self, article_type, previous_count, in_count, out_count):
        self.article_type = article_type
        self.previous_count = previous_count
        self.in_count = in_count
        self.out_count = out_count
        self.expected_count = previous_count + in_count - out_count

    def __str__(self):
        return "Article: {}, prev: {}, in: {}, out: {}, expected: {}".format(self.article_type, self.previous_count,
                                                                             self.in_count, self.out_count,
                                                                             self.expected_count)

    def __eq__(self, other):
        if type(other) is not TemporaryCounterLine:
            return False
        else:
            return (self.article_type == other.article_type and self.previous_count == other.previous_count
            and self.in_count == other.in_count and self.out_count == other.out_count and self.expected_count ==
                    other.expected_count)

    @staticmethod
    def get_all_stock_changes_since_last_stock_count():
        if StockCountDocument.objects.exists():
            last_stock_count = StockCountDocument.objects.last()
            stock_changes = StockChange.objects.filter(
                change_set__date__gt=last_stock_count.date_created).select_related("change_set")
        else:
            last_stock_count = None
            stock_changes = StockChange.objects.all().select_related("change_set")

        return stock_changes, last_stock_count

    @staticmethod
    def get_all_temporary_counterlines_since_last_stock_count(stock_changes, last_stock_count: StockCountDocument):
        """
        Returns a list of all temporary counter lines since the last stock. It makes these lines from the
        stock changes since the last stock count.
        :param stock_changes:
        :param last_stock_count:
        :rtype list[TemporaryCounterLine]
        :return:
        """
        article_mods = {}
        for change in stock_changes:
            if article_mods.get(change.article):
                if change.is_in:
                    article_mods[change.article].in_count = article_mods[change.article].in_count + change.count
                else:
                    article_mods[change.article].out_count = article_mods[change.article].out_count + change.count
            else:
                if change.is_in:
                    article_mods[change.article] = TemporaryCounterLine(change.article, 0, change.count, 0)
                else:
                    article_mods[change.article] = TemporaryCounterLine(change.article, 0, 0, change.count)

        # Grab articles that are not yet considered in the list. These are articles which contained no modification
        # since the last stock count. They could however, still be in stock.
        modded_articles = list(article_mods.keys())
        modded_article_ids = []
        for m_a in modded_articles:
            modded_article_ids.append(m_a.id)

        if len(modded_article_ids) != ArticleType.objects.count():
            ats = list(ArticleType.objects.all().exclude(id__in=modded_article_ids))
        else:
            ats = []

        for at in ats:
            article_mods[at] = TemporaryCounterLine(at, 0, 0, 0)

        article_mods = list(article_mods.values())

        if last_stock_count:
            count_lines = StockCountLine.objects.filter(document=last_stock_count)
            count_dict = {}
            # Full the previous value as the expected value(DB value) at the previous count
            for line in count_lines:
                count_dict[line.article_type] = line.previous_count + line.in_count - line.out_count

            for mod in article_mods:
                count = count_dict.get(mod.article_type, None)
                if count:
                    mod.previous_count = count

        for mod in article_mods:  # Type: TemporaryCounterLine
            mod.expected_count = mod.previous_count + mod.in_count - mod.out_count

        return article_mods  # Type: List[TemporaryCounterLine]


class TemporaryArticleCount(models.Model):
    """
    Temporary store of the article count. This allows for multiple users counting the stock separately. Used as eventual
    input as the actual count.
    """
    # The articleType to be counted
    article_type = models.OneToOneField(ArticleType)
    # The number of articles counted temporarily.
    count = models.IntegerField()
    # Checks if the amount is truly counted or just a default.
    checked = models.BooleanField(default=False)

    @staticmethod
    def clear_temporary_counts():
        """
        Sets all counts back to 0
        """
        TemporaryArticleCount.objects.all().update(count=0, checked=False)
        article_type_ids = TemporaryArticleCount.objects.all().values('id')
        ats = ArticleType.objects.exclude(id__in=article_type_ids)
        if len(ats) > 0:
            new_temporary_article_counts = []
            for at in ats:
                new_temporary_article_counts.append(TemporaryArticleCount(article_type=at, count=0, checked=False))
            TemporaryArticleCount.objects.bulk_create(new_temporary_article_counts)

    @staticmethod
    def update_temporary_counts(article_type_count_combinations):
        """
        Generates a temporary store of article type counts. Persists until a count is completed.
        :param article_type_count_combinations: List[Tuple[ArticleType, int]] A number of articleTypes, which have
        a certain temporary count
        """
        # Not the fastest, fix by some smart fetching if this proves to be slow
        for article, count in article_type_count_combinations:
            art = TemporaryArticleCount.objects.filter(article_type=article)
            if len(art) == 0:
                TemporaryArticleCount.objects.create(article_type=article, count=count, checked=True)
            else:
                art[0].count = count
                art[0].checked = True
                art[0].save()

    @staticmethod
    def get_count_dict():
        """
        Returns a dictionary of all counts that are checked.
        """
        result = {}
        lst = list(TemporaryArticleCount.objects.filter(checked=True))
        for elem in lst:
            result[elem.article_type] = elem.count
        return result

    def __str__(self):
        return "Article: {}, count: {}, checked: {}".format(self.article_type, self.count, self.checked)

    def __eq__(self, other):
        if type(other) is not TemporaryArticleCount:
            return False
        else:
            return self.article_type == other.article_type and self.count == other.count \
                   and self.checked == other.checked


class UncountedError(Exception):
    pass


class FunctionError(Exception):
    pass


class SolutionError(Exception):
    pass

