"""
Travis Robinson
Oregon State
Computer Science
travisrobinson2006@gmail.com
robitrav@oregonstate.edu
"""

"""
Message sending module for Victoria--voice controlled personal assistant
This module contains the needed functions for writing and sending emails, to an email address or phone number
Phone/email info stored in the contacts module.
"""

"""
Note: Retrieve number function needs some error controls for when user only provides a first name--what if we have multiple people with that name?
"""
#use phone_number + gateway to send message to phone number; cheap alternative to using twilio, white pages, or similar service
gateway_carrier_email = [
    "@mms.alltelwireless.com",
    "@mms.att.net",
    "@myboostmobile.com",
    "@mms.cricketwireless.net",
    "@msg.fi.google.com",
    "@text.republicwireless.com",
    "@pm.sprint.com",
    "@tmomail.net",
    "@mms.uscc.net",
    "@vzwpix.com",
    "@vmpix.com"
]

#gateway names used to retrieve proper gateway email
gateway_carrier_name = [
    "Alltel",
    "AT&T",
    "Boost Mobile",
    "Cricket Wireless",
    "Project Fi",
    "Republic Wireless",
    "Sprint",
    "T-Mobile",
    "US Cellular",
    "Verizon Wireless",
    "Virgin Mobile"
]

#file name/path of contacts, as well as column locations within contacts list-placed here for ease of alteration should need arise
fileName = "contacts\contact_data"
first_name_location = 0
last_name_location = 1
phone_number_location = 2
carrier_location = 3
email_location = 4

"""
Description: This function receives a potential contact name (first or last) and verifies that the number is in contacts
Input: potential contact name
Output: an int, indicating whether the name is valid and its location in the contacts list
"""
def in_conatcts(potential_name):
    potential_name = potential_name.lower()
    with open(fileName) as file_to_search:
        lines = file_to_search.readlines()
    for i,line in enumerate(lines):
        line = line.split(",")
        if potential_name == line[first_name_location].lower():#first name matches up
            return 0
        if potential_name == line[last_name_location].lower():#last name matches up
            return 1
    return -1#no name matches up


"""
Description: This function receives a first name and returns a last name
Input: first name of contact
Output: last name of contact
"""
def retrieve_lname(fname):
    fname = fname.lower()
    with open(fileName) as file_to_search:
        lines = file_to_search.readlines()
    for i,line in enumerate(lines):
        line = line.split(",")
        if fname == line[first_name_location].lower():#first name matches up
            yield line[last_name_location]

"""
Description: This function receives a last name and returns a first name
Input: last name of contact
Output: first name of contact
"""
def retrieve_fname(lname):
    lname = lname.lower()
    with open(fileName) as file_to_search:
        lines = file_to_search.readlines()
    for i,line in enumerate(lines):
        line = line.split(",")
        if lname == line[last_name_location].lower():#last name matches up
            yield line[first_name_location]

"""
Description: This function recieves a list and searches it for contact names
Input: the user inputed command split from a string into a list
Output: the name of the contact
"""
def retrieve_contact_name(split_string):
    command = []
    message_recipient_fname = []#list of potential first names of recipients
    message_recipient_lname = []#list of potential last names of recipients
    for i in split_string:
        fname_or_lname = in_conatcts(i)#verify if i is a contact name, and whether it's a first or last name
        if fname_or_lname == 0 and i not in message_recipient_fname:#don't have same name in multiple times
            message_recipient_fname.append(i)
        elif fname_or_lname == 1 and i not in message_recipient_lname:#same as previous comment
            message_recipient_lname.append(i)
    if len(message_recipient_fname) == 1 and len(message_recipient_lname) == 1:#first and last name valid
        command = command + message_recipient_fname + message_recipient_lname
    elif len(message_recipient_fname) == 1 and len(message_recipient_lname) < 1:#retrieve last name
        potential_lnames = list(retrieve_lname(message_recipient_fname[0]))
        if len(potential_lnames) != 1:
            command.append("notValidContact")
        else:
            command = command + message_recipient_fname + potential_lnames
    elif len(message_recipient_fname) < 1 and len(message_recipient_lname) == 1:#retrieve first name
        potential_fnames = list(retrieve_fname(message_recipient_lname[0]))
        if len(potential_fnames) != 1:
            command.append("notValidContact")
        else:
            command = command + potential_fnames + message_recipient_lname
    else:#either not enough or too many of each name, attach notValidContact flag to command for calling function to act on
        #print "not right number of names"
        command.append("notValidContact")
    return command

"""
Description: retrieves phone number of contact based on name
Input: person who's number is desired
Output: persons phone number
"""
def retrieve_number(recipient):
    recipient = recipient.split(" ")
    with open(fileName) as file_to_search:
        lines = file_to_search.readlines()
    for i,line in enumerate(lines):
        line = line.split(",")
        if recipient[0].lower() == line[first_name_location].lower():#first name matches up
            if len(recipient) != 1:#user gave first and last name
                if recipient[1].lower() == line[last_name_location].lower():#now first and last match up
                    if line[carrier_location] in gateway_carrier_name:#we need to append the gateway address to the phone number
                        yield (line[phone_number_location]+gateway_carrier_email[gateway_carrier_name.index(line[carrier_location])])
                    else:#problem in the contact--we have an invalid carrier
                        yield "invalid_phone_number"
            else:#in this case, we only got a first name, so that's what we'll retrieve
                if line[carrier_location] in gateway_carrier_name:
                    yield (line[phone_number_location]+gateway_carrier_email[gateway_carrier_name.index(line[carrier_location])])
                else:
                    yield "invalid_phone_number"

"""
Description: retrieves email of contact based on name
Input: person who's email is desired
Output: persons email
"""
def retrieve_email(recipient):
    recipient = recipient.split(" ")
    with open(fileName) as file_to_search:
        lines = file_to_search.readlines()
    for i,line in enumerate(lines):
        line = line.split(",")
        if recipient[0] == line[first_name_location].lower():#first name matches up
            if len(recipient) != 1:#user gave first and last name
                if recipient[1] == line[last_name_location].lower():
                    yield line[email_location]
            else:#else user only gave first name
                yield line[email_location]
