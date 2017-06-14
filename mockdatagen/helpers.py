import queue

from copy import deepcopy


class MockGen:
    _instance = None
    requires = {}
    requiredBy = {}
    functions = {}

    @classmethod
    def register(cls, to_register):
        inst = MockGen.get_instance()

        model = to_register.model
        func = to_register.func
        requirements = to_register.requirements
        if not inst.requiredBy.get(model):
            inst.requiredBy[model] = []
        inst.requires[model] = requirements
        inst.functions[model] = func
        for req in requirements:
            if not inst.requiredBy.get(req):
                inst.requiredBy[req] = []
            inst.requiredBy[req].append(model)
        return to_register

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = MockGen()
        return cls._instance

    def do_in_order(self, func):
        req = deepcopy(self.requires)
        reqb = deepcopy(self.requiredBy)
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

    def execute(self, model):
        if not type(model) is str:
            print(model.__name__)
            model.objects.all().delete()
        self.functions[model]()
        if not type(model) is str:
            print(model.objects.all())
