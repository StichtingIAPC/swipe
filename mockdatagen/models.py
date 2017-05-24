import queue

from copy import deepcopy
from django.db import models

# Create your models here.
from money.models import Currency, CurrencyData
requires = {}
requiredBy = {}
functions = {}


def register(cls):
    model = cls.model
    func = cls.func
    requirements = cls.requirements
    if not requiredBy.get(model):
        requiredBy[model] = []
    requires[model] = requirements
    functions[model] = func
    for req in requirements:
        if not requiredBy.get(req):
            requiredBy[req] = []
        requiredBy[req].append(model)
    return cls





def do_in_order(func):
    req = deepcopy(requires)
    reqb = deepcopy(requiredBy)
    q = queue.Queue()
    for key, value in req.items():
        if not value:
            q.put(key)
    while not q.empty():
        a = q.get()
        func(a)
        r = reqb[a]
        for rr in r:
            req[rr].remove(a)
            if not req[rr]:
                q.put(rr)


def execute(model):
    functions[model](model)
