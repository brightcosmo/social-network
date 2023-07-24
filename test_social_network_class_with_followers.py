from contextlib import contextmanager
import sys, os
from social_network_class_with_followers import *
import datetime
import unittest

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout

class build_network_test(unittest.TestCase):
    def testNull(self):
        line = []
        expected = ""
        S = SocialNetworkWithFollowers(line, [])
        assert str(S)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(S)}'

    def testOnePerson(self):
        line = ['A,2000-01-01']
        expected = "1 (A, 2000-01-01) --> Fr[] ==> Fo[]\n"
        observed = SocialNetworkWithFollowers(line, [])
        assert str(observed)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(observed)}'

    def testManyPeopleNoFriends(self):
        line = ['A,2000-01-01','B,2000-01-02','C,2000-01-03']
        expected = "1 (A, 2000-01-01) --> Fr[] ==> Fo[]\n2 (B, 2000-01-02) --> Fr[] ==> Fo[]\n3 (C, 2000-01-03) --> Fr[] ==> Fo[]\n"
        observed = SocialNetworkWithFollowers(line, [])
        assert str(observed)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(observed)}'

    def testManyPeopleNoFriendsDupes(self):
        line = ['A,2000-01-01','B,2000-01-02','C,2000-01-03','B,2000-01-02']
        expected = "1 (A, 2000-01-01) --> Fr[] ==> Fo[]\n2 (B, 2000-01-02) --> Fr[] ==> Fo[]\n3 (C, 2000-01-03) --> Fr[] ==> Fo[]\n"
        observed = SocialNetworkWithFollowers(line, [])
        assert str(observed)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(observed)}'

    def testOnePair(self):
        line = ['A,2000-01-01<->B,2000-01-02']
        expected = "1 (A, 2000-01-01) --> Fr[2] ==> Fo[]\n2 (B, 2000-01-02) --> Fr[1] ==> Fo[]\n"
        observed = SocialNetworkWithFollowers(line, [])
        assert str(observed)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(observed)}'

    def testOneFollow(self):
        line = ['A,2000-01-01-->B,2000-01-02']
        expected = "1 (A, 2000-01-01) --> Fr[] ==> Fo[2]\n2 (B, 2000-01-02) --> Fr[] ==> Fo[]\n"
        observed = SocialNetworkWithFollowers(line, [])
        assert str(observed)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(observed)}'

    def testOneBackFollow(self):
        line = ['A,2000-01-01<--B,2000-01-02']
        expected = "1 (A, 2000-01-01) --> Fr[] ==> Fo[]\n2 (B, 2000-01-02) --> Fr[] ==> Fo[1]\n"
        observed = SocialNetworkWithFollowers(line, [])
        assert str(observed)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(observed)}'

    def testOneDblFollow(self):
        line = ['A,2000-01-01<--B,2000-01-02','A,2000-01-01-->B,2000-01-02']
        expected = "1 (A, 2000-01-01) --> Fr[] ==> Fo[2]\n2 (B, 2000-01-02) --> Fr[] ==> Fo[1]\n"
        observed = SocialNetworkWithFollowers(line, [])
        assert str(observed)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(observed)}'

    def testOnePairOneSingle(self):
        line = ['A,2000-01-01<->B,2000-01-02','C,2000-01-03']
        expected = "1 (A, 2000-01-01) --> Fr[2] ==> Fo[]\n2 (B, 2000-01-02) --> Fr[1] ==> Fo[]\n3 (C, 2000-01-03) --> Fr[] ==> Fo[]\n"
        observed = SocialNetworkWithFollowers(line, [])
        assert str(observed)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(observed)}'

    def testManyPeopleManyFriends(self):
        line = ['A,2000-01-01<->B,2000-01-02','C,2000-01-03<->D,2000-01-04','E,2000-01-05<->F,2000-01-06','G,2000-01-07<->H,2000-01-08']
        expected = "1 (A, 2000-01-01) --> Fr[2] ==> Fo[]\n2 (B, 2000-01-02) --> Fr[1] ==> Fo[]\n3 (C, 2000-01-03) --> Fr[4] ==> Fo[]\n4 (D, 2000-01-04) --> Fr[3] ==> Fo[]\n5 (E, 2000-01-05) --> Fr[6] ==> Fo[]\n6 (F, 2000-01-06) --> Fr[5] ==> Fo[]\n7 (G, 2000-01-07) --> Fr[8] ==> Fo[]\n8 (H, 2000-01-08) --> Fr[7] ==> Fo[]\n"
        observed = SocialNetworkWithFollowers(line, [])
        assert str(observed)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(observed)}'

    def testManyPeopleManyFollows(self):
        line = ['A,2000-01-01-->B,2000-01-02','C,2000-01-03<--D,2000-01-04','E,2000-01-05<--F,2000-01-06','C,2000-01-03<--G,2000-01-07','G,2000-01-07-->H,2000-01-08']
        expected = "1 (A, 2000-01-01) --> Fr[] ==> Fo[2]\n2 (B, 2000-01-02) --> Fr[] ==> Fo[]\n3 (C, 2000-01-03) --> Fr[] ==> Fo[]\n4 (D, 2000-01-04) --> Fr[] ==> Fo[3]\n5 (E, 2000-01-05) --> Fr[] ==> Fo[]\n6 (F, 2000-01-06) --> Fr[] ==> Fo[5]\n7 (G, 2000-01-07) --> Fr[] ==> Fo[3, 8]\n8 (H, 2000-01-08) --> Fr[] ==> Fo[]\n"
        observed = SocialNetworkWithFollowers(line, [])
        assert str(observed)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(observed)}'

    def testManyPeopleManyFollowsAndFriends(self):
        line = ['A,2000-01-01-->B,2000-01-02','C,2000-01-03<--D,2000-01-04','E,2000-01-05<->F,2000-01-06','C,2000-01-03<--G,2000-01-07','G,2000-01-07-->H,2000-01-08']
        expected = "1 (A, 2000-01-01) --> Fr[] ==> Fo[2]\n2 (B, 2000-01-02) --> Fr[] ==> Fo[]\n3 (C, 2000-01-03) --> Fr[] ==> Fo[]\n4 (D, 2000-01-04) --> Fr[] ==> Fo[3]\n5 (E, 2000-01-05) --> Fr[6] ==> Fo[]\n6 (F, 2000-01-06) --> Fr[5] ==> Fo[]\n7 (G, 2000-01-07) --> Fr[] ==> Fo[3, 8]\n8 (H, 2000-01-08) --> Fr[] ==> Fo[]\n"
        observed = SocialNetworkWithFollowers(line, [])
        assert str(observed)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(observed)}'

    def testManyPeopleManyFriendsFollowerDupes(self):
        line = [
            'A,2000-01-01<->B,2000-01-02',
            'C,2000-01-03<--D,2000-01-04',
            'E,2000-01-05-->F,2000-01-06',
            'G,2000-01-07<->H,2000-01-08',
            'A,2000-01-01-->C,2000-01-03',
            'B,2000-01-02<--D,2000-01-04',
            'B,2000-01-02<--F,2000-01-06',
            'B,2000-01-02<->H,2000-01-08',
        ]
        expected = "1 (A, 2000-01-01) --> Fr[2] ==> Fo[3]\n2 (B, 2000-01-02) --> Fr[1, 8] ==> Fo[]\n3 (C, 2000-01-03) --> Fr[] ==> Fo[]\n4 (D, 2000-01-04) --> Fr[] ==> Fo[3, 2]\n5 (E, 2000-01-05) --> Fr[] ==> Fo[6]\n6 (F, 2000-01-06) --> Fr[] ==> Fo[2]\n7 (G, 2000-01-07) --> Fr[8] ==> Fo[]\n8 (H, 2000-01-08) --> Fr[7, 2] ==> Fo[]\n"
        observed = SocialNetworkWithFollowers(line, [])
        assert str(observed)==expected, f'str(Expected social_network_ff({line})) == {expected}; got \n{str(observed)}'

threaded_post_tests = {
    'str_network': ('1 (A, 2000-01-01) --> Fr[2] ==> Fo[3]'+'\n'+
                    '2 (B, 2000-01-02) --> Fr[1, 8] ==> Fo[]'+'\n'+
                    '3 (C, 2000-01-03) --> Fr[] ==> Fo[]'+'\n'+
                    '4 (D, 2000-01-04) --> Fr[5] ==> Fo[3, 2]'+'\n'+
                    '5 (E, 2000-01-05) --> Fr[4] ==> Fo[6]'+'\n'+
                    '6 (F, 2000-01-06) --> Fr[] ==> Fo[2]'+'\n'+
                    '7 (G, 2000-01-07) --> Fr[8] ==> Fo[4]'+'\n'+
                    '8 (H, 2000-01-08) --> Fr[7, 2] ==> Fo[]'),
    'network': [
            'A,2000-01-01<->B,2000-01-02',
            'C,2000-01-03<--D,2000-01-04',
            'E,2000-01-05-->F,2000-01-06',
            'G,2000-01-07<->H,2000-01-08',
            'A,2000-01-01-->C,2000-01-03',
            'B,2000-01-02<--D,2000-01-04',
            'B,2000-01-02<--F,2000-01-06',
            'B,2000-01-02<->H,2000-01-08',
            'D,2000-01-04<->E,2000-01-05',
            'G,2000-01-07-->D,2000-01-04',
        ],
    "contents":[
        ["source"],
        ["source"],
        ["source1","child2.1","child2.2"],
        ["source1","child2.1","child2.2"],
        ["source1","child2.1","child2.2","child2.3","child3.1","child3.2","child4.1"],
        ["source1","child2.1","child2.2","child2.3","child2.4","child3.1","child3.2","child3.3","child4.1","child4.2"],
        ["source1","child2.1","child2.2","child2.3","child3.1","child3.2","child4.1"],
        ["Mustard 1","Tomato Sauce 2.1","Jam flavoured jam 3.1","Liquified vaporised bees vomit 3.2"],
        ["Spiders are not nice", "What about spiders with spiders for eyes?", "Wait did we not all dress up as parts of a spider?"],
    ],
    "owners":[
        [4],
        [4],
        [4,5,7],
        [4,5,7],
        [4,5,7,7,4,8,2],
        [4,5,5,5,7,4,5,3,6,5],
        [4,5,7,7,4,8,5],
        [1,2,4,8],
        [1,2,4],
    ],
    "tagged":[
        [[]],
        [[]],
        [[],[],[]],
        [[],[],[]],
        [[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[],[],[],[]],
        [[],[],[],[],[],[],[]],
        [[],[],[],[]],
        [[],[],[1,3,5,2]],
    ],
    "private":[
        [True],
        [False],
        [False,False,False],
        [True,True,True],
        [False,False,False,False,False,False,False],
        [True,True,True,True,True,True,True,True,True,True],
        [False,False,False,False,False,False,False],
        [False,True,False,False],
        [False,False,False,False]
    ],
    "test_describe":[
        [f'network.people.get_person_by_id(4).make_threaded_post("source",[],True)'],
        [f'network.people.get_person_by_id(4).make_threaded_post("source",[],False)'],
        [
            f'source = network.people.get_person_by_id(4).make_threaded_post("source1",[],False)',
            f'add_child(source,"child2.1",5,[],False)',
            f'add_child(source,"child2.2",7,[],False)',
        ],
        [
            f'source = network.people.get_person_by_id(4).make_threaded_post("source1",[],True)',
            f'add_child(source,"child2.1",5,[],True)',
            f'add_child(source,"child2.2",7,[],True)',
        ],
        [
            f'source = network.people.get_person_by_id(4).make_threaded_post("source1",[],False)',
            f'add_child(source,"child2.1",5,[],False)',
            f'add_child(source,"child2.2",7,[],False)',
            f'add_child(source,"child2.3",7,[],False)',
            f'add_child(source[4][0],"child3.1,4,[],False")',
            f'add_child(source[4][1],"child3.2,8,[],False")',
            f'add_child(source[4][1][4][0],"child4.1,2,[],False")',
        ],
        [
            f'source = network.people.get_person_by_id(4).make_threaded_post("source1",[],True)',
            f'add_child(source, "child2.1",5,[],True)',
            f'add_child(source, "child2.2",5,[],True)',
            f'add_child(source, "child2.3",5,[],True)',
            f'add_child(source, "child2.4",7,[],True)',
            f'add_child(source[4][0], "child3.1,4,[],True")',
            f'add_child(source[4][1], "child3.2,5,[],True")',
            f'add_child(source[4][1], "child3.3,3,[],True")',
            f'add_child(source[4][1][4][0], "child4.1,6,[],True")',
            f'add_child(source[4][1][4][0], "child4.2,5,[],True")',
        ],
        [
            f'source = network.people.get_person_by_id(4).make_threaded_post("source1",[],False)',
            f'add_child(source, "child2.1",5,[],False)',
            f'add_child(source, "child2.2",7,[],False)',
            f'add_child(source, "child2.3",7,[],False)',
            f'add_child(source[4][0], "child3.1,4,[],False")',
            f'add_child(source[4][1], "child3.2,8,[],False")',
            f'add_child(source[4][0][4][0], "child4.1,5,[],False")',
        ],
        [
            f'source = network.people.get_person_by_id(1).make_threaded_post("Mustard 1",[],False)',
            f'add_child(source, "Tomato Sauce 2.1",2,[],True)',
            f'add_child(source[4][0], "Jam flavoured jam 3.1",4,[],False")',
            f'add_child(source[4][0], "Liquified vaporised bees vomit 3.2",8,[],False")',
        ],
        [
            f'source = network.people.get_person_by_id(1).make_threaded_post("Spiders are not nice",[],False)',
            f'add_child(source, "What about spiders with spiders for eyes?",2,[],True)',
            f'add_child(source[4][0], "Wait did we not all dress up as parts of a spider?",4,[1,3,5,2],False")',
        ],
    ]
    ,
    "expected":[
        [('source', 4, [], True, [])],
        [('source', 4, [], False, [])],
        [('source1', 4, [], False, [('child2.1', 5, [], False, []), ('child2.2', 7, [], False, [])])],
        [('source1', 4, [], True, [('child2.1', 5, [], True, [])])],
        [('source1', 4, [], False, [('child2.1', 5, [], False, [('child3.1', 4, [], False, [])]), ('child2.2', 7, [], False, [('child3.2', 8, [], False, [('child4.1', 2, [], False, [])])]), ('child2.3', 7, [], False, [])]), ('child3.1', 4, [], False, [])],
        [('source1', 4, [], True, [('child2.1', 5, [], True, [('child3.1', 4, [], True, [])]), ('child2.2', 5, [], True, [('child3.2', 5, [], True, [('child4.2', 5, [], True, [])])]), ('child2.3', 5, [], True, [])]), ('child3.1', 4, [], True, [])],
        [('source1', 4, [], False, [('child2.1', 5, [], False, [('child3.1', 4, [], False, [('child4.1', 5, [], False, [])])]),('child2.2', 7, [], False, [('child3.2', 8, [], False, [])]),('child2.3', 7, [], False, [])	]),	('child3.1', 4, [], False, [('child4.1', 5, [], False, [])])],
        [('Mustard 1', 1, [], False, [('Tomato Sauce 2.1', 2, [] ,True, [('Liquified vaporised bees vomit 3.2', 8, [], False, [])])])],
        [('Spiders are not nice', 1, [], False, [('What about spiders with spiders for eyes?', 2, [], False, [('Wait did we not all dress up as parts of a spider?', 4, [5], False, [])])])]
    ]
}
make_network = lambda : SocialNetworkWithFollowers(threaded_post_tests['network'], [])
get_post_data = lambda case : {"contents": threaded_post_tests["contents"][case], "owners": threaded_post_tests["owners"][case], "tagged": threaded_post_tests["tagged"][case], "private": threaded_post_tests["private"][case]}
str_expect_expected = lambda case : [[str(i) for i in threaded_post_tests["expected"][case]], threaded_post_tests["expected"][case]]
expect_actual = lambda case, person : [[str(i) for i in person.history]] + str_expect_expected(case)
get_test_calls = lambda case : "\n".join(threaded_post_tests["test_describe"][case])
class threaded_post_test(unittest.TestCase):
    def testSourceOnlyPrivate(self):
        case = 0
        failed=False
        str_Expected, Expected = str_expect_expected(case)
        try:
            str_network = threaded_post_tests["str_network"]
            S = make_network()
            R = get_post_data(case)
            person = S.people[R["owners"][0]]
            source = person.make_threaded_post(R["contents"][0],R["tagged"][0],R["private"][0])
            str_posts,str_Expected, Expected = expect_actual(case, person)
            with suppress_stdout():

                self.assertListEqual(str_posts,str_Expected)
        except:
            failed=True
        #You release here:
        if failed:
            actual,expected = 1,2
            assert actual==expected, f'\n\nWith network \n{str_network}\n\nWe ran these calls:\n{get_test_calls(case)}\nExpected: {Expected}\nGot:      {person.history}'

    def testSourceOnlyPublic(self):
        case = 1
        failed=False
        str_Expected, Expected = str_expect_expected(case)
        try:
            str_network = threaded_post_tests["str_network"]
            S = make_network()
            R = get_post_data(case)
            person = S.people[R["owners"][0]]

            source = person.make_threaded_post(R["contents"][0],R["tagged"][0],R["private"][0])
            str_posts,str_Expected, Expected = expect_actual(case, person)
            with suppress_stdout():
                self.assertListEqual(str_posts,str_Expected)
        except:
            failed=True
        if failed:
            actual,expected = 1,2
            assert actual==expected, f'\n\nWith network \n{str_network}\n\nWe ran these calls:\n{get_test_calls(case)}\nExpected: {Expected}\nGot:      {person.history}'

    def testOneChildPublicFollowFriend(self):
        case = 2
        failed=False
        str_Expected, Expected = str_expect_expected(case)
        try:
            str_network = threaded_post_tests["str_network"]
            S = make_network()
            R = get_post_data(case)
            person = S.people[R["owners"][0]]

            source = person.make_threaded_post(R["contents"][0],R["tagged"][0],R["private"][0])
            for childcount in range(1,3):
                add_child(source, R["contents"][childcount],S.people[R["owners"][childcount]],R["tagged"][childcount],R["private"][childcount])

            str_posts,str_Expected, Expected = expect_actual(case, person)
            with suppress_stdout():
                self.assertListEqual(str_posts,str_Expected)
        except:
            failed=True
        #You release here:
        if failed:
            actual,expected = 1,2
            assert actual==expected, f'\n\nWith network \n{str_network}\n\nWe ran these calls:\n{get_test_calls(case)}\nExpected: {Expected}\nGot:      {person.history}'

    def testOneChildPrivateFollowFriend(self):
        case = 3
        failed=False
        str_Expected, Expected = str_expect_expected(case)
        try:
            str_network = threaded_post_tests["str_network"]
            S = make_network()
            R = get_post_data(case)
            person = S.people[R["owners"][0]]

            source = person.make_threaded_post(R["contents"][0],R["tagged"][0],R["private"][0])
            for childcount in range(1,3):
                add_child(source, R["contents"][childcount],S.people[R["owners"][childcount]],R["tagged"][childcount],R["private"][childcount])
            str_posts,str_Expected, Expected = expect_actual(case, person)
            with suppress_stdout():
                self.assertListEqual(str_posts,str_Expected)
        except:
            failed=True
        #You release here:
        if failed:
            actual,expected = 1,2
            assert actual==expected, f'\n\nWith network \n{str_network}\n\nWe ran these calls:\n{get_test_calls(case)}\nExpected: {Expected}\nGot:      {person.history}'

    def testManyLevelPrivate(self):
        case = 4
        failed=False
        str_Expected, Expected = str_expect_expected(case)
        try:
            str_network = threaded_post_tests["str_network"]
            S = make_network()
            R = get_post_data(case)
            person = S.people[R["owners"][0]]

            source = person.make_threaded_post(R["contents"][0],R["tagged"][0],R["private"][0])
            index = 1
            while index < 4:
                add_child(source, R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
                index+=1
            add_child(source[4][0], R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
            index+=1
            add_child(source[4][1], R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
            index+=1
            add_child(source[4][1][4][0], R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
            str_posts,str_Expected, Expected = expect_actual(case, person)
            with suppress_stdout():
                self.assertListEqual(str_posts,str_Expected)
        except:
            failed=True
        #You release here:
        if failed:
            actual,expected = 1,2
            assert actual==expected, f'\n\nWith network \n{str_network}\n\nWe ran these calls:\n{get_test_calls(case)}\nExpected: {Expected}\nGot:      {person.history}'

    def testManyLevelPublic(self):
        case = 5
        failed=False
        str_Expected, Expected = str_expect_expected(case)
        try:
            str_network = threaded_post_tests["str_network"]
            S = make_network()
            R = get_post_data(case)
            person = S.people[R["owners"][0]]

            source = person.make_threaded_post(R["contents"][0],R["tagged"][0],R["private"][0])
            index = 1
            while index < 5:
                add_child(source, R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
                index+=1

            add_child(source[4][0], R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
            index+=1
            for _ in range(2):
                add_child(source[4][1], R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
                index+=1
            for _ in range(2):
                add_child(source[4][1][4][0], R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
                index+=1
            str_posts,str_Expected, Expected = expect_actual(case, person)
            with suppress_stdout():
                self.assertListEqual(str_posts,str_Expected)

        except:
            failed = True


        #You release here:
        if failed:
            actual,expected = 1,2
            assert actual==expected, f'\n\nWith network \n{str_network}\n\nWe ran these calls:\n{get_test_calls(case)}\nExpected: {Expected}\nGot:      {person.history}'

    def testManyLevelPrivateMultiSelfPosts(self):
        case = 6
        failed=False
        str_Expected, Expected = str_expect_expected(case)
        try:
            str_network = threaded_post_tests["str_network"]
            S = make_network()
            R = get_post_data(case)
            person = S.people[R["owners"][0]]

            source = person.make_threaded_post(R["contents"][0],R["tagged"][0],R["private"][0])
            index = 1
            while index < 4:
                add_child(source, R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
                index+=1
            add_child(source[4][0], R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
            index+=1
            add_child(source[4][1], R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
            index+=1
            add_child(source[4][0][4][0], R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
            str_posts,str_Expected, Expected = expect_actual(case, person)
            with suppress_stdout():
                self.assertListEqual(str_posts,str_Expected)
        except:
            failed=True
        #You release here:
        if failed:
            actual,expected = 1,2
            assert actual==expected, f'\n\nWith network \n{str_network}\n\nWe ran these calls:\n{get_test_calls(case)}\nExpected: {Expected}\nGot:      {person.history}'

    def testDifferingPrivacy(self):
        case = 7
        failed=False
        str_Expected, Expected = str_expect_expected(case)
        try:
            str_network = threaded_post_tests["str_network"]
            S = make_network()
            R = get_post_data(case)
            person = S.people[R["owners"][0]]

            source = person.make_threaded_post(R["contents"][0],R["tagged"][0],R["private"][0])
            index = 1
            add_child(source, R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
            for _ in range(2):
                index+=1
                add_child(source[4][0], R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
            str_posts,str_Expected, Expected = expect_actual(case, person)
            with suppress_stdout():
                self.assertListEqual(str_posts,str_Expected)
        except:
            failed=True
        #You release here:
        if failed:
            actual,expected = 1,2
            assert actual==expected, f'\n\nWith network \n{str_network}\n\nWe ran these calls:\n{get_test_calls(case)}\nExpected: {Expected}\nGot:      {person.history}'

    def testLevelsTagged(self):
        case = 8
        failed=False
        str_Expected, Expected = str_expect_expected(case)
        try:
            str_network = threaded_post_tests["str_network"]
            S = make_network()
            R = get_post_data(case)
            person = S.people[R["owners"][0]]

            source = person.make_threaded_post(R["contents"][0],R["tagged"][0],R["private"][0])
            index = 1
            add_child(source, R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
            index+=1
            add_child(source[4][0], R["contents"][index],S.people[R["owners"][index]],R["tagged"][index],R["private"][index])
            str_posts,str_Expected, Expected = expect_actual(case, person)
            with suppress_stdout():
                self.assertListEqual(str_posts,str_Expected)
        except:
            failed=True

        if failed:
            actual,expected = 1,2
            assert actual==expected, f'\n\nWith network \n{str_network}\n\nWe ran these calls:\n{get_test_calls(case)}\nExpected: {Expected}\nGot:      {person.history}'


if __name__=="__main__":
        unittest.main()

