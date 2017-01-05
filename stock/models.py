from django.db import models
from django.db import transaction
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from article.models import ArticleType
from money.models import CostField
from stock.exceptions import StockSmallerThanZeroError, Id10TError
from money.exceptions import CurrencyInconsistencyError
from stock.stocklabel import StockLabeledLine, StockLabel
from swipe.settings import DELETE_STOCK_ZERO_LINES, FORCE_NEGATIVE_STOCKCHANGES_TO_MAINTAIN_COST
from crm.models import User
from tools.util import raiseif
# Stop PyCharm from seeing tools as a package.
# noinspection PyPackageRequirements
from tools.management.commands.consistencycheck import consistency_check, HIGH


class Stock(StockLabeledLine):
    """
        Keeps track of the current state of the stock
        Do not edit this thing directly, use StockChangeSet.construct instead.

        article: What product is this line about?
        count: How many are in stock?
        book_value: What's the cost per product for this product?
    """
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    book_value = CostField()

    def save(self, *args, indirect=False, **kwargs):
        if not indirect:
            raise Id10TError(
                "Stock modifications shouldn't be done directly, but rather, they should be done on StockChangeSet.")
        super(Stock, self).save(*args, **kwargs)

    def to_key(self):
        return "{}_{}_{}".format(self.pk, self.labeltype, self.labelkey)

    @staticmethod
    @consistency_check
    def do_check():
        errors = []
        stock = Stock.objects.all()
        required_result = {}
        for st in stock:
            if st.labeltype is not None and st.labeltype not in StockLabel.labeltypes:
                errors.append({"text": "StockLabelType {} not currrently"
                                       "in use, but still in use in DB".format(st.labeltype),
                               "location": "Stock",
                               "Line": st.pk,
                               "severity": HIGH})
            key = "{}_{}_{}".format(st.article_id, st.labeltype, st.labelkey)
            if key in required_result.keys():
                errors.append({"text": 'Same stockline exists twice, even though it should be unique: {}.'.format(key),
                               "location": 'Stock',
                               "Line": st.pk,
                               "severity": HIGH})
            required_result[key] = {"count": st.count, "bookvalue": st.book_value}
        running_result = {}
        changes = StockChange.objects.all()

        for change in changes:
            key = "{}_{}_{}".format(change.article_id, change.labeltype, change.labelkey)
            if change.labeltype is not None and change.labeltype not in StockLabel.labeltypes:
                errors.append({"text": "StockLabelType {} not currrently in use,"
                                       "but still in use in DB".format(change.labeltype),
                               "location": "StockChange",
                               "Line": change.pk,
                               "severity": HIGH})
            if key in running_result.keys():
                if change.count < 0:
                    if change.cost != running_result[key]["cost"]:
                        errors.append({"text": 'Inconsistency found in stock:'
                                               'negative stock, cost of removal differs:'
                                               '{} instead of {}'.format(change.cost, running_result[key]["cost"]),
                                       "location": 'StockChange',
                                       "Line": change.pk,
                                       "severity": HIGH})
                if change.get_count() + running_result[key]["count"] != 0:
                    running_result[key]["bookvalue"] = (
                                                       running_result[key]["bookvalue"] * running_result[key]["count"] +
                                                       change.book_value * change.get_count()) / \
                                                       (change.get_count() + running_result[key]["count"])
                running_result[key]["count"] = running_result[key]["count"] + change.get_count()
                if running_result[key]["count"] < 0:
                    errors.append({"text": 'Inconsistency found in stock:' +
                                           " stock levels turn (temporarily) negative in the past.",
                                   "location": 'StockChange',
                                   "line": change.pk,
                                   "severity": HIGH})

            else:
                running_result[key] = {"count": change.get_count(), "bookvalue": change.book_value}
        key_list = list(required_result.keys())
        for z in key_list:
            a = required_result.pop(z, None)
            b = running_result.pop(z, None)
            if b is None or a["count"] != b["count"] or a["bookvalue"] != b["bookvalue"]:
                if b is None and a["count"] != 0:
                    errors.append({"text": 'Found no stock for {} when rerunning, '
                                           'but {} are still in Stock according to the Database'.format(z, a["count"]),
                                   "location": 'Recalculated Stock',
                                   "line": z,
                                   "severity": HIGH})
                else:
                    errors.append(dict(
                        text="Different counts or costs found for"
                             "{}: ({} {}) found, ({} {}) expected".format(
                                 z, a["count"], a["bookvalue"], b["count"], b["bookvalue"]),
                        location='Stock', line=z, severity=HIGH))

        key_list = list(running_result.keys())
        for z in key_list:
            b = running_result.pop(z, None)
            if b["count"] != 0:
                errors.append({
                    "text": 'Running result found stock not in normal Stock! '
                            'Call for help, this is serious'.format(b["count"], b["bookvalue"]),
                    "location": 'Recalculated Stock',
                    "line": z})
        return errors

    @staticmethod
    def get_merge_line(mod):
        try:
            if mod.label is None:
                return Stock.objects.get(article=mod.article, labeltype=None)
            else:
                return Stock.objects.get(article=mod.article, labeltype=mod.labeltype, labelkey=mod.labelkey)
        except Stock.DoesNotExist:
            return None

    @staticmethod
    def modify(stock_mod):
        merge_line = Stock.get_merge_line(stock_mod)
        # Create new merge_line
        if not merge_line:
            merge_line = Stock(article=stock_mod.article, label=stock_mod.label, book_value=stock_mod.book_value,
                               count=stock_mod.get_count())
        else:
            # Merge average book_value
            if merge_line.book_value.currency != stock_mod.book_value.currency:
                raise CurrencyInconsistencyError("GOT {} instead of {}".format(
                    merge_line.book_value.currency, stock_mod.book_value.currency))

            if FORCE_NEGATIVE_STOCKCHANGES_TO_MAINTAIN_COST \
                    and int((merge_line.book_value.amount - stock_mod.book_value.amount) * 10 ** 5) != 0 \
                    and stock_mod.get_count() < 0:
                raise ValueError("book value changed during negative line, "
                                 "from: {} to: {} ".format(merge_line.amount, stock_mod.book_value.amount))

            old_cost = merge_line.book_value
            if stock_mod.get_count() + merge_line.count != 0:
                merge_cost_total = (
                    merge_line.book_value * merge_line.count + stock_mod.book_value * stock_mod.get_count()
                )
                merge_line.book_value = merge_cost_total / (stock_mod.get_count() + merge_line.count)
            if FORCE_NEGATIVE_STOCKCHANGES_TO_MAINTAIN_COST \
                    and int((merge_line.book_value.amount - old_cost.amount) * 10 ** 5) != 0 \
                    and stock_mod.get_count() < 0:
                raise ValueError("book value changed during negative line, "
                                 "from: {} to: {} ".format(old_cost.amount, merge_line.book_value.amount))
            # Update stockmod count
            merge_line.count += stock_mod.get_count()

        if merge_line.count < 0:
            raise StockSmallerThanZeroError("Stock levels can't be below zero.")

        # Delete line if at zero and software wants to delete line
        if merge_line.count == 0 and DELETE_STOCK_ZERO_LINES:
            if merge_line.id is not None:
                merge_line.delete()
        else:
            merge_line.save(indirect=True)

        return merge_line

    def __str__(self):
        return "{}| {}: {} @ {} {}".format(self.pk, self.article, self.count, self.book_value, self.label)

    class Meta:
        # This check  is only partly valid, because most databases don't enforce null uniqueness.
        unique_together = ('labeltype', 'labelkey', 'article',)


class StockChangeSet(models.Model):
    """
    A log of one or multiple stockchanges
    """

    # The possible sources for a StockChange. If you change this, please only ADD new sources,
    # and only remove or edit them if you are absolutely sure what you are doing!
    # If you change this you will need to create a new migration, and
    # possibly a data migration if you change the existing strings!
    SOURCE_CASHREGISTER = "cash_register"
    SOURCE_SUPPLICATION = "supplication"
    SOURCE_RMA = "rma"
    SOURCE_INTERNALISE = "internalise"
    SOURCE_EXTERNALISE = "externalise"
    SOURCE_REVALUATION = "revaluation"

    # The choices for the source field, using the keys specified above.
    # The keys are separate variables so you can use them in other models (e.g. StockChangeSet.SOURCE_CASHREGISTER)
    # If you change this you will need to create a new migration.
    STOCKCHANGE_SOURCES = (
        (SOURCE_CASHREGISTER, _("Cash register")),
        (SOURCE_SUPPLICATION, _("Supplication")),
        (SOURCE_RMA, _("RMA")),
        (SOURCE_INTERNALISE, _("Internalise")),
        (SOURCE_EXTERNALISE, _("Externalise")),
        (SOURCE_REVALUATION, _("Revaluation")),
    )

    # Date the changes were done
    date = models.DateTimeField(auto_now_add=True)

    # Description of what happened
    memo = models.CharField(max_length=255, null=True)

    # The source of these changes, from the possible sources in the settings.
    source = models.CharField(max_length=50, choices=STOCKCHANGE_SOURCES)

    def save(self, *args, indirect=False, **kwargs):
        if not indirect:
            raise Id10TError(
                "Please use the StockChangeSet.construct function.")
        super(StockChangeSet, self).save(*args, **kwargs)

    @classmethod
    @transaction.atomic()
    def construct(cls, description, entries, source):
        """
        Construct a modification to the stock, and log it to the StockChangeSet.
        :param description: A description of what happened
        :type description: str
        :param entries: A list of dictionaries with the data for the stock modifications. Each dictionary should have
                        at least the keys "article", "count", "book_value" and "is_in". See StockChange.
        :type entries: list(dict)
        :param source: The source of these changes, from one of StockChangeSet.STOCKCHANGE_SOURCES.
        :type source: str
        :return: A completed StockChangeSet of the modification
        :rtype: StockChangeSet
        """
        # Check if stock is locked
        if StockLock.is_locked():
            raise LockError("Stock is locked. Unlock first")
        # Check if the entry dictionaries are complete
        for entry in entries:
            stock_modification_keys = ['article', 'count', 'book_value', 'is_in']

            if not all(key in entry.keys() for key in stock_modification_keys):
                raise ValueError("Missing data in StockChangeSet entry values.\n"
                                 "Expected keys: {}\n"
                                 "Entry: {},\n"
                                 "StockChangeSet description: {}".format(stock_modification_keys, entry, description))

        # Create the StockChangeSet instance to use as a foreign key in the Stockchanges
        sl = StockChangeSet(memo=description, source=source)
        sl.save(indirect=True)

        # Create the Stockchanges and set the StockChangeSet in them.
        for entry in entries:
            try:
                if not isinstance(entry["count"], int):
                    raise ValueError("count isn't integer")
                s = StockChange(change_set=sl, **entry)
                s.save(indirect=True)
            except ValueError as e:
                raise ValueError("Something went wrong while creating the a stock modification: {}".format(e))

        # Modify the stock for each StockChange now linked to the StockChangeSet we created
        for modification in sl.stockchange_set.all():
            Stock.modify(modification)

        # Return the created StockChangeSet
        return sl


class StockChange(StockLabeledLine):
    """
        change_set: What article is this StockChange a part of
        count: How many articles is this modification?
        book_value: What's the cost (per object) for this modification?
        is_in: Is this an in  (True) or an out (False)
        memo:  description of why this stock change happened. It's optional.
    """
    article = models.ForeignKey(ArticleType)
    count = models.IntegerField()
    book_value = CostField()

    change_set = models.ForeignKey(StockChangeSet)
    is_in = models.BooleanField()
    memo = models.CharField(blank=True, max_length=255)

    def save(self, *args, indirect=False, **kwargs):
        if not indirect:
            raise Id10TError(
                "Please use the StockChangeSet.construct function.")
        super(StockChange, self).save(*args, **kwargs)

    def get_count(self):
        if self.is_in:
            return self.count
        else:
            return -1 * self.count

    @property
    def date(self):
        return self.change_set.date

    def __str__(self):
        return "{}| {} x {} {}".format(self.pk, self.count, self.article, self.label)


class StockLock(models.Model):
    """
    A locker for the stock
    """

    # Indicates if the stock is locked
    locked = models.BooleanField(default=False)

    def delete(self, using=None, keep_parents=False):
        # No deletion
        pass

    @staticmethod
    def is_locked() -> bool:
        try:
            stl = StockLock.objects.get(id=1)
            return stl.locked
        except StockLock.DoesNotExist:
            StockLock.objects.create(id=1, locked=False)
            return False

    @staticmethod
    def is_unlocked() -> bool:
        return not StockLock.is_locked()

    @staticmethod
    def lock(user: User):
        raiseif(not user or not isinstance(user, User), TypeError, "Expected a user")
        try:
            sl = StockLock.objects.get(id=1)
            sl.locked = True
            sl.save()
        except StockLock.DoesNotExist:
            StockLock.objects.create(id=1, locked=True)

        StockLockLog.objects.create(locked=True, user=user)

    @staticmethod
    def unlock(user: User):
        raiseif(not user or not isinstance(user, User), TypeError, "Expected a user")
        try:
            sl = StockLock.objects.get(id=1)
            sl.locked = False
            sl.save()
        except StockLock.DoesNotExist:
            StockLock.objects.create(id=1, locked=False)

        StockLockLog.objects.create(locked=False, user=user)


class StockLockLog(models.Model):
    """
    A log of the state of the stock with user
    """

    locked = models.BooleanField()

    user = models.ForeignKey(User)


class LockError(Exception):
    pass
