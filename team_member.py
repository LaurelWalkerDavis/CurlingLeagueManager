from identified_object import IdentifiedObject
from fake_emailer import FakeEmailer


class TeamMember(IdentifiedObject):
    """Describes a member of a team. Inherits from IdentifiedObject."""

    @property  # M3-50 page 10.
    def name(self):
        return self._name

    @property
    def email(self):
        return self._email

    def __init__(self, oid, name, email):
        """
        Creates a TeamMember object. Uses the __init__ provided by IdentifiedObject,
        but overrides it with two new fields.
        :param oid: the object ID
        :param name: the name of the team member
        :param email: the email address of the team member
        """
        super().__init__(oid)  # have to use what's provided by the method in IdentifiedObject
        self._name = name
        self._email = email

    def send_email(self, emailer, subject, message):
        emailer.send_plain_email([self.email], subject, message)  # okay, so the email recipients have to be
        # a collection of email addresses

    def __str__(self):
        return f"{self.name}<{self.email}>"
