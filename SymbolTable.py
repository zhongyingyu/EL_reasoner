import string
import random


def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class SymbolTable(object):
    sym_list = set()

    def add_to_table(self, s):
        self.sym_list.add(s)

    def get_fresh_symbol(self):
        while True:
            s = string.ascii_uppercase
            r = random.choice(s)
            if not len(self.sym_list) == 24:
                if not self.sym_list.__contains__(r):
                    break
            else:
                r = r + str(random.randint())
                if not self.sym_list.__contains__(r):
                    break
        return r