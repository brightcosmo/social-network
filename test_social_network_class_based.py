from social_network_class_based import *
import datetime
import unittest

make_person_cases = {
    "inputs": [
        [1,"",datetime.date(2000, 1, 1)],
        [1,"hello",datetime.date(2000, 12, 31)],
        [1,"multi Name with capitals",datetime.date(2123, 5, 15)],
        [2,'sample',datetime.date(1905, 5, 5)],
        [54325643,'sample',datetime.date(1905, 5, 5)],
    ],
    "expected":[
        {'friends': [], 'id': 1, 'name': '', 'date_of_birth': datetime.date(2000, 1, 1)},
        {'friends': [], 'id': 1, 'name': 'hello', 'date_of_birth': datetime.date(2000, 12, 31)},
        {'friends': [], 'id': 1, 'name': 'multi Name with capitals', 'date_of_birth': datetime.date(2123, 5, 15)},
        {'friends': [], 'id': 2, 'name': 'sample', 'date_of_birth': datetime.date(1905, 5, 5)},
        {'friends': [], 'id': 54325643, 'name': 'sample', 'date_of_birth': datetime.date(1905, 5, 5)}
    ]
}
fake_friend_str = lambda fake_friend : str(fake_friend["id"])+" ("+fake_friend["name"]+", "+str(fake_friend["date_of_birth"])+") --> "+str(fake_friend["friends"])[1:-1]
make_person_test_case = lambda case : True if str(Person(make_person_cases["inputs"][case][0], make_person_cases["inputs"][case][1], make_person_cases["inputs"][case][2])) == fake_friend_str(make_person_cases["expected"][case]) else f'Expected make_person_cases({make_person_cases["inputs"][case][0], make_person_cases["inputs"][case][1], make_person_cases["inputs"][case][2]})==...\n{fake_friend_str(make_person_cases["expected"][case])}; got \n{str(Person(make_person_cases["inputs"][case][0], make_person_cases["inputs"][case][1], make_person_cases["inputs"][case][2]))}'
class build_friend_Test(unittest.TestCase):
    def testNoName(self):
        R = make_person_test_case(0)
        assert R==True,R

    def testyearEnd(self):
        R = make_person_test_case(1)
        assert R==True,R

    def testLongName(self):
        R = make_person_test_case(2)
        assert R==True,R

    def testHigherID(self):
        R = make_person_test_case(3)
        assert R==True,R

    def testVBigID(self):
        R = make_person_test_case(4)
        assert R==True,R

class build_network_test(unittest.TestCase):
    def testNull(self):
        line = []
        expected = ""
        S = SocialNetwork(line, [])
        assert str(S)==expected, f'str(Expected social_network({line})) == {expected}; got \n{str(S)}'

    def testOnePerson(self):
        line = ['A,2000-01-01']
        expected = "1 (A, 2000-01-01) --> \n"
        observed = SocialNetwork(line, [])
        assert str(observed)==expected, f'str(Expected social_network({line})) == {expected}; got \n{str(observed)}'

    def testManyPeopleNoFriends(self):
        line = ['A,2000-01-01','B,2000-01-02','C,2000-01-03']
        expected = "1 (A, 2000-01-01) --> \n2 (B, 2000-01-02) --> \n3 (C, 2000-01-03) --> \n"
        observed = SocialNetwork(line, [])
        assert str(observed)==expected, f'str(Expected social_network({line})) == {expected}; got \n{str(observed)}'

    def testManyPeopleNoFriendsDupes(self):
        line = ['A,2000-01-01','B,2000-01-02','C,2000-01-03','B,2000-01-02']
        expected = "1 (A, 2000-01-01) --> \n2 (B, 2000-01-02) --> \n3 (C, 2000-01-03) --> \n"
        observed = SocialNetwork(line, [])
        assert str(observed)==expected, f'str(Expected social_network({line})) == {expected}; got \n{str(observed)}'

    def testOnePair(self):
        line = ['A,2000-01-01<->B,2000-01-02']
        expected = "1 (A, 2000-01-01) --> 2\n2 (B, 2000-01-02) --> 1\n"
        observed = SocialNetwork(line, [])
        assert str(observed)==expected, f'str(Expected social_network({line})) == {expected}; got \n{str(observed)}'

    def testOnePairOneSingle(self):
        line = ['A,2000-01-01<->B,2000-01-02','C,2000-01-03']
        expected = "1 (A, 2000-01-01) --> 2\n2 (B, 2000-01-02) --> 1\n3 (C, 2000-01-03) --> \n"
        observed = SocialNetwork(line, [])
        assert str(observed)==expected, f'str(Expected social_network({line})) == {expected}; got \n{str(observed)}'

    def testManyPeopleManyFriends(self):
        line = ['A,2000-01-01<->B,2000-01-02','C,2000-01-03<->D,2000-01-04','E,2000-01-05<->F,2000-01-06','G,2000-01-07<->H,2000-01-08']
        expected = "1 (A, 2000-01-01) --> 2\n2 (B, 2000-01-02) --> 1\n3 (C, 2000-01-03) --> 4\n4 (D, 2000-01-04) --> 3\n5 (E, 2000-01-05) --> 6\n6 (F, 2000-01-06) --> 5\n7 (G, 2000-01-07) --> 8\n8 (H, 2000-01-08) --> 7\n"
        observed = SocialNetwork(line, [])
        assert str(observed)==expected, f'str(Expected social_network({line})) == {expected}; got \n{str(observed)}'

    def testManyPeopleManyFriendsDupes(self):
        line = [
            'A,2000-01-01<->B,2000-01-02',
            'C,2000-01-03<->D,2000-01-04',
            'E,2000-01-05<->F,2000-01-06',
            'G,2000-01-07<->H,2000-01-08',
            'A,2000-01-01<->C,2000-01-03',
            'B,2000-01-02<->D,2000-01-04',
            'B,2000-01-02<->F,2000-01-06',
            'B,2000-01-02<->H,2000-01-08',
        ]
        expected = "1 (A, 2000-01-01) --> 2, 3\n2 (B, 2000-01-02) --> 1, 4, 6, 8\n3 (C, 2000-01-03) --> 4, 1\n4 (D, 2000-01-04) --> 3, 2\n5 (E, 2000-01-05) --> 6\n6 (F, 2000-01-06) --> 5, 2\n7 (G, 2000-01-07) --> 8\n8 (H, 2000-01-08) --> 7, 2\n"
        observed = SocialNetwork(line, [])
        assert str(observed)==expected, f'str(Expected social_network({line})) == {expected}; got \n{str(observed)}'

class test_birthday_posts(unittest.TestCase):
    def testNoFriends(self):
        line = [
            'A,2000-01-01<->B,2000-01-02',
            'C,2000-01-03<->D,2000-01-04',
            'E,2000-01-05<->F,2000-01-06',
            'G,2000-01-07<->H,2000-01-08',
            'A,2000-01-01<->C,2000-01-03',
            'B,2000-01-02<->D,2000-01-04',
            'B,2000-01-02<->F,2000-01-06',
            'B,2000-01-02<->H,2000-01-08',
            'I,2000-01-09'
        ]
        str_network = "1 (A, 2000-01-01) --> 2, 3\n2 (B, 2000-01-02) --> 1, 4, 6, 8\n3 (C, 2000-01-03) --> 4, 1\n4 (D, 2000-01-04) --> 3, 2\n5 (E, 2000-01-05) --> 6\n6 (F, 2000-01-06) --> 5, 2\n7 (G, 2000-01-07) --> 8\n8 (H, 2000-01-08) --> 7, 2\n"
        friend_id = 9
        comparison_date = datetime.date(2022,1,9)
        S = SocialNetwork(line, [])
        S.make_birthday_posts(friend_id,comparison_date)
        expected = []
        assert S.posts == expected, f'with the network of \n{str_network}\n we looked for birthday posts for the friend id: {friend_id} on the date {comparison_date} and expected the posts\n{expected}\n we got\n{S.posts}'

    def testOneFriendNoDay(self):
        line = [
            'A,2000-01-01<->B,2000-01-02',
            'C,2000-01-03<->D,2000-01-04',
            'E,2000-01-05<->F,2000-01-06',
            'G,2000-01-07<->H,2000-01-08',
            'A,2000-01-01<->C,2000-01-03',
            'B,2000-01-02<->D,2000-01-04',
            'B,2000-01-02<->F,2000-01-06',
            'B,2000-01-02<->H,2000-01-08',
        ]
        str_network = "1 (A, 2000-01-01) --> 2, 3\n2 (B, 2000-01-02) --> 1, 4, 6, 8\n3 (C, 2000-01-03) --> 4, 1\n4 (D, 2000-01-04) --> 3, 2\n5 (E, 2000-01-05) --> 6\n6 (F, 2000-01-06) --> 5, 2\n7 (G, 2000-01-07) --> 8\n8 (H, 2000-01-08) --> 7, 2\n"
        friend_id = 5
        comparison_date = datetime.date(2022,12,1)
        S = SocialNetwork(line, [])
        S.make_birthday_posts(friend_id,comparison_date)
        expected = []
        assert S.posts == expected, f'with the network of \n{str_network}\n we looked for birthday posts for the friend id: {friend_id} on the date {comparison_date} and expected the posts\n{expected}\n we got\n{S.posts}'

    def testOneFriendWithDay(self):
        line = [
            'A,2000-01-01<->B,2000-01-02',
            'C,2000-01-03<->D,2000-01-04',
            'E,2000-01-05<->F,2000-01-06',
            'G,2000-01-07<->H,2000-01-08',
            'A,2000-01-01<->C,2000-01-03',
            'B,2000-01-02<->D,2000-01-04',
            'B,2000-01-02<->F,2000-01-06',
            'B,2000-01-02<->H,2000-01-08',
        ]
        str_network = "1 (A, 2000-01-01) --> 2, 3\n2 (B, 2000-01-02) --> 1, 4, 6, 8\n3 (C, 2000-01-03) --> 4, 1\n4 (D, 2000-01-04) --> 3, 2\n5 (E, 2000-01-05) --> 6\n6 (F, 2000-01-06) --> 5, 2\n7 (G, 2000-01-07) --> 8\n8 (H, 2000-01-08) --> 7, 2\n"
        friend_id = 7
        comparison_date = datetime.date(2022,1,1)
        S = SocialNetwork(line, [])
        S.make_birthday_posts(friend_id,comparison_date)
        expected = [('Happy birthday H! Hope you have a good one!', 7, [8])]
        assert S.posts == expected, f'with the network of \n{str_network}\n we looked for birthday posts for the friend id: {friend_id} on the date {comparison_date} and expected the posts\n{expected}\n we got\n{S.posts}'

    def testManyFriendNoDay(self):
        line = [
            'A,2000-01-01<->B,2000-01-02',
            'C,2000-01-03<->D,2000-01-04',
            'E,2000-01-05<->F,2000-01-06',
            'G,2000-01-07<->H,2000-01-08',
            'A,2000-01-01<->C,2000-01-03',
            'B,2000-01-02<->D,2000-01-04',
            'B,2000-01-02<->F,2000-01-06',
            'B,2000-01-02<->H,2000-01-08',
        ]
        str_network = "1 (A, 2000-01-01) --> 2, 3\n2 (B, 2000-01-02) --> 1, 4, 6, 8\n3 (C, 2000-01-03) --> 4, 1\n4 (D, 2000-01-04) --> 3, 2\n5 (E, 2000-01-05) --> 6\n6 (F, 2000-01-06) --> 5, 2\n7 (G, 2000-01-07) --> 8\n8 (H, 2000-01-08) --> 7, 2\n"
        friend_id = 4
        comparison_date = datetime.date(2022,12,25)
        S = SocialNetwork(line, [])
        S.make_birthday_posts(friend_id,comparison_date)
        expected = []
        assert S.posts == expected, f'with the network of \n{str_network}\n we looked for birthday posts for the friend id: {friend_id} on the date {comparison_date} and expected the posts\n{expected}\n we got\n{S.posts}'

    def testManyFriendOneDay(self):
        line = [
            'A,2000-01-01<->B,2000-01-02',
            'C,2000-01-03<->D,2000-01-04',
            'E,2000-01-05<->F,2000-01-06',
            'G,2000-01-07<->H,2000-01-08',
            'A,2000-01-01<->C,2000-01-03',
            'B,2000-01-02<->D,2000-01-04',
            'B,2000-01-02<->F,2000-01-06',
            'B,2000-01-02<->H,2000-01-08',
        ]
        str_network = "1 (A, 2000-01-01) --> 2, 3\n2 (B, 2000-01-02) --> 1, 4, 6, 8\n3 (C, 2000-01-03) --> 4, 1\n4 (D, 2000-01-04) --> 3, 2\n5 (E, 2000-01-05) --> 6\n6 (F, 2000-01-06) --> 5, 2\n7 (G, 2000-01-07) --> 8\n8 (H, 2000-01-08) --> 7, 2\n"
        friend_id = 2
        comparison_date = datetime.date(2022,12,25)
        S = SocialNetwork(line, [])
        S.make_birthday_posts(friend_id,comparison_date)
        expected = [('Happy birthday A! Hope you have a good one!', 2, [1])]
        assert S.posts == expected, f'with the network of \n{str_network}\n we looked for birthday posts for the friend id: {friend_id} on the date {comparison_date} and expected the posts\n{expected}\n we got\n{S.posts}'

    def testManyFriendManyDay(self):
        line = [
            'A,2000-01-01<->B,2000-01-02',
            'C,2000-01-03<->D,2000-01-04',
            'E,2000-01-05<->F,2000-01-06',
            'G,2000-01-07<->H,2000-01-08',
            'A,2000-01-01<->C,2000-01-03',
            'B,2000-01-02<->D,2000-01-04',
            'B,2000-01-02<->F,2000-01-06',
            'B,2000-01-02<->H,2000-01-08',
        ]
        str_network = "1 (A, 2000-01-01) --> 2, 3\n2 (B, 2000-01-02) --> 1, 4, 6, 8\n3 (C, 2000-01-03) --> 4, 1\n4 (D, 2000-01-04) --> 3, 2\n5 (E, 2000-01-05) --> 6\n6 (F, 2000-01-06) --> 5, 2\n7 (G, 2000-01-07) --> 8\n8 (H, 2000-01-08) --> 7, 2\n"
        friend_id = 2
        comparison_date = datetime.date(2022,1,2)
        S = SocialNetwork(line, [])
        S.make_birthday_posts(friend_id,comparison_date)
        expected = [('Happy birthday A! Hope you have a good one!', 2, [1]), ('Happy birthday D! Hope you have a good one!', 2, [4]), ('Happy birthday F! Hope you have a good one!', 2, [6]), ('Happy birthday H! Hope you have a good one!', 2, [8])]
        assert S.posts == expected, f'with the network of \n{str_network}\n we looked for birthday posts for the friend id: {friend_id} on the date {comparison_date} and expected the posts\n{expected}\n we got\n{S.posts}'

if __name__=="__main__":
        unittest.main()
