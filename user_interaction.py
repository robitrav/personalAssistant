"""
Travis Robinson
Oregon State
Computer Science
travisrobinson2006@gmail.com
robitrav@oregonstate.edu
"""

"""
User interaction module for Victoria--voice controlled personal assistant
This modules purpose is to recognize user speech, to parse user speech into commands, and to provide feedback to user
(user feedback note: currently a work in progress, ultimately there will be text files that contain possible replies (greeting messages, termination messages, error messages, etc)
that will be randomly selected as needed. This is currently not implemented program wide
"""

#import assorted libraries and modules
import imp
from random import randint
import linecache
import speech_recognition as sr

calculator = imp.load_source('calculator','./calculator_lib_files/calculator.py')
from calculator import operators
from calculator import scale_units
from calculator import operators_english

search_lib = imp.load_source('search_lib','./search/search_lib.py')
from search_lib import available_browsers

contact_data_retrievers = imp.load_source('contact_data_retrievers','./contacts/contact_data_retrievers.py')
from contact_data_retrievers import retrieve_contact_name

#key words for command parsing; use as globals so that they can be accessed by other modules
computer_search_keyword = ["computer"]
web_search_keyword = ["web","internet","online"]
terminate_keyword = ["goodbye","shutdown","terminate","no"]
setup_keyword = ["setup","set"]
message_keyword = ["send","message","text","email"]
valid_search_method_keyword = ["text","email"]
search_keyword = ["find","what","what's","search","look"]
calculate_keyword = operators


"""
Description: This function retrieves user input via microphone and turns it into text. Uses google to transcribe-consider switching to cmusphinx so as not to require internet
for transcription
Input: N/A
Output: User speech transcribed into text
Note: Speech Recognition courtesy of https://pypi.python.org/pypi/SpeechRecognition/
"""
def get_user_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        userInput = r.recognize_google(audio)
    except:
        userInput = "comprehensionException"
    return userInput;

"""
Description: This function is to clarify user intentions when message command is given-ie if user says message, should it be text or email
Input: User command as text
Output: Either original command (if command == text/email) else altered command
"""
def clarify_message_command(command):
    if command[0] != "text" and command[0] != "email":
        print "Sure I can do that! Should it be text or email?"
        command[0] = get_user_input()
    while command[0] != "text" and command[0] != "email":
        print "I'm sorry. Currently I can only send messages via text and email."
        command[0] = get_user_input()
    return command

"""
Description: This function is to clarify user intentions when search command is given-ie if user says search, should it be internet or computer, browswer type
Input: User command as text
Output: Either original command (if command == text/email) else altered command
"""
def clarify_search_command():
    computer_search_keyword = ["computer"]
    web_search_keyword = ["web","internet","online",]
    print "Yeah, no problem!"
    print "Quick question: should I search online or on the computer?"
    while (1):
        response = get_user_input().split()
        for i in response:
            if i in computer_search_keyword:
                return ["computer"]
            elif i.lower() in available_browsers:
                return ["internet",i]
            elif i in web_search_keyword:
                print "Okay! What search engine should I use?"
                while (1):
                    engine = get_user_input().split()
                    for i in engine:
                        #print engine
                        if i.lower() in available_browsers:
                            return ["internet",i]
                    print "I'm sorry, I'm not familiar with that engine. Is there another I can use?"
        print "I'm sorry, where should I search again?"

"""
Description: receives contact name from calling function, checks its validity (presence in contacts list), if invalid requests new user input, returns name to calling function
Input: Contact name from calling function
Output: Contact name-whether as is or modified depending on validity
"""
def clarify_contact_name(name):
    while name[len(name)-1] == "notValidContact":#in this case, user has asked to message somebody who is not in the contacts list
        print "Invalid name requested\n", "To Do: Add functionality so user can add a contact from here if desired"
        print "I'm sorry...who I was I supposed to send this to again?"
        name = get_user_input().split()
        name = retrieve_contact_name(name)
        print name
    return name

"""
Description: Retrieves random line from input text file; used for variation in user interactions***not implemented program wide yet***
Input: File name appropriate for use, such as greeting file or goodbye file
Output: Random line from file
"""
def getRandomLine(fileName):
    with open(fileName) as f:
        for lineCount, l in enumerate(f):
            pass
        lineCount = lineCount+1
        lineToRead = randint(1,lineCount)
        line = linecache.getline(fileName,lineToRead)
        linecache.clearcache()
        return(line)

"""
Description: Turns user input into program commands-which can then be used to call on appropriate modules
Input: user speech as text
Output: command for main function to act on
Note: There's a lot of improvement that can be done here
"""
def parse_into_command(userInput):
    #flags to indicate what needs to be done
    terminate_command = 0
    setup_command = 0
    message_command = 0
    search_command = 0
    calculate_command = 0

    command = []
    split_string = userInput.split(" ")

    #replace english names of math operators with their symbols
    for i in split_string:
        for sublist in operators_english:
            if i in sublist:
                split_string[split_string.index(i)] = operators[sublist.index(i)]
                break

    for i in split_string:
        if i in terminate_keyword:#send terminate command to close program
            return ["terminate"]
        elif i in message_keyword:#set message flag
            if message_command != 1:
                command.append(i)
                message_command = 1
            else:
                if i in valid_search_method_keyword:
                    command[0] = i
           #break
        elif i in calculate_keyword:#set calculate flag
            command.append("calculate")
            calculate_command = 1
            #break
        elif i in search_keyword:#set search flag
            search_command = 1
    if message_command == 1:#clarify message command, add contact name onto it clarify_contact_name notValidContact retrieve_contact_name
        command = clarify_message_command(command) + clarify_contact_name(retrieve_contact_name(split_string[1:len(split_string)]))
    elif calculate_command == 1:#check this first first-else we may have situation where depending on phrasing of user they may do search when they want calculate
        #-can be avoided by checking calculate command before search
        for i in split_string:
            try:
                command.append(int(i))
            except:
                if i in calculate_keyword or i in scale_units or isinstance(i,(int,long)):
                    command.append(i)
    elif search_command == 1:
        for j in split_string:
            if j.lower() in available_browsers:#if command includes searcg engine, we don't need to clarify, we know they want a browser search
                command.append("internet")
                command.append(j)
                break
            elif j.lower() in computer_search_keyword:#if they include one of these key words, also no need to clarify
                command.append("computer")
                break
        if len(command) == 0:#if we make to here, we don't know what kind of search is wanted, need to clarify
            command = clarify_search_command()
        if command[0] == "internet":
            command = command + split_string
            return command
        elif command[0] == "computer":
            for j in split_string:
                if j == "for" or j == "find":#attempt to strip extraneous phrasing; it'll mess with the computer search-more work likely needed for this
                    command.append(split_string[split_string.index(j)+1])
            if len(command) < 2:
                print "I'm sorry. What should I be searching for again?"
                response = get_user_input()
                command.append(response)
    elif len(command) < 1:#let user know they gave a bad command--possible add clarify function here to get users intention?
        command.append("invalidCommand")
    return command
