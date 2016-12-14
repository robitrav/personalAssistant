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

#import modules
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from user_interaction import get_user_input

#from contacts import contact_data_retrievers
import imp
contact_data_retrievers = imp.load_source('contact_data_retrievers','./contacts/contact_data_retrievers.py')
#calculator = imp.load_source('calculator','../calculator_lib_files/calculator.py')
from contact_data_retrievers import retrieve_email
from contact_data_retrievers import retrieve_contact_name

#ease of change, will be altering this later to match email provided in user profile
my_email = "travisrobinson2006@gmail.com"

"""
Description: This is the main interface function for this module-it determines which message method to use and calls on them, sending the contact name to the appropriate persons
Input: command, along with contact name
Output: passes contact name on to appropriate message sending function
"""
def message_sender(command):
    if command[0] == "text":
        send_text(" ".join(command[1:len(command)]))
    elif command[0] == "email":
        send_email(" ".join(command[1:len(command)]))
    else:
        "I'm sorry, there seems to have been an error in sending this message. Currently I can send text or email"

"""
Description: This function receives the sender, recipient, subject and text of a message and sends it-if a text message is desired, calling function must append gateway to number
Input: sender, recipient, subject and text of a message
Output: message to either email address or phone number (passed to phone via carrier gateway)
"""
def send_message_helper(sender,recipient,message_subject,message_text):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(recipient)#using recipient as list right now, at some point would like to add ability to send group emails/messages
    msg['subject'] = message_subject

    body = message_text
    msg.attach(MIMEText(body,'plain'))


    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "axaqbqrprggfbvbz")
    text = msg.as_string()
    server.sendmail(sender, recipient, text)
    server.quit()

"""
Description: This function receives the message recipient, gets the desired message text from the user, and sends it to the text message calling function
Input: recipient
Output: calls on message_helper function to send text message, passing it the sender email, phone number, and message
Notes: This function is a copy/paste of the send_email function. Can easily be altered so one function performs both jobs--leaving as is, will be easy to change in future if
better text messaging system is used (ie twilio, etc) that wouldn't require the carrier gateway (services such as twilio though require payment; I'm okay with the cheap method right now)
"""
def send_text(recipient):
    numbers=list(contact_data_retrievers.retrieve_number(recipient.lower()))
    while len(numbers) > 1:
        print "There are too many people with that name: Please provide a first and last name for me to look for"
        recipient = get_user_input()
        numbers=list(contact_data_retrievers.retrieve_number(recipient.lower()))
    if len(numbers) < 1:
        print "I'm sorry. I couldn't find anyone with that name"
        return
    if "invalid_phone_number" in numbers:
        print "I'm sorry, that number is not valid. Please check with the contact again for a valid phone number or carrier"
    recipient_number = numbers[0]
    print "What's your message?"
    message = get_user_input()
    print "Your message is: " + message
    print "Is that correct?"
    verify = get_user_input()
    while verify == "no":
        print "I'm sorry! What's the message then?"
        message = get_user_input()
        print "Your message is: " + message
        print "Is that correct?"
        verify = get_user_input()
    print "Okay! Sending message now..."
    send_message_helper(my_email,recipient_number,"Sent by my Assistant",message)
    print "Message sent!"

"""
Description: This function receives the message recipient, gets the desired message text from the user, and sends it to the text message calling function
Input: recipient
Output: calls on message_helper function to send email, passing it the sender email, recipient email, and message
Notes: This function is a copy/paste of the send_text function. Can easily be altered so one function performs both jobs--leaving as is, will be easy to change in future if
better text messaging system is used (ie twilio, etc) that wouldn't require the carrier gateway (services such as twilio though require payment; I'm okay with the cheap method right now)
"""
def send_email(recipient):
    email=list(retrieve_email(recipient.lower()))
    while len(email) > 1:
        print "There are too many people with that name: Please provide a first and last name for me to look for"
        recipient = get_user_input()
        email=list(retrieve_number(recipient.lower()))
    if len(email) < 1:
        print "I'm sorry. I couldn't find anyone with that name"
        return
    recipient_email = email[0]
    print "What's your message?"
    message = get_user_input()
    print "Your message is: " + message
    print "Is that correct?"
    verify = get_user_input()
    while verify == "no":
        print "I'm sorry! What's the message then?"
        message = get_user_input()
        print "Your message is: " + message
        print "Is that correct?"
        verify = get_user_input()
    print "Okay! Sending message now..."
    send_message_helper(my_email,recipient_email,"Sent by my Assistant",message)
    print "Message sent!"
