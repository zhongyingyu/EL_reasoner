from KB import *
from concept import *


if __name__ == '__main__':
    concept1 = Inclusion(AtomicConcept("A"), Conjunction(AtomicConcept("B"), Existence(Role("r"), AtomicConcept("C"))))
    concept2 = Inclusion(AtomicConcept("C"), Existence(Role("s"), AtomicConcept("D")))
    concept3 = Inclusion(
        Conjunction(Existence(Role("r"), Existence(Role("s"), TopConcept())), AtomicConcept("B")),
        AtomicConcept("D"))
    KB = KnowledgeBase()
    KB.add_axioms([concept1, concept2, concept3])
    KB.print_kb()
    KB.normalization()
    KB.print_kb()
    KB.reasoner(Inclusion(AtomicConcept("A"), AtomicConcept("D")))
