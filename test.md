# Voorraadmodel


Het voorraadmodel is gebaseerd op drie modellen:
1. Stock
2. StockChange
3. StockChangeSet

Om extra dingen toe te voegen aan de voorraad dient de functie StockChangeSet.construct() gebruikt te worden.
Hierover staat verderop meer beschreven.

## Stock
```
Fields:
article    -- What article type is this stock-line about?
count      -- how many of them are in stock on this line?
book_value -- What's the value of one product on this line?

Fields from StockLabeledLine
labeltype  -- What label type (String) is this Label?
labelkey   -- What number does this label have? (Often: document ID)
```
Stock is verantwoordelijk voor de huidige staat van de voorraad.

Stock heeft een eigen manager; en er kan gezocht worden op label, en labeltype.

Om te sorteren op labeltype moet gesorteerd worden op het labeltype-veld van een Label.

Stock heeft daarnaast een eigen functie Stock.objects.all_without_label(), die alle Stock-regels teruggeeft zonder Label.

## StockChangeSet

De StockChangeSet wordt gebruikt om aan te geven dat bepaalde StockChange's gelijktijdig gebeurd zijn.

### construct()

De Construct-functie  van de StockChangeSet wordt gebruikt om StockChanges aan te maken.
Voorbeeld-implementatie:

```python
eur = Currency("EUR")
usd = Currency("USD")
vat = VAT.objects.create(vatrate=Decimal("1.21"), name="HIGH", active=True)
cost_eur = Cost(amount=Decimal(str(1)), currency=eur)  # 1 euro
art = ArticleType.objects.create(name="P1", vat=vat)
label = MyCustomLabel(1)
# Add 1 article with cost 1 euro
entries = [{
    'article': art,
    'book_value': cost_eur,
    'count': 1,
    'is_in': True,
    'label': label
}]
StockChangeSet.construct(description="ThisIsADescription", entries=entries, enum=1)

```
## StockChange
```
Fields:
article    -- What article type is this stock-line about?
count      -- how many of them are in stock on this line?
book_value -- What's the value of one product on this line?

change_set -- What StockChangeSet is this StockChange a part of?
is_in      -- Is this StockChange an In-line, or an Out-line:
                Out-lines treat positive numbers as having a negative effect on stock


Fields from StockLabeledLine
labeltype  -- What label type (String) is this Label?
labelkey   -- What number does this label have? (Often: document ID)
```

Stock-changes zijn de regels die de veranderingen op de voorraad modelleren.





# StockLabel
Stock-labels zijn zwaar gerelateerd aaan het **[Voorraadmodel](voorraadmodel)**.

StockLabels worden gebruikt om voorraad te reserveren voor een bepaald doel.
De bedoeling is dat de gebruiker zijn eigen StockLabel definieert, als subclass van StockLabel.

Dit behoort als volgt te worden gedaan:

```python
# Example label: Explicit no-label
class ExampleLabel(StockLabel):
    _labeltype="Example"
StockLabel.add_label_type(ExampleLabel)
```

## StockLabeledLine
StockLabeledLine wordt gebruikt als abstractie van modellen die stocklabels kunnen krijgen.


## StockLabel
Dit is de klasse die gebruikt wordt om StockLabels vanuit te creeeren.

Deze klasse is verantwoordelijk voor de functionaliteit van StockLabels, alsmede voor de reverse lookup van subklasses van StockLabel.

Je wilt geen StockLabel maken, maar een eigen subklasse van StockLabel maken, zoals hierboven beschreven. Vervolgens wil je de label registreren, zodat de reverse lookup goed gaat.