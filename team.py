from identified_object import IdentifiedObject


class Team(IdentifiedObject):
    """Describes a team composed of TeamMember objects. Inherits from IdentifiedObject."""

    @property
    def name(self):
        return self.team_name

    @property
    def members(self):  # must be read only
        return self.memberList  # list of TeamMember objects

    def __init__(self, oid, name):
        super().__init__(oid)
        self.team_name = name
        self.memberList = []

    def add_member(self, member):
        if member not in self.memberList:
            self.memberList.append(member)

    def member_named(self, s):
        i = 0
        while i < len(self.memberList):
            if self.memberList[i].name == s:
                return self.memberList[i]
            i += 1
        return None

    def remove_member(self, member):
        if member in self.memberList:
            self.memberList.remove(member)

    def send_email(self, emailer, subject, message):
        email_list = []
        for member in self.members:
            if member.email is not None:
                email_list.append(member.email)
        emailer.send_plain_email(email_list, subject, message)

    def __str__(self):
        team_name = self.name
        num_of_players = len(self.members)
        return f"{team_name}: {num_of_players} members"

        # name_list = []
        # for member in self.members:
        #     if member.name is not None:
        #         name_list.append(member.name)
        # name_string = ""
        # for name in name_list:
        #     name_string += "\n" + name
        # return f"{self.name.title()}:{name_string}"




