class IdentifiedObject:
    """Abstract superclass that is inherited by TeamMember, Team, Competition, and League"""
    # struggling to understand how to make this class abstract. could use @abstractmethod or @classmethod for methods
    # tried using @abstractmethod, but it requires an import that I don't recall discussing. won't compile without it.
    # tried using @classmethod, but it requires that "self" in the arguments be replaced with "cls", which breaks
    # everything

    def __init__(self, oid):
        self._oid = oid

    @property  # M3-50 page 10
    def oid(self):  # this should be read only - see paragraph under IdentifiableObjects?
        return self._oid

    def __eq__(self, other):  # check on whether this will support polymorphism
        return self._oid == other.oid

    def __hash__(self):  # review M3-60, page 7 PDF. Hash has to be consistent with equals.
        return hash(self._oid)

