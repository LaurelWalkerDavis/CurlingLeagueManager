import unittest
import datetime
import unittest
from fake_emailer import FakeEmailer
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


class CompetitionTests(unittest.TestCase):
    def test_create(self):
        now = datetime.datetime.now()
        t1 = Team(1, "Team 1")
        t2 = Team(2, "Team 2")
        t3 = Team(3, "Team 3")
        c1 = Competition(1, [t1, t2], "Here", None)
        c2 = Competition(2, [t2, t3], "There", now)

        self.assertEqual("Here", c1.location)
        self.assertEqual(1, c1.oid)
        self.assertIsNone(c1.date_time)
        self.assertEqual(2, len(c1.teams_competing))
        self.assertIn(t1, c1.teams_competing)
        self.assertIn(t2, c1.teams_competing)
        self.assertNotIn(t3, c1.teams_competing)

        self.assertEqual("There", c2.location)
        self.assertEqual(2, c2.oid)
        self.assertEqual(now, c2.date_time)
        self.assertEqual(2, len(c2.teams_competing))
        self.assertNotIn(t1, c2.teams_competing)
        self.assertIn(t2, c2.teams_competing)
        self.assertIn(t3, c2.teams_competing)


if __name__ == '__main__':
    unittest.main()
