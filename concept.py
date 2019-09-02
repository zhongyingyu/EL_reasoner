from SymbolTable import *


class Concept(object):
    """
        base class of Concept
    """
    def __init__(self, concept_type):
        self.type = concept_type


class Role(Concept):
    """
        atomic concept
    """
    def __init__(self, name):
        super().__init__("ROLE")
        self.name = name

    def __str__(self):
        return str(self.name)


class AtomicConcept(Concept):
    """
        atomic concept
    """
    def __init__(self, name):
        super().__init__("ATOMIC_CONCEPT")
        self.name = name
        SymbolTable().add_to_table(self.name)

    def __str__(self):
        return str(self.name)


class TopConcept(Concept):
    """
        Top concept
    """
    def __init__(self):
        super().__init__("TOP")
        self.name = "┬"

    def __str__(self):
        return str(self.name)


class Conjunction(Concept):
    """
        concept contain conjunction
    """
    def __init__(self, concept1, concept2):
        super().__init__("COMPLEX_CONCEPT")
        self.A = concept1
        self.B = concept2
        self.axiom_type = "CONJUNCTION"
        self.name = str(self.A) + " ∩ " + str(self.B)

    def __str__(self):
        return str(self.name)


class Equivalent(Concept):
    """
        concept contain equivalent
    """

    def __init__(self, concept1, concept2):
        super().__init__("COMPLEX_CONCEPT")
        self.A = concept1
        self.B = concept2
        self.axiom_type = "EQUIVALENT"
        self.name = str(self.A) + " ≡ " + str(self.B)

    def __str__(self):
        return str(self.name)


class Existence(Concept):
    """
        concept contain existence restriction
    """

    def __init__(self, concept1, concept2):
        super().__init__("COMPLEX_CONCEPT")
        self.A = concept1
        self.B = concept2
        self.axiom_type = "EXISTENCE"
        self.name = "∃" + str(self.A) + "." + str(self.B)

    def __str__(self):
        return str(self.name)


class Inclusion(Concept):
    """
        concept contain inclusion
    """

    def __init__(self, concept1, concept2):
        super().__init__("COMPLEX_CONCEPT")
        self.A = concept1
        self.B = concept2
        self.axiom_type = "INCLUSION"
        self.name = str(self.A) + " ⊆ " + str(self.B)

    def __str__(self):
        return str(self.name)
