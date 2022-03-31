import random


# This code template was taken from the Assigment "Example Bots"
def Alice(a, b = None):
    return "I think {} sounds awesome!".format(a + "ing")

def Bob(a, b = None):
    if b is None:
        return "Not sure about {}. Don't I get a choice?".format(a + "ing")
    return "Sure, both {} and {} seems ok to me".format(a, b + "ing")

def Dora(a, b = None):
    alternatives = ["coding", "singing", "sleeping", "fighting"]
    b = random.choice(alternatives)
    res = f"Yea, {a}ing is an option. Or we could do some {b}."
    return res

def Chuck(a, b = None):
    action = a + "ing"
    bad_things = ["fighting", "bickering", "yelling", "complaining"]
    good_things = ["singing", "hugging", "playing", "working", "eating", "crying", "sleeping", "coding"]

    if action in bad_things:
        return "YESS! Time for {}".format(action)
    elif action in good_things:
        return "What? {} sucks. Not doing that.".format(action)
    return "I don't care!"

#this function will allows the user to communicate and have a coversation with bots
def User(a, b = None):
    print(a)
    return input ("What is your response?: ")


# This code template was taken from the Assigment "Example Bots"