"""
Travis Robinson
Oregon State
Computer Science
travisrobinson2006@gmail.com
robitrav@oregonstate.edu
"""

"""
Main function for Victoria--voice controlled personal assistant
Program is currently a work in progress, written for fun.
I used Python for this because I've never used Python before and it seemed like a good way to learn, in
addition to easy-to-use modules for speech recognition
"""

"""
Current functionality:
Calculator
Web-based browser search
Directory search of computer
"""


#import modules
import imp
send_message = imp.load_source('send_message','./message_lib/send_message.py')
import user_interaction
calculator = imp.load_source('calculator','./calculator_lib_files/calculator.py')
search_lib = imp.load_source('search_lib','./search/search_lib.py')


#program main--excepts no inputs from command line--will get input through user interactions
def main():
    print(user_interaction.getRandomLine("character_building/greetingText"))#print random greeting
    print "Just fyi, there may be some limited functionality in some places. Especially with regards to commands involving searching the computer"
    command = [0]
    while(1):
        command = [0] #prevent list from going out of range below if nothing input
        command = user_interaction.get_user_input()#retrieve user input via voice command
        command = user_interaction.parse_into_command(command)#parse user input into understandable commands
        print command#for error controlling only
        if command[0] == "text" or command[0] == "email":#send message
            send_message.message_sender(command)
        elif command[0] == "calculate":#use calculator
            print calculator.calculate(command[1:len(command)])
        elif command[0] == "internet":#search internet; will open browser window
            search_lib.search_web(command[1],command[2:len(command)])
        elif command[0] == "computer":#search computer; will print list of file locations of search
            print "searching for ", command[1].lower()
            print search_lib.search_computer(command[1].lower().encode('ascii','ignore'))
        elif command[0] == "invalidCommand":#invalid, try again
            print "I'm sorry, I didn't understand"
        elif command[0] == "terminate":#to end program say goodbye
            break
        print "Alright, is there anything else I can do?"
    print "Cool beans, yo! I'll talk to you later!"



main()
