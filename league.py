from identified_object import IdentifiedObject


class League(IdentifiedObject):

    @property
    def name(self):
        return self.league_name

    @property  # read only
    def teams(self):
        return self.list_of_teams

    @property
    def competitions(self):  # read only
        return self.list_of_games

    def __init__(self, oid, name):
        super().__init__(oid)
        self.league_name = name
        self.list_of_teams = []
        self.list_of_games = []

    def add_team(self, team):
        if team not in self.teams:
            self.teams.append(team)

    def remove_team(self, team):
        if team in self.teams:
            self.teams.remove(team)
        else:
            pass

    def team_named(self, s):
        i = 0
        while i < len(self.teams):
            if self.teams[i].team_name == s:
                return self.teams[i]
            i += 1
        return None

    def add_competition(self, competition):
        self.list_of_games.append(competition)

    def teams_for_member(self, member):
        player_teams = []
        for team in self.teams:
            if member in team.members:
                player_teams.append(team)
        return player_teams

    def competitions_for_team(self, team):  # this doesn't like self.competitions because it isn't iterable.
        # try list comprehension?
        # angry about __str__ and __eq__ but don't know why yet
        # try comparing team objects rather than names since names don't have oid
        team_games = []
        for competition in self.competitions:
            if team in competition.teams_competing:
                team_games.append(competition)
        return team_games

    def competitions_for_member(self, member):  # clean before submitting
        # this is getting convoluted
        # break into smaller pieces
        # get all teams member plays on
        # get all competitions teams play in
        # i = 0
        # player_games = []
        # player_teams = self.teams_for_member(member)  # get all teams member plays on
        # for team in player_teams:
        #     if any(self.competitions_for_team(team)) in self.competitions:
        #         player_games.append(self.competitions[i])
        #         i += 1
        # return [competition for competition in self.competitions if (any(player_teams) in competition.teams_competing)]
        # team_games = [team for team in player_teams if team in self.competitions_for_team(team)]
        # player_games = []
        # for game in team_games:
        #     player_games.append(game)
        # list of teams for which the member plays
        # for each team in the teams that are competing
        # player_games = [competition for competition in self.competitions if
        #                 (team in player_teams for team in competition.teams_competing)]
        # for competition in self.competitions:
        #     if member in player_teams and player_teams in self.competitions:
        #         player_games.append(member)

        player_teams = self.teams_for_member(member)  # get all teams member plays on
        player_games = [competition for competition in self.competitions  # gets all competitions
                        if any(team in player_teams for team in competition.teams_competing)]  # if any team is in the
        return player_games

    def __str__(self):
        num_of_teams = len(self.teams)
        num_of_games = len(self.competitions)
        return f"{self.name}: {num_of_teams} teams, {num_of_games} competitions"
