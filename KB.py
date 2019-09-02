from axioms import *
from concept import *
from SymbolTable import *


class KnowledgeBase(object):
    """
        Defines the KB.
    """
    def __init__(self):
        self.tbox = TBox()
        self.symbol_table = SymbolTable()

    def __axiom_adder(self, axiom):
        """
            Adds axiom to appropriate box.
        """
        self.tbox.add_axiom(axiom)

    def add_axioms(self, axiom_list):
        for axiom in axiom_list:
            self.__axiom_adder(axiom)

    def contains(self, axiom):
        """
            returns whether the KB contains the given axiom.
        """
        return self.tbox.contains(axiom)

    def normalization(self):
        """
            The normalisation procedure
        """
        print("Normalization:")
        while True:
            tag = True
            for axiom in list(self.tbox):
                if axiom.type is "COMPLEX_CONCEPT":
                    if axiom.axiom_type is "EQUIVALENT":
                        """ NF1: C ≡ D -> C ⊆ D, D ⊆ C """
                        tag = False
                        A, B = axiom.A, axiom.B
                        self.tbox.remove(axiom)
                        self.tbox.add_axioms([Inclusion(A, B), Inclusion(B, A)])
                    elif axiom.axiom_type is "INCLUSION" and axiom.A.type is "COMPLEX_CONCEPT" \
                            and axiom.B.type is "COMPLEX_CONCEPT":
                        # NF2: C ⊆ D -> C ⊆ A, A ⊆ D
                        tag = False
                        A, B = axiom.A, axiom.B
                        C = AtomicConcept(SymbolTable().get_fresh_symbol())
                        self.tbox.remove(axiom)
                        self.tbox.add_axioms([Inclusion(A, C), Inclusion(C, B)])
                    elif axiom.axiom_type is "INCLUSION" and axiom.A.type is "COMPLEX_CONCEPT" \
                            and axiom.A.axiom_type is "EXISTENCE" and axiom.A.B.type is "COMPLEX_CONCEPT":
                        # NF3: ∃r.C ⊆ D -> C ⊆ A, ∃r.A ⊆ D
                        R, C, D = axiom.A.A, axiom.A.B, axiom.B
                        A = AtomicConcept(SymbolTable().get_fresh_symbol())
                        self.tbox.remove(axiom)
                        self.tbox.add_axioms([Inclusion(C, A), Inclusion(Existence(R, A), D)])
                        tag = False
                    elif axiom.axiom_type is "INCLUSION" and axiom.A.type is "COMPLEX_CONCEPT" \
                            and axiom.A.axiom_type is "CONJUNCTION" and axiom.A.A.type is "COMPLEX_CONCEPT":
                        # NF4: C ∩ D ⊆ E -> C ⊆ A, A ∩ D ⊆ E
                        A1, A2, B = axiom.A.A, axiom.A.B, axiom.B
                        C = AtomicConcept(SymbolTable().get_fresh_symbol())
                        self.tbox.remove(axiom)
                        self.tbox.add_axioms([Inclusion(A1, C), Inclusion(Conjunction(C, A2), B)])
                        tag = False
                    elif axiom.axiom_type is "INCLUSION" and axiom.B.type is "COMPLEX_CONCEPT" \
                            and axiom.B.axiom_type is "EXISTENCE" and axiom.B.B.type is "COMPLEX_CONCEPT":
                        # NF5: B ⊆ ∃r.C -> C ⊆ A, B ⊆ ∃r.A
                        B, R, C = axiom.A, axiom.B.A, axiom.B.B
                        A = AtomicConcept(SymbolTable().get_fresh_symbol())
                        self.tbox.remove(axiom)
                        self.tbox.add_axioms([Inclusion(C, A), Inclusion(B, Existence(R, A))])
                        tag = False
                    elif axiom.axiom_type is "INCLUSION" and axiom.B.type is "COMPLEX_CONCEPT" \
                            and axiom.B.axiom_type is "CONJUNCTION":
                        """ NF6: B ⊆ C ∩ D -> B ⊆ C, B ⊆ D """
                        tag = False
                        A, B1, B2 = axiom.A, axiom.B.A, axiom.B.B
                        self.tbox.remove(axiom)
                        self.tbox.add_axioms([Inclusion(A, B1), Inclusion(A, B2)])
            if tag:
                break

    def reasoner(self, inclusion_axiom):
        print("Reasoning:")
        left, right = inclusion_axiom.A, inclusion_axiom.B
        sym_list = list(SymbolTable().sym_list)
        # initial S() and R() for all symbol
        S = {}
        R = [[[] for i in sym_list] for j in sym_list]
        for s in sym_list:
            S[s] = [TopConcept().name, s]
        for axiom in self.tbox:
            if axiom.type is "COMPLEX_CONCEPT" and axiom.axiom_type is "INCLUSION" and not axiom.B.type is "COMPLEX_CONCEPT":
                if S.get(axiom.A.name) is not None:
                    S[axiom.A.name].append(axiom.B.name)
                else:
                    S[axiom.A.name] = [TopConcept().name, axiom.A.name, axiom.B.name]
            elif axiom.type is "COMPLEX_CONCEPT" and axiom.axiom_type is "INCLUSION" \
                    and axiom.B.type is "COMPLEX_CONCEPT" and axiom.B.axiom_type is "EXISTENCE":
                i, j = sym_list.index(axiom.A.name), sym_list.index(axiom.B.B.name)
                R[i][j].append(axiom.B.A.name)
                R[j][i].append(axiom.B.A.name)
        for _ in range(3):
            # Rule1
            for k in S.keys():
                for axiom in self.tbox:
                    if axiom.type is "COMPLEX_CONCEPT" and axiom.axiom_type is "INCLUSION" \
                            and axiom.A.type is "COMPLEX_CONCEPT" and axiom.A.axiom_type is "CONJUNCTION":
                        if S[k].__contains__(axiom.A.A.name) and S[k].__contains__(axiom.A.B.name) \
                                and not S[k].__contains__(axiom.B.name):
                            S[k].append(axiom.B.name)
            # Rule2
            for k in sym_list:
                for axiom in self.tbox:
                    if axiom.type is "COMPLEX_CONCEPT" and axiom.axiom_type is "INCLUSION" \
                            and axiom.B.type is "COMPLEX_CONCEPT" and axiom.B.axiom_type is "EXISTENCE":
                        i, j = sym_list.index(axiom.A.name), sym_list.index(axiom.B.B.name)
                        if not len(R[i][j]) == 0 and S[k].__contains__(sym_list) \
                                and not R[sym_list.index(k)][j].__contains__(axiom.B.A.name):
                            R[sym_list.index(k)][j].append(axiom.B.A.name)
                            R[j][sym_list.index(k)].append(axiom.B.A.name)
            # Rule3
            for k in sym_list:
                for axiom in self.tbox:
                    if axiom.type is "COMPLEX_CONCEPT" and axiom.axiom_type is "INCLUSION" \
                            and axiom.B.type is "COMPLEX_CONCEPT" and axiom.B.axiom_type is "EXISTENCE" and k == axiom.A.name:
                        r, Y = axiom.B.A.name, axiom.B.B.name
                        for A in S[Y]:
                            for axiom in self.tbox:
                                if axiom.type is "COMPLEX_CONCEPT" and axiom.axiom_type is "INCLUSION" \
                                        and axiom.A.type is "COMPLEX_CONCEPT" and axiom.A.axiom_type is "EXISTENCE" \
                                        and A == axiom.A.B.name and r == axiom.A.A.name:
                                    B = axiom.B.name
                                    if not S[k].__contains__(B):
                                        S[k].append(B)
        if S[left.name].__contains__(right.name):
            print(str(inclusion_axiom) + " establish ")
        else:
            print(str(inclusion_axiom) + " not establish ")
        print(left.name+"'s inclusion set: "+ str(S[left.name]))

    def print_kb(self):
        print("KB {" + self.tbox.__str__() + "}")
