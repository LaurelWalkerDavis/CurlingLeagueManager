from identified_object import IdentifiedObject

class Competition(IdentifiedObject):
    """Describes a competition between teams. Inherits from IdentifiedObject."""

    @property
    def teams_competing(self):  # must be read only
        return self._teams

    @teams_competing.setter
    def teams_competing(self, team_list):
        self.teams_competing.Add(team_list)

    @property
    def date_time(self):
        return self._datetime

    @property
    def location(self):
        return self._location

    def __init__(self, oid, teams, location, datetime):
        super().__init__(oid)
        self._teams = teams
        self._location = location
        self._datetime = datetime

    def send_email(self, emailer, subject, message):
        team1 = self.teams_competing[0].members
        team2 = self.teams_competing[1].members
        participants = list(set(team1 + team2))
        email_list = []
        for player in participants:
            email_list.append(player.email)
        emailer.send_plain_email(email_list, subject, message)

    def __str__(self):
        num_of_teams = self.teams_competing.Length
        if self.date_time is None:
            return f"Competition at {self.location} with {num_of_teams} teams"
        else:
            return f"Competition at {self.location} on {self.date_time} with {num_of_teams} teams"
