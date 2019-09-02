class TBox(set):
    """
        TBox.
    """
    def __init__(self, obj=None):
        if obj:
            super().__init__(obj)

    def add_axiom(self, axiom):
        """
            Add a single axiom.
        """
        if axiom not in self:
            self.add(axiom)

    def add_axioms(self, axiom_list):
        """
            Add multiple axioms.
        """
        for axiom in axiom_list:
            self.add_axiom(axiom)

    def pop_axiom(self):
        """
            Remove and return an axiom from the TBOX.
        """
        if len(self):
            return self.pop()
        else:
            return None

    def contains(self, axiom):
        """
            Checks if the TBOX contains the given axiom.
        """
        return axiom in self

    def __str__(self):
        str = "TBOX ["
        for a in self:
            str += a.__str__() + ", "
        str = str[:-2]
        str += "]"
        return str
