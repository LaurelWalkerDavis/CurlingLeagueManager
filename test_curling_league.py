import datetime
import unittest
from fake_emailer import FakeEmailer
from league import League
from team_member import TeamMember
from competition import Competition
from team import Team


class TeamMemberTests(unittest.TestCase):
    def test_create(self):
        oid = 1
        name = "Fred"
        email = "fred.flintstone@gmail.com"
        tm = TeamMember(oid, name, email)
        self.assertEqual(oid, tm.oid)
        self.assertEqual(name, tm.name)
        self.assertEqual(email, tm.email)

    def test_name_and_email(self):
        oid = 1
        name = "Fred"
        email = "fred.flintstone@gmail.com"
        tm = TeamMember(oid, name, email)
        self.assertEqual("Fred", tm.name)
        self.assertEqual("fred.flintstone@gmail.com", tm.email)

    def test_equality_based_on_id(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(1, "other name", "other email")
        tm_3 = TeamMember(2, "name", "email")

        # team members must be equal to themselves
        self.assertTrue(tm_1 == tm_1)
        self.assertTrue(tm_2 == tm_2)
        self.assertTrue(tm_3 == tm_3)

        # same id are equal, even if other fields different
        self.assertTrue(tm_1 == tm_2)

        # different ids are not equal, even if other fields the same
        self.assertTrue(tm_1 != tm_3)

    def test_hash_based_on_id(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(1, "other name", "other email")
        tm_3 = TeamMember(2, "name", "email")

        # hash depends only on id
        self.assertTrue(hash(tm_1) == hash(tm_2))

        # objects with different id's may have different hash codes
        # note: this is not a requirement of the hash function but
        # for the case of id == 1 and id == 2 we can verify that their
        # hash codes are different in a REPL (just print(hash(1)) etc).
        self.assertTrue(hash(tm_1) != hash(tm_3))

    def test_str(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(1, "other name", "other email")
        self.assertEqual("name<email>", str(tm_1))
        self.assertEqual("other name<other email>", str(tm_2))

    def test_sends_email(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(1, "other name", "other email")
        fe = FakeEmailer()
        tm_1.send_email(fe, "Foo", "Bar")
        self.assertEqual(["email"], fe.recipients)
        self.assertEqual("Foo", fe.subject)
        self.assertEqual("Bar", fe.message)
        tm_2.send_email(fe, "Different", "Ugh")
        self.assertEqual(["other email"], fe.recipients)
        self.assertEqual("Different", fe.subject)
        self.assertEqual("Ugh", fe.message)


class TeamTests(unittest.TestCase):

    def test_create(self):
        name = "Curl Jam"
        oid = 10
        t = Team(oid, name)
        self.assertEqual(name, t.name)
        self.assertEqual(oid, t.oid)

    def test_name_and_members(self):
        name = "Curl Jam"
        oid = 10
        t = Team(oid, name)
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        t.add_member(tm1)
        t.add_member(tm2)
        self.assertEqual("Curl Jam", t.name)
        self.assertEqual([tm1, tm2], t.members)

    def test_adding_adds_to_members(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        t.add_member(tm1)
        self.assertIn(tm1, t.members)
        self.assertNotIn(tm2, t.members)
        t.add_member(tm2)
        self.assertIn(tm1, t.members)
        self.assertIn(tm2, t.members)

    def test_removing_removes_from_members(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f")
        tm2 = TeamMember(6, "g", "g")
        t.add_member(tm1)
        t.add_member(tm2)
        t.remove_member(tm1)
        self.assertNotIn(tm1, t.members)
        self.assertIn(tm2, t.members)

    def test_member_named(self):
        t = Team(1, "Flintstones")
        t.add_member(TeamMember(2, "Fred", "fred@bedrock"))
        t.add_member(TeamMember(3, "Barney", "barney@bedrock"))
        t.add_member(TeamMember(4, "Wilma", "wima@bedrock"))
        self.assertEqual(t.members[0], t.member_named("Fred"))
        self.assertEqual(t.members[2], t.member_named("Wilma"))
        self.assertEqual(t.members[1], t.member_named("Barney"))
        self.assertIsNone(t.member_named("fred"))

    def test_str(self):
        t = Team(1, "Flintstones")
        t.add_member(TeamMember(2, "Fred", "fred@bedrock"))
        t.add_member(TeamMember(3, "Barney", "barney@bedrock"))
        t.add_member(TeamMember(4, "Wilma", "wima@bedrock"))
        self.assertEqual("Flintstones: 3 members", t.__str__())

    def test_sends_email(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f@foo.com")
        tm2 = TeamMember(6, "g", "g@bar.com")
        t.add_member(tm1)
        t.add_member(tm2)
        fe = FakeEmailer()
        t.send_email(fe, "S", "M")
        self.assertIn("f@foo.com", fe.recipients)
        self.assertIn("g@bar.com", fe.recipients)
        self.assertEqual(2, len(fe.recipients))
        self.assertEqual("S", fe.subject)
        self.assertEqual("M", fe.message)

    def test__str__(self):
        t = Team(1, "Flintstones")
        tm1 = TeamMember(5, "f", "f@foo.com")
        tm2 = TeamMember(6, "g", "g@bar.com")
        t.add_member(tm1)
        t.add_member(tm2)
        self.assertEqual("Flintstones: 2 members", t.__str__())


class CompetitionTests(unittest.TestCase):
    def test_create(self):
        now = datetime.datetime.now()
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        # __init__
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t2, t3], "There", now)
        # oid
        self.assertEqual(1, c1.oid)
        self.assertEqual(2, c2.oid)
        # location
        self.assertEqual("There", c2.location)
        self.assertEqual("Here", c1.location)
        # date_time
        self.assertIsNone(c1.date_time)
        self.assertEqual(now, c2.date_time)
        # teams_competing
        self.assertEqual(2, len(c2.teams_competing))
        self.assertNotIn(t1, c2.teams_competing)
        self.assertIn(t2, c2.teams_competing)
        self.assertIn(t3, c2.teams_competing)
        self.assertEqual(2, len(c1.teams_competing))
        self.assertIn(t1, c1.teams_competing)
        self.assertIn(t2, c1.teams_competing)
        self.assertNotIn(t3, c1.teams_competing)

    def test_send_email(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(2, "other name", "other email")
        tm_3 = TeamMember(3, "Buggs", "carrot@gmail")
        tm_4 = TeamMember(4, "Bunny", "radish@hotmail")
        now = datetime.datetime.now()
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        t1.add_member(tm_1)
        t1.add_member(tm_2)
        t2.add_member(tm_3)
        t2.add_member(tm_4)
        t3.add_member(tm_1)
        t3.add_member(tm_1)  # duplicate check
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t2, t3], "There", now)
        fe = FakeEmailer()
        # Competition1
        c1.send_email(fe, "Tournament", "Gear up!")
        self.assertEqual(['email', 'other email', 'carrot@gmail', 'radish@hotmail'], fe.recipients)
        self.assertEqual("Tournament", fe.subject)
        self.assertEqual("Gear up!", fe.message)
        # Competition2
        c2.send_email(fe, "Winner", "Congrats Cardinals!")
        self.assertEqual(['email', 'carrot@gmail', 'radish@hotmail'], fe.recipients)
        self.assertEqual("Winner", fe.subject)
        self.assertEqual("Congrats Cardinals!", fe.message)

    def test__str__(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(2, "other name", "other email")
        tm_3 = TeamMember(3, "Buggs", "carrot@gmail")
        tm_4 = TeamMember(4, "Bunny", "radish@hotmail")
        now = datetime.datetime.now()
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        t1.add_member(tm_1)
        t1.add_member(tm_2)
        t2.add_member(tm_3)
        t2.add_member(tm_4)
        t3.add_member(tm_1)
        t3.add_member(tm_1)  # duplicate check
        c1 = Competition(1, [t1, t2], "O'Malley Field", None)
        c2 = Competition(2, [t2, t3], "SuperDome", now)
        self.assertEqual("Competition at O'Malley Field with 2 teams", c1.__str__())
        self.assertEqual(f"Competition at SuperDome on {now} with 2 teams", c2.__str__())


class LeagueTests(unittest.TestCase):
    def test_create(self):
        league = League(1, "AL State Curling League")
        self.assertEqual(1, league.oid)
        self.assertEqual("AL State Curling League", league.name)
        self.assertEqual([], league.teams)
        self.assertEqual([], league.competitions)

    def test_adding_team_adds_to_teams(self):
        t = Team(1, "Ice Maniacs")
        league = League(1, "AL State Curling League")
        self.assertNotIn(t, league.teams)
        league.add_team(t)
        self.assertIn(t, league.teams)

    def test_adding_competition_adds_to_competitions(self):
        c = Competition(1, [], "Local tourney", None)
        league = League(13, "AL State Curling League")
        self.assertNotIn(c, league.competitions)
        league.add_competition(c)
        self.assertIn(c, league.competitions)

    def test__str__(self):
        league = self.build_league()
        self.assertEqual(f"Some league: 3 teams, {len(league.competitions)} competitions", league.__str__())

    @staticmethod
    def build_league():
        league = League(1, "Some league")
        t1 = Team(1, "t1")
        t2 = Team(2, "t2")
        t3 = Team(3, "t3")
        all_teams = [t1, t2, t3]
        league.add_team(t1)
        league.add_team(t2)
        league.add_team(t3)
        tm1 = TeamMember(1, "Fred", "fred")
        tm2 = TeamMember(2, "Barney", "barney")
        tm3 = TeamMember(3, "Wilma", "wilma")
        tm4 = TeamMember(4, "Betty", "betty")
        tm5 = TeamMember(5, "Pebbles", "pebbles")
        tm6 = TeamMember(6, "Bamm-Bamm", "bam-bam")
        tm7 = TeamMember(7, "Dino", "dino")
        tm8 = TeamMember(8, "Mr. Slate", "mrslate")
        t1.add_member(tm1)
        t1.add_member(tm2)
        t2.add_member(tm3)
        t2.add_member(tm4)
        t2.add_member(tm5)
        t3.add_member(tm6)
        t3.add_member(tm7)
        t3.add_member(tm8)
        # every team plays every other team twice
        oid = 1
        for c in [Competition(oid := oid + 1, [team1, team2], team1.name + " vs " + team2.name, None)
                  for team1 in all_teams
                  for team2 in all_teams
                  if team1 != team2]:
            league.add_competition(c)
        return league

    def test_team_named(self):
        league = self.build_league()
        t = league.team_named("t1")
        self.assertEqual(league.teams[0], t)
        t = league.team_named("t3")
        self.assertEqual(league.teams[2], t)
        t = league.team_named("bogus")
        self.assertIsNone(t)

    def test_big_league(self):
        league = self.build_league()
        t = league.teams[0]
        cs = league.competitions_for_team(t)
        # matchups are (t1, t2), (t1, t3), (t2, t1), (t3, t1) but we don't know what order they will be returned in
        # so use sets.
        cs_names = {c.location for c in cs}  # set comprehension
        self.assertEqual({"t1 vs t2", "t1 vs t3", "t2 vs t1", "t3 vs t1"}, cs_names)
        dummy = league.teams_for_member(league.teams[2].members[0])
        self.assertEqual([league.teams[2]], league.teams_for_member(league.teams[2].members[0]))

        # Grab a player from the third team
        cs = league.competitions_for_member(league.teams[2].members[0])
        # matchups are (t3, t1), (t3, t2), (t2, t3), (t1, t3) but we don't know what order they will be returned in
        # so use sets.
        cs_names = {c.location for c in cs}  # set comprehension
        self.assertEqual({"t3 vs t1", "t3 vs t2", "t2 vs t3", "t1 vs t3"}, cs_names)

    def test_teams(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(2, "other name", "other email")
        tm_3 = TeamMember(3, "Buggs", "carrot@gmail")
        tm_4 = TeamMember(4, "Bunny", "radish@hotmail")
        team1 = Team(1, "Team 1")
        team2 = Team(2, "Team 2")
        team3 = Team(3, "Team 3")
        team1.add_member(tm_1)
        team1.add_member(tm_2)
        team2.add_member(tm_3)
        team2.add_member(tm_4)
        team3.add_member(tm_1)
        team3.add_member(tm_1)  # duplicate check
        team3.add_member(tm_3)
        now = datetime.datetime.now()
        c1 = Competition(1, [team1, team2], "Here", None)
        c2 = Competition(2, [team2, team3], "There", now)
        #__init__
        league1 = League(1, "Major League")
        league2 = League(2, "Minor League")
        # name
        self.assertEqual("Major League", league1.name)
        self.assertEqual("Minor League", league2.name)
        # teams
        self.assertEqual([], league1.teams)
        self.assertEqual([], league2.teams)
        league1.add_team(team1)
        league2.add_team(team2)
        league2.add_team(team3)
        self.assertEqual([team1], league1.teams)
        self.assertEqual([team2, team3], league2.teams)
        # teams_for_member(member)
        self.assertEqual([team1], league1.teams_for_member(tm_1))
        self.assertEqual([team2, team3], league2.teams_for_member(tm_3))

    def test_add_and_remove(self):
        tm_1 = TeamMember(1, "name", "email")
        tm_2 = TeamMember(2, "other name", "other email")
        tm_3 = TeamMember(3, "Buggs", "carrot@gmail")
        tm_4 = TeamMember(4, "Bunny", "radish@hotmail")
        team1 = Team(1, "Team 1")
        team2 = Team(2, "Team 2")
        team3 = Team(3, "Team 3")
        team1.add_member(tm_1)
        team1.add_member(tm_2)
        team2.add_member(tm_3)
        team2.add_member(tm_4)
        team3.add_member(tm_1)
        team3.add_member(tm_1)  # duplicate check
        now = datetime.datetime.now()
        c1 = Competition(1, [team1, team2], "Here", None)
        c2 = Competition(2, [team2, team3], "There", now)
        league1 = League(1, "Major League")
        league2 = League(2, "Minor League")
        league1.add_team(team1)
        league2.add_team(team2)
        league2.add_team(team3)

        # competitions
        self.assertEqual([], league1.competitions)
        self.assertEqual([], league2.competitions)
        # add_competitions
        league1.add_competition(c1)
        league2.add_competition(c1)
        league2.add_competition(c2)
        self.assertEqual([c1], league1.competitions)
        self.assertEqual([c1, c2], league2.competitions)
        # add_team
        league1.add_team(team2)
        self.assertEqual([team1, team2], league1.teams)
        # remove_team
        league1.remove_team(team2)
        self.assertEqual([team1], league1.teams)
        # teams_named
        self.assertEqual(team1, league1.team_named("Team 1"))
        self.assertEqual(team2, league2.team_named("Team 2"))
        self.assertEqual(team3, league2.team_named("Team 3"))


if __name__ == '__main__':
    unittest.main()
