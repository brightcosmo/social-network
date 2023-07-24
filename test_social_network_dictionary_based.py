from social_network_dictionary_based import *
import datetime
import unittest
import copy
def dict_equal(d1,d2):
    if len(d1) == len(d2):
        for key in d1:
            if key in d2:
                if (type(d1[key]) == type(dict())) and (type(d2[key]) == type(dict())):
                    result = dict_equal(d1[key],d2[key])
                    if not result:
                        return False
                elif not (d1[key] == d2[key]):
                    return False
            else:
                return False
        return True
    return False
def list_of_dict_equal(l1,l2):
    if len(l1) == len(l2):
        for index in range(len(l1)):
            if not dict_equal(l1[index],l2[index]):
                return False
        return True
    return False
def duplicate_dict_wo_X(dict_in,X,recursive=False):
    """
    to allow test cases to work regardless of whether a history attribute exists
    :param dict_in: teh dictionary potentially including an attribute "X" -- be it history or some other
    :return: a new dictionary containing all elements except the property X
    """
    output_dict = dict()
    for key in dict_in:
        if not (key == X):
            if recursive and type(dict_in[key]) == type(dict()):
                output_dict[key] = duplicate_dict_wo_X(dict_in[key],X,recursive)
            else:
                output_dict[key] = copy.deepcopy(dict_in[key])
    return output_dict

new_dict_no_history = lambda dict_in,recursive=False : duplicate_dict_wo_X(dict_in,"history",recursive)
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
make_person_test_case = lambda case : True if dict_equal(new_dict_no_history(make_person(make_person_cases["inputs"][case][0],make_person_cases["inputs"][case][1],make_person_cases["inputs"][case][2])),make_person_cases["expected"][case]) else f'Expected make_person_cases({make_person_cases["inputs"][case][0],make_person_cases["inputs"][case][1],make_person_cases["inputs"][case][2]})==...\n{make_person_cases["expected"][case]}; got \n{make_person(make_person_cases["inputs"][case][0],make_person_cases["inputs"][case][1],make_person_cases["inputs"][case][2])}'
class make_person_Test(unittest.TestCase):
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

find_person_cases = {
    "inputs": [
        [{'friends': [], 'id': 1, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [1], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [2], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [5,7,13,6,4,1,99], 'id': 3, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [5,7,3,6,4,11,99], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [1], 'id': 4, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [], 'id': 5, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [5], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
    ],
    "expected":[
        None,
        0,
        2,
        None,
        0
    ]
}
find_person_test_case = lambda case : True if find_friendX_inY(find_person_cases["inputs"][case][0],find_person_cases["inputs"][case][1]) == find_person_cases["expected"][case] else f'Expected find_friendX_inY(\n{find_person_cases["inputs"][case][0]},\n{find_person_cases["inputs"][case][1]}\n)=={find_person_cases["expected"][case]}; got {find_friendX_inY(find_person_cases["inputs"][case][0],find_person_cases["inputs"][case][1])}'
class find_person_Test(unittest.TestCase):
    def testSelfNoFriend(self):
        R = find_person_test_case(0)
        assert R==True,R
    def testBiDirectional(self):
        R = find_person_test_case(1)
        assert R==True,R
    def testBidirectionalMidList(self):
        R = find_person_test_case(2)
        assert R==True,R
    def testY_in_X_only(self):
        R = find_person_test_case(3)
        assert R==True,R
    def testX_in_Y_only(self):
        R = find_person_test_case(4)
        assert R==True,R

make_friendship_cases = {
    "str_input":[
        [R"{'friends': [], 'id': 1, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
        [R"{'friends': [1], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [2], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
        [R"{'friends': [5,7,8,6,4,1,99], 'id': 3, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [5,7,3,6,4,12,99], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
        [R"{'friends': [1], 'id': 4, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
        [R"{'friends': [], 'id': 5, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [5], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
        [R"{'friends': [], 'id': 5, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
    ],
    "inputs": [
        [{'friends': [], 'id': 1, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [], 'id': 1, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [1], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [2], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [5,7,8,6,4,1,99], 'id': 3, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [5,7,3,6,4,12,99], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [1], 'id': 4, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [], 'id': 5, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [5], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [], 'id': 5, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
    ],
    "expected":[
        [[],[]],
        [[1],[2]],
        [[5,7,8,6,4,1,99],[5,7,3,6,4,12,99]],
        [[1],[4]],
        [[1],[5]],
        [[1],[5]],
    ]

}
run_friendship_test_input = lambda case : make_friendship(make_friendship_cases["inputs"][case][0],make_friendship_cases["inputs"][case][1])
check_friendship_test_output = lambda case : True if (make_friendship_cases["inputs"][case][0]['friends'] == make_friendship_cases["expected"][case][0]) and (make_friendship_cases["inputs"][case][1]['friends'] == make_friendship_cases["expected"][case][1]) else f'Expected make_friendship(\n{make_friendship_cases["str_input"][case][0]},\n{make_friendship_cases["str_input"][case][1]}\n) would result in --> Friends holding: \n{make_friendship_cases["expected"][case][0]},\nInstead we got: {make_friendship_cases["expected"][case][1]}'
class make_friendship_Test(unittest.TestCase):
    def testSelfFriend(self):
        case = 0
        run_friendship_test_input(case)
        R = check_friendship_test_output(case)
        assert R==True,R
    def testExistingFriend(self):
        case = 1
        run_friendship_test_input(case)
        R = check_friendship_test_output(case)
        assert R==True,R
    def testExistingManyFriend(self):
        case = 2
        run_friendship_test_input(case)
        R = check_friendship_test_output(case)
        assert R==True,R
    def testY_to_X_Friend(self):
        case = 3
        run_friendship_test_input(case)
        R = check_friendship_test_output(case)
        assert R==True,R
    def testX_to_Y_Friend(self):
        case = 4
        run_friendship_test_input(case)
        R = check_friendship_test_output(case)
        assert R==True,R
    def testNotFriend(self):
        case = 5
        run_friendship_test_input(case)
        R = check_friendship_test_output(case)
        assert R==True,R

end_friendship_cases = {
    "str_input":[
        [R"{'friends': [], 'id': 1, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
        [R"{'friends': [1], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [2], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
        [R"{'friends': [5,7,8,6,4,1,99], 'id': 3, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [5,7,3,6,4,12,99], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
        [R"{'friends': [1], 'id': 4, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
        [R"{'friends': [], 'id': 5, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [5], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
        [R"{'friends': [], 'id': 5, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
        [R"{'friends': [15,7,8,6,4,1,99], 'id': 5, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)}",R"{'friends': [5,7,3,6,4,12,199], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}"],
    ],
    "inputs": [
        [{'friends': [], 'id': 1, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [1], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [2], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [5,7,8,6,4,1,99], 'id': 3, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [5,7,3,6,4,12,99], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [1], 'id': 4, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [], 'id': 5, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [5], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [], 'id': 5, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [], 'id': 1, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
        [{'friends': [15,7,8,6,4,1,99], 'id': 5, 'name': 'X', 'date_of_birth': datetime.date(2000, 1, 1)},{'friends': [5,7,3,6,4,12,199], 'id': 99, 'name': 'Y', 'date_of_birth': datetime.date(2000, 1, 1)}],
    ],
    "expected":[
        [[],[]],
        [[],[]],
        [[5,7,8,6,4,99],[5,7,6,4,12,99]],
        [[],[]],
        [[],[]],
        [[],[]],
        [[15,7,8,6,4,1],[7,3,6,4,12,199]],
    ]

}
run_end_friendship_test_input = lambda case : end_friendship(end_friendship_cases["inputs"][case][0],end_friendship_cases["inputs"][case][1])
check_end_friendship_test_output = lambda case : True if (end_friendship_cases["inputs"][case][0]['friends'] == end_friendship_cases["expected"][case][0]) and (end_friendship_cases["inputs"][case][1]['friends'] == end_friendship_cases["expected"][case][1]) else f'Expected make_friendship(\n{end_friendship_cases["str_input"][case][0]},\n{end_friendship_cases["str_input"][case][1]}\n) --> Friends == \n{end_friendship_cases["expected"][case][0]},\n{end_friendship_cases["expected"][case][1]}'
class end_friendship_Test(unittest.TestCase):
    def testSelfFriend(self):
        case = 0
        run_end_friendship_test_input(case)
        R = check_end_friendship_test_output(case)
        assert R==True,R
    def testExistingFriend(self):
        case = 1
        run_end_friendship_test_input(case)
        R = check_end_friendship_test_output(case)
        assert R==True,R
    def testExistingManyFriend(self):
        case = 2
        run_end_friendship_test_input(case)
        R = check_end_friendship_test_output(case)
        assert R==True,R
    def testY_to_X_Friend(self):
        case = 3
        run_end_friendship_test_input(case)
        R = check_end_friendship_test_output(case)
        assert R==True,R
    def testX_to_Y_Friend(self):
        case = 4
        run_end_friendship_test_input(case)
        R = check_end_friendship_test_output(case)
        assert R==True,R
    def testNotFriend(self):
        case = 5
        run_end_friendship_test_input(case)
        R = check_end_friendship_test_output(case)
        assert R==True,R
    def testStartEndFriend(self):
        case = 6
        run_end_friendship_test_input(case)
        R = check_end_friendship_test_output(case)
        assert R==True,R

birthday_cases = {
    "inputs":[
        [{'friends': [], 'id': 1, 'name': 'X', 'date_of_birth': datetime.date(2000, 10, 10)},0,datetime.date(2000, 10, 10)],
        [{'friends': [], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(2000, 10, 10)},0,datetime.date(1000, 10, 10)],
        [{'friends': [], 'id': 3, 'name': 'X', 'date_of_birth': datetime.date(2000, 5, 5)},2,datetime.date(2000, 6, 5)],
        [{'friends': [], 'id': 4, 'name': 'X', 'date_of_birth': datetime.date(1980, 5, 5)},2,datetime.date(2000, 5, 6)],
        [{'friends': [], 'id': 5, 'name': 'X', 'date_of_birth': datetime.date(1845, 5, 30)},2,datetime.date(2000, 6, 1)],
        [{'friends': [], 'id': 6, 'name': 'X', 'date_of_birth': datetime.date(1845, 6, 1)},2,datetime.date(2000, 5, 30)],
        [{'friends': [], 'id': 7, 'name': 'X', 'date_of_birth': datetime.date(1845, 12, 15)},30,datetime.date(2000, 1, 10)],
        [{'friends': [], 'id': 8, 'name': 'X', 'date_of_birth': datetime.date(1845, 1, 10)},30,datetime.date(2000, 12, 15)],
    ],
    "expected":[
        True,
        True,
        False,
        True,
        True,
        True,
        True,
        True
    ]
}
birthday_check = lambda case : True if birthday_cases["expected"][case]==birthday_within_X_days_of_Y(birthday_cases["inputs"][case][0],birthday_cases["inputs"][case][1],birthday_cases["inputs"][case][2]) else f'Expected that birthday_within_X_days_of_Y({birthday_cases["inputs"][case][0],birthday_cases["inputs"][case][1],birthday_cases["inputs"][case][2]})=={birthday_cases["expected"][case]}; got {birthday_within_X_days_of_Y(birthday_cases["inputs"][case][0],birthday_cases["inputs"][case][1],birthday_cases["inputs"][case][2])}'
class birthday_within_test(unittest.TestCase):
    def testSameDay(self):
        R = birthday_check(0)
        assert R==True, R
    def testSameDayNotYear(self):
        R = birthday_check(1)
        assert R==True, R
    def testMonthWrong(self):
        R = birthday_check(2)
        assert R==True, R
    def testNearDay(self):
        R = birthday_check(3)
        assert R==True, R
    def testMonthEdge(self):
        R = birthday_check(4)
        assert R==True, R
    def testBirthdayPast(self):
        R = birthday_check(5)
        assert R==True, R
    def testYearEdge(self):
        R = birthday_check(6)
        assert R==True, R
    def testYearEdge2(self):
        R = birthday_check(7)
        assert R==True, R

add_person_cases = {
    "str_inputs": [
        f"{{1: {{'friends': [], 'id': 1, 'name': 'X', 'date_of_birth': datetime.date(1543, 5, 14)}},2: {{'friends': [], 'id': 2, 'name': 'Y', 'date_of_birth': datetime.date(1943, 12, 21)}},3: {{'friends': [], 'id': 3, 'name': 'Z', 'date_of_birth': datetime.date(2012, 3, 12)}}",
        f"{{}}"
    ],
    "inputs": [
        [{
            1: {'friends': [], 'id': 1, 'name': 'X', 'date_of_birth': datetime.date(1543, 5, 14)},
            2: {'friends': [], 'id': 2, 'name': 'Y', 'date_of_birth': datetime.date(1943, 12, 21)},
            3: {'friends': [], 'id': 3, 'name': 'Z', 'date_of_birth': datetime.date(2012, 3, 12)},
        },"AAAA",datetime.date(9999, 9, 19)],
        [{},"AAAB",datetime.date(9999, 9, 19)],
        [{
            1: {'friends': [], 'id': 1, 'name': 'X', 'date_of_birth': datetime.date(1543, 5, 14)},
            6: {'friends': [], 'id': 6, 'name': 'Y', 'date_of_birth': datetime.date(1943, 12, 21)},
            3: {'friends': [], 'id': 3, 'name': 'Z', 'date_of_birth': datetime.date(2012, 3, 12)},
        },"AAAC",datetime.date(9999, 9, 19)],
        [{
            765: {'friends': [], 'id': 765, 'name': 'X', 'date_of_birth': datetime.date(1543, 5, 14)},
        },"AAAD",datetime.date(9999, 9, 19)],
    ],
    "expected": [
        [4,{'friends': [], 'id': 4, 'name': 'AAAA', 'date_of_birth': datetime.date(9999, 9, 19)}],
        [1,{'friends': [], 'id': 1, 'name': 'AAAB', 'date_of_birth': datetime.date(9999, 9, 19)}],
        [7,{'friends': [], 'id': 7, 'name': 'AAAC', 'date_of_birth': datetime.date(9999, 9, 19)}],
        [766,{'friends': [], 'id': 766, 'name': 'AAAD', 'date_of_birth': datetime.date(9999, 9, 19)}],
    ]
}
run_add_person_case = lambda case : add_person(add_person_cases["inputs"][case][0],add_person_cases["inputs"][case][1],add_person_cases["inputs"][case][2])
check_add_person = lambda case : True if dict_equal(new_dict_no_history(add_person_cases["inputs"][case][0][add_person_cases["expected"][case][0]]),add_person_cases["expected"][case][1]) else f'Expected add_person({add_person_cases["str_inputs"][case]},\n{add_person_cases["inputs"][case][1],add_person_cases["inputs"][case][2]})\n --> adds {add_person_cases["expected"][case][1]} at position {add_person_cases["expected"][case][0]}\n Instead we have:\n {add_person_cases["inputs"][case][0]}'
class add_person_test(unittest.TestCase):
    def testExistingStd(self):
        case = 0
        run_add_person_case(case)
        R = check_add_person(case)
        assert R==True, R

    def testExistingEmpty(self):
        case = 1
        run_add_person_case(case)
        R = check_add_person(case)
        assert R==True, R

    def testBigNotAtEnd(self):
        case = 2
        run_add_person_case(case)
        R = check_add_person(case)
        assert R==True, R

    def testBigAtEnd(self):
        case = 3
        run_add_person_case(case)
        R = check_add_person(case)
        assert R==True, R

get_id_cases = {
    "look_in" : {
            1: {'friends': [], 'id': 1, 'name': 'X', 'date_of_birth': datetime.date(1543, 5, 14)},
            6: {'friends': [], 'id': 6, 'name': 'Y', 'date_of_birth': datetime.date(1943, 12, 21)},
            3: {'friends': [], 'id': 3, 'name': 'Z', 'date_of_birth': datetime.date(2012, 3, 12)},
        },
    "inputs" : [6,1,3,0,2,4,7,-1],
    "expected" : [
        {'friends': [], 'id': 6, 'name': 'Y', 'date_of_birth': datetime.date(1943, 12, 21)},
        {'friends': [], 'id': 1, 'name': 'X', 'date_of_birth': datetime.date(1543, 5, 14)},
        {'friends': [], 'id': 3, 'name': 'Z', 'date_of_birth': datetime.date(2012, 3, 12)},
        None,
        None,
        None,
        None,
        None
    ]
}
get_id_test = lambda case : True if (None is get_person_by_id(get_id_cases["look_in"],get_id_cases["inputs"][case]) if get_id_cases["expected"][case] is None else dict_equal(get_person_by_id(get_id_cases["look_in"],get_id_cases["inputs"][case]),get_id_cases["expected"][case])) else f'Expected get_person_by_id({get_id_cases["look_in"],get_id_cases["inputs"][case]})\n=={get_id_cases["expected"][case]}\nGot: {get_person_by_id(get_id_cases["look_in"],get_id_cases["inputs"][case])}'
class get_person_by_id_test(unittest.TestCase):
    def testStart(self):
        R = get_id_test(0)
        assert R==True,R
    def testMid(self):
        R = get_id_test(1)
        assert R==True,R
    def testEnd(self):
        R = get_id_test(2)
        assert R==True,R
    def testZero(self):
        R = get_id_test(3)
        assert R==True,R
    def testInvCountRight(self):
        R = get_id_test(4)
        assert R==True,R
    def testInvUnderMax(self):
        R = get_id_test(5)
        assert R==True,R
    def testInvOverMax(self):
        R = get_id_test(6)
        assert R==True,R
    def testInvNeg(self):
        R = get_id_test(7)
        assert R==True,R

class convert_lines_to_friendships_test(unittest.TestCase):
    def testNull(self):
        line = []
        expected = dict()
        observed = new_dict_no_history(convert_lines_to_friendships(line),True)
        assert dict_equal(expected,observed), f'Expected convert_lines_to_friendships({line}) == {expected}; got {observed}'

    def testOnePerson(self):
        line = ['A,2000-01-01']
        expected = {1: {'friends':[], 'id':1, 'name':"A", 'date_of_birth':datetime.date(2000,1,1)}}
        observed = new_dict_no_history(convert_lines_to_friendships(line),True)
        assert dict_equal(expected,observed), f'Expected convert_lines_to_friendships({line}) == {expected}; got {observed}'

    def testManyPeopleNoFriends(self):
        line = ['A,2000-01-01','B,2000-01-02','C,2000-01-03']
        expected = {1: {'friends':[], 'id':1, 'name':"A", 'date_of_birth':datetime.date(2000,1,1)},
                    2: {'friends':[], 'id':2, 'name':"B", 'date_of_birth':datetime.date(2000,1,2)},
                    3: {'friends':[], 'id':3, 'name':"C", 'date_of_birth':datetime.date(2000,1,3)}}
        observed = new_dict_no_history(convert_lines_to_friendships(line),True)
        assert dict_equal(expected,observed), f'Expected convert_lines_to_friendships({line}) == {expected}; got {observed}'

    def testManyPeopleNoFriendsDupes(self):
        line = ['A,2000-01-01','B,2000-01-02','C,2000-01-03','B,2000-01-02']
        expected = {1: {'friends':[], 'id':1, 'name':"A", 'date_of_birth':datetime.date(2000,1,1)},
                    2: {'friends':[], 'id':2, 'name':"B", 'date_of_birth':datetime.date(2000,1,2)},
                    3: {'friends':[], 'id':3, 'name':"C", 'date_of_birth':datetime.date(2000,1,3)}}
        observed = new_dict_no_history(convert_lines_to_friendships(line),True)
        assert dict_equal(expected,observed), f'Expected convert_lines_to_friendships({line}) == \n{expected}; got\n {observed}'

    def testOnePair(self):
        line = ['A,2000-01-01<->B,2000-01-02']
        expected = {1: {'friends':[2], 'id':1, 'name':"A", 'date_of_birth':datetime.date(2000,1,1)},
                    2: {'friends':[1], 'id':2, 'name':"B", 'date_of_birth':datetime.date(2000,1,2)}}
        observed = new_dict_no_history(convert_lines_to_friendships(line),True)
        assert dict_equal(expected,observed), f'Expected convert_lines_to_friendships({line}) == {expected}; got {observed}'

    def testOnePairOneSingle(self):
        line = ['A,2000-01-01<->B,2000-01-02','C,2000-01-03']
        expected = {1: {'friends':[2], 'id':1, 'name':"A", 'date_of_birth':datetime.date(2000,1,1)},
                    2: {'friends':[1], 'id':2, 'name':"B", 'date_of_birth':datetime.date(2000,1,2)},
                    3: {'friends':[], 'id':3, 'name':"C", 'date_of_birth':datetime.date(2000,1,3)}}
        observed = new_dict_no_history(convert_lines_to_friendships(line),True)
        assert dict_equal(expected,observed), f'Expected convert_lines_to_friendships({line}) == {expected}; got {observed}'

    def testManyPeopleManyFriends(self):
        line = ['A,2000-01-01<->B,2000-01-02','C,2000-01-03<->D,2000-01-04','E,2000-01-05<->F,2000-01-06','G,2000-01-07<->H,2000-01-08']
        expected = {1: {'friends':[2], 'id':1, 'name':"A", 'date_of_birth':datetime.date(2000,1,1)},
                    2: {'friends':[1], 'id':2, 'name':"B", 'date_of_birth':datetime.date(2000,1,2)},
                    3: {'friends':[4], 'id':3, 'name':"C", 'date_of_birth':datetime.date(2000,1,3)},
                    4: {'friends':[3], 'id':4, 'name':"D", 'date_of_birth':datetime.date(2000,1,4)},
                    5: {'friends':[6], 'id':5, 'name':"E", 'date_of_birth':datetime.date(2000,1,5)},
                    6: {'friends':[5], 'id':6, 'name':"F", 'date_of_birth':datetime.date(2000,1,6)},
                    7: {'friends':[8], 'id':7, 'name':"G", 'date_of_birth':datetime.date(2000,1,7)},
                    8: {'friends':[7], 'id':8, 'name':"H", 'date_of_birth':datetime.date(2000,1,8)}}
        observed = new_dict_no_history(convert_lines_to_friendships(line),True)
        assert dict_equal(expected,observed), f'Expected convert_lines_to_friendships({line}) == \n{expected}; got\n {observed}'

    def testManyPeopleManyFriendsDupes(self):
        line = [
            'A,2000-01-01<->B,2000-01-02',
            'C,2000-01-03<->D,2000-01-04',
            'E,2000-01-05<->F,2000-01-06',
            'G,2000-01-07<->H,2000-01-08',
            'A,2000-01-01<->C,2000-01-03',
            'B,2000-01-02<->D,2000-01-04',
            'B,2000-01-02<->F,2000-01-06',
            'B,2000-01-02<->H,2000-01-08'
        ]
        expected = {1: {'friends':[2,3], 'id':1, 'name':"A", 'date_of_birth':datetime.date(2000,1,1)},
                    2: {'friends':[1,4,6,8], 'id':2, 'name':"B", 'date_of_birth':datetime.date(2000,1,2)},
                    3: {'friends':[4,1], 'id':3, 'name':"C", 'date_of_birth':datetime.date(2000,1,3)},
                    4: {'friends':[3,2], 'id':4, 'name':"D", 'date_of_birth':datetime.date(2000,1,4)},
                    5: {'friends':[6], 'id':5, 'name':"E", 'date_of_birth':datetime.date(2000,1,5)},
                    6: {'friends':[5,2], 'id':6, 'name':"F", 'date_of_birth':datetime.date(2000,1,6)},
                    7: {'friends':[8], 'id':7, 'name':"G", 'date_of_birth':datetime.date(2000,1,7)},
                    8: {'friends':[7,2], 'id':8, 'name':"H", 'date_of_birth':datetime.date(2000,1,8)}}
        observed = new_dict_no_history(convert_lines_to_friendships(line),True)
        assert dict_equal(expected,observed), f'Expected convert_lines_to_friendships({line}) == \n{expected}; got\n {observed}'

new_post_cases = {
    "people_in": [
        {'friends': [1,4,8,10], 'history':[], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(1975, 11, 5)},
        {'friends': [1,4,8,10], 'history':[("old item",2,[]),("middle item",2,[])], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(1975, 11, 5)},
        {'friends': [1,4,8,10], 'history':[("old item",2,[]),("middle item",2,[])], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(1975, 11, 5)},
        {'friends': [1,4,8,10], 'history':[("old item",2,[]),("middle item",2,[])], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(1975, 11, 5)},
        {'friends': [1,4,8,10], 'history':[("old item",2,[]),("middle item",2,[])], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(1975, 11, 5)},
        {'friends': [1,4,8,10], 'history':[("old item",2,[]),("middle item",2,[])], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(1975, 11, 5)},
        {'friends': [1,4,8,10], 'history':[("old item",2,[]),("middle item",2,[])], 'id': 2, 'name': 'X', 'date_of_birth': datetime.date(1975, 11, 5)},
    ],
    "people_in_base":[],
    "post_in": [
        ["hello world",[]],
        ["new item1",[]],
        ["new item2",[1]],
        ["new item3",[4]],
        ["new item4",[4,10]],
        ["new item5",[2,4,6,8,10]],
        ["new item6",[2,3,5,9]],
    ],
    "expected": [
        [("hello world",2,[])],
        [("old item",2,[]),("middle item",2,[]),("new item1",2,[])],
        [("old item",2,[]),("middle item",2,[]),("new item2",2,[1])],
        [("old item",2,[]),("middle item",2,[]),("new item3",2,[4])],
        [("old item",2,[]),("middle item",2,[]),("new item4",2,[4,10])],
        [("old item",2,[]),("middle item",2,[]),("new item5",2,[4,8,10])],
        [("old item",2,[]),("middle item",2,[]),("new item6",2,[])],
    ]
}
new_post_cases["people_in_base"] = copy.deepcopy(new_post_cases["people_in"])
get_history_case = lambda case : new_post_cases["people_in"][case]['history']
history_matches_expected = lambda case : all([(get_history_case(case)[i] == new_post_cases["expected"][case][i]) for i in range(len(get_history_case(case)))])
run_new_post = lambda case : new_post(new_post_cases["post_in"][case][0],new_post_cases["people_in"][case],new_post_cases["post_in"][case][1])
return_matches_expected = lambda case : run_new_post(case) == new_post_cases["expected"][case][-1]
test_new_post_case = lambda case : True if (return_matches_expected(case) and history_matches_expected(case)) else f'Expected new_post({new_post_cases["post_in"][case][0]},\n{new_post_cases["people_in_base"][case]},\n{new_post_cases["post_in"][case][1]})\n == {new_post_cases["expected"][case]} but got: {get_history_case(case)}'
class new_post_test(unittest.TestCase):
    def testNoTagValidEmpty(self):
        R = test_new_post_case(0)
        assert R == True, R

    def testNoTagValid(self):
        R = test_new_post_case(1)
        assert R == True, R

    def testTagValidStart(self):
        R = test_new_post_case(2)
        assert R == True, R

    def testTagValidMid(self):
        R = test_new_post_case(3)
        assert R == True, R
    def testTagValidMany(self):
        R = test_new_post_case(4)
        assert R == True, R
    def testTagMixedMany(self):
        R = test_new_post_case(5)
        assert R == True, R
    def testTagInvalidOnly(self):
        R = test_new_post_case(6)
        assert R == True, R

birthday_post_cases = {
    "people_in": {
        1: {'friends':[2,3], 'id':1, 'name':"A", 'date_of_birth':datetime.date(2000,1,1)},
        2: {'friends':[1,4,6,8], 'id':2, 'name':"B", 'date_of_birth':datetime.date(2000,1,2)},
        3: {'friends':[4,1], 'id':3, 'name':"C", 'date_of_birth':datetime.date(2000,1,3)},
        4: {'friends':[3,2], 'id':4, 'name':"D", 'date_of_birth':datetime.date(2000,1,4)},
        5: {'friends':[6], 'id':5, 'name':"E", 'date_of_birth':datetime.date(2000,1,5)},
        6: {'friends':[5,2], 'id':6, 'name':"F", 'date_of_birth':datetime.date(2000,1,6)},
        7: {'friends':[8], 'id':7, 'name':"G", 'date_of_birth':datetime.date(2000,1,7)},
        8: {'friends':[7,2], 'id':8, 'name':"H", 'date_of_birth':datetime.date(2000,1,8)},
        9: {'friends':[], 'id':9, 'name':"I", 'date_of_birth':datetime.date(2000,1,9)}
    },
    "dates":datetime.date(2000,1,11),
    "id_chose": [9,7,8,2,1],
    "expected":[[],[8],[7],[4,6,8],[]]
}
run_bday_case = lambda case : birthdays_within_a_week_of(birthday_post_cases["id_chose"][case],birthday_post_cases["people_in"],birthday_post_cases["dates"])
check_bday_case = lambda case : True if run_bday_case(case) == birthday_post_cases["expected"][case] else f'Expected birthdays_within_a_week_of({birthday_post_cases["id_chose"][case]},\n{birthday_post_cases["people_in"]},\n{birthday_post_cases["dates"]}) == {birthday_post_cases["expected"][case]}; but got {run_bday_case(case)}'

class birthdayPostTests(unittest.TestCase):
    def testNoFriends(self):
        R = check_bday_case(0)
        assert R==True,R
    def testOneFriendsWith(self):
        R = check_bday_case(1)
        assert R==True,R
    def testMultiFriendsSomeApply(self):
        R = check_bday_case(2)
        assert R==True,R
    def testMultiFriendsManyApply(self):
        R = check_bday_case(3)
        assert R==True,R
    def testMultiFriendsNoneApply(self):
        R = check_bday_case(4)
        assert R==True,R
if __name__=="__main__":
        unittest.main()
