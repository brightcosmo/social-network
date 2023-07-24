import datetime

def make_person(this_id: int, name: str, date_of_birth: datetime.date) -> dict:
    """Creates a new dictionary based on the person's properties.

    Args: 
        this_id: An integer ID assigned to the person.
        name: The name of the person as a string.
        date_of_birth: The date from the datetime library.
    
    Returns:
        A dictionary of the given input including 2 empty lists representing the person's friends and post history.
    """
    return {
        "friends": [],
        "history": [],
        "id": this_id,
        "name": name,
        "date_of_birth": date_of_birth,
    }


def find_friendX_inY(person_X: dict, person_Y: dict) -> int:
    """Checks if person X is in Y's friends list and finds the index.

    Args:
        person_X: A dictionary of a person to be checked for.
        person_Y: A dictionary of the person whose friends list is being checked.
    
    Returns: 
        The index of person X in person Y's friends list, or None if not found.
    """
    # if person X's ID in person Y's friends list, returns the index of X's ID
    if person_X["id"] in person_Y["friends"]:
        return person_Y["friends"].index(person_X["id"])
    return None


def make_friendship(person_X: dict, person_Y: dict):
    """Adds person X and person Y's ID's to each other's friends list.

    Args:
        person_X: A dictionary of the first person.
        person_Y: A dictionary of the second person.

    Returns:
        None
    """
    # checks that the two people are not the same
    if person_X["id"] != person_Y["id"]:
        # adds person Y's ID to person X's friends list, unless already there, and vice versa
        if person_Y["id"] not in person_X["friends"]:
            person_X["friends"].append(person_Y["id"])
        if person_X["id"] not in person_Y["friends"]:
            person_Y["friends"].append(person_X["id"])


def end_friendship(person_X: dict, person_Y: dict):
    """Removes the IDs of person X and Y from each other's friends list.

    Args:
        person_X: A dictionary of the first person.
        person_Y: A dictionary of the second person.

    Returns: 
        None
    """
    # if person Y's ID is in person X's friend list, remove person Y from person X's friends, and vice versa
    if person_Y["id"] in person_X["friends"]:
        del person_X["friends"][person_X["friends"].index(person_Y["id"])]
    if person_X["id"] in person_Y["friends"]:
       del person_Y["friends"][person_Y["friends"].index(person_X["id"])]


def birthday_within_X_days_of_Y(person: dict, days: int, comparison_date: datetime.date) -> bool:
    """Checks if the comparison date falls within the number of days of the given birthday.

    Args:
        person: The person's birthday to be checked.
        days: The number of days between the comparison_date and birthday.
        comparison_date: The date to be compared.

    Returns: 
        True if the birthday falls within days of comparison_date, and False otherwise.
    """
    # iterates through the previous year, same year, and next year of the comparison date 
    # checks if any of their dates are within the specified number of days
    for i in range(-1, 2):
        if abs((comparison_date - person["date_of_birth"].replace(year = comparison_date.year + i)).days) <= days:
            return True
    return False


def add_person(dict_of_people: dict, name: str, date_of_birth: datetime.date) -> int:
    """Adds a new person with a new ID according to the details input.

    Args:
        dict_of_people: The dictionaries of people using ID as key.
        name: The string name of the new person to be added.
        date_of_birth: The date of birth of the new person to be added.

    Returns:
        The new integer ID, which is the current highest ID + 1, or 1 if the dictionary was empty.
    """
    # obtains a list of IDs
    id_keys = list(dict_of_people.keys())
    # if not empty
    if len(id_keys):
        # sorts the list in reverse order to obtain the highest ID
        id_keys.sort(reverse = True)
        # creates a new ID which is the highest ID + 1
        new_id = int(id_keys[0]) + 1
        # calls the make_person function to add a person to the dict_of_people list
        dict_of_people[new_id] = make_person(new_id, name, date_of_birth)
        # returns the new ID
        return new_id
    # if empty, make a new person with ID 1
    else:
        dict_of_people[1] = make_person(1, name, date_of_birth)
        return 1


def get_person_by_id(dict_of_people: dict, find_id: int) -> dict:
    """Finds the ID in the dictionary and returns it.

    Args:
        dict_of_people: The dictionaries of people using ID as key.
        find_id: The ID to be searched for.
    
    Returns: 
        The dictionary belonging to the ID, or None if not found.
    """
    # if ID is in the dictionary
    if find_id in dict_of_people:
        # it returns the id of the dictionary of people 
        return dict_of_people[find_id]
    else:
        # if the id is not present in the dictionary it returns nothing
        return None


def convert_lines_to_friendships(lines: list) -> dict:
    """Reads a list of strings and processes the information into a dictionary.

    Args:
        lines: A list of strings with person details separated by arrows and commas.

    Returns: 
        A dictionary with the properties in the strings given.
    """
    def process_person_data(dict_of_people: dict, person_data: list) -> int:
        """Checks whether the ID in person_data is in dict_of_people, and if not, creates a new person based on the data.

        Args:
            dict_of_people: The dictionaries of people using ID as key.
            person_data: The details of the person.
        
        Returns:
            The integer ID in dict_of_people, or the new ID created if not found.
        """
        # splits the string to to separate the name and date of birth
        person_data = person_data.split(",")
        id_in_dict = None
        # iterates the given dictionaries
        for i in dict_of_people:
            # checks if any names from the dictionary match the name given
            if dict_of_people[i]["name"] == person_data[0]:
                id_in_dict = i
                break
        # if no match was found, create a new person and return its ID
        if not id_in_dict:
            return add_person(dict_of_people, person_data[0], datetime.date.fromisoformat(person_data[1]))
        # if a match was found, return the ID
        else:
            return id_in_dict
    

    # creates an empty dictionary representing all the people
    dict_of_people = {}
    # iterates the list of strings
    for i in lines:
        # splits the strings by an arrow
        line = i.split("<->")
        # checks if 2 people were in the line
        if len(line) == 2:
            friend_ids = []
            # each friend's data is processed and both are appended to the list
            for j in line:
                friend_ids.append(process_person_data(dict_of_people, j))
            # the two IDs are added to each other's friends list
            make_friendship(dict_of_people[friend_ids[0]], dict_of_people[friend_ids[1]])
        else:
        # only one person in the line, so data is only processed
            process_person_data(dict_of_people, line[0])
    # returns the dictionary of people 
    return dict_of_people


def new_post(content: str, owner: dict, tagged: list) -> tuple:
    """Appends a new post based on the parameters to the owner's post history.

    Args: 
        content: The content of the post as a string.
        owner: The dictionary of the person who is the owner of the post.
        tagged: The integer IDs of users to be tagged.

    Returns: 
        The post (represented as a tuple) created based on the content, owner ID, and tagged users.
    """
    i = 0
    # loops through the list of tagged people
    while i < len(tagged):
        # deletes the tagged person if not in the owner's friends list
        if tagged[i] not in owner["friends"]:
            del tagged[i]
        else:
            i += 1
    # creates the post as a tuple of the content, owner ID, and tagged users
    post = (content, owner["id"], tagged)
    # adds the post to the owner's history and returns it
    owner["history"].append(post)
    return post


def birthdays_within_a_week_of(person_id: int, people_dict: dict, comparison: datetime.date) -> list:
    """Checks whether birthdays of person_id's friends fall within 7 days of the comparison date.

    Args:
        person_id: The person's id who's friends list will be checked.
        people_dict: The dictionaries of people using ID as key.
        comparison: The date to be compared.

    Returns:
        The list of people's IDs whose birthday falls within 7 days of the comparisn date.
    """
    people_list = []
    # iterates the list of friends belonging to the person of the given ID
    for i in people_dict[person_id]["friends"]:
        # appends the friend's ID only if the birthday is within 7 days of the comparison date
        if birthday_within_X_days_of_Y(people_dict[i], 7, comparison):
            people_list.append(people_dict[i]["id"])
    return people_list


def make_birthday_posts(people_dict: dict, from_person_id: int, for_people_ids: list) -> list:
    """Creates a birthday post by from_person_id for all the IDs given in for_people_ids.
    
    Args:
        people_dict: The dictionaries of people using ID as key.
        from_person_id: The ID of the person making birthday posts for their friends.
        for_people_ids: A list of the people who have upcoming birthdays.
    
    Returns:
        A list of all the birthday posts.
    """
    post_list = []
    # iterates every ID given
    for i in for_people_ids:
        # creates a new birthday post and appends it to the list
        post_list.append(new_post(f"Happy birthday {people_dict[i]['name']}! Hope you have a good one!", people_dict[from_person_id], [i]))
    return post_list

if __name__ == "__main__":
    # creates a new list for the data of people
    people_data = []

    # accepts user input
    data = input()
    while data:
        # appends user input to the created list
        people_data.append(data)
        data = input()

    # prints the final list
    print(convert_lines_to_friendships(people_data))
