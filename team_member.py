from identified_object import IdentifiedObject

class TeamMember(IdentifiedObject):
    """Describes a member of a team. Inherits from IdentifiedObject."""

    def name(self):
        pass

    def email(self):
        pass

    def __init__(self, oid, name, email):
        super().__init__(oid)
        self._name = name
        self._email = email

    def send_email(self, emailer, subject, message):
        pass

    def __str__(self):
        pass
