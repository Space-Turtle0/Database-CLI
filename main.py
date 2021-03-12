from __future__ import print_function, unicode_literals
from pprint import pprint
import json
from types import LambdaType
from prompt_toolkit.shortcuts import confirm
from pygments.lexer import default
import regex
from prompt_toolkit.validation import ValidationError, Validator
from PyInquirer import print_json, prompt
from core import database
import subprocess
import sys

from core.functions import *

while True:
    values = getInput(questions, "startAction")

    if values == "Setup":
        num = getInput(numberValue, "quantity")
        for x in range(num):
            answers = prompt(classSetup)

            #Get Independent Values: 
            period = retriveInput(answers, "period")
            day = retriveInput(answers, "day")
            link = retriveInput(answers, "link")
            timeStart = retriveInput(answers, "timeStart")

            try:
                database.db.connect(reuse_if_open=True)
                q: database.MeetingSession = database.MeetingSession.create(period = period, day = day, timeStarted = timeStart, link = link)
                q.save()
            except Exception as e:
                print(f"{bcolors.WARNING}WARNING: Unable to register details!{bcolors.ENDC}\n{e}")

            else:
                print(f"{bcolors.OKGREEN}INFO: Registered Details for{bcolors.ENDC} {period}!")
                database.db.close()
        
        print(f"{bcolors.OKGREEN}INFO:{bcolors.ENDC} Completed Meeting Setup!")
    
    elif values == "Create Entry":
        answers = prompt(NoteSetup)

        #Get Independent Values: 
        noteName = retriveInput(answers, "noteName")
        noteContent = retriveInput(answers, "noteContent")
        passwordProtected = retriveInput(answers, "passwordProtected")

        if passwordProtected == True:
            answers = prompt(NotePassword)
            password = retriveInput(answers, "password")

            try:
                database.db.connect(reuse_if_open=True)
                q: database.Notes = database.Notes.create(noteName = noteName, note = noteContent, passwordProtected = password)
                q.save()
            except Exception as e:
                print(f"{bcolors.WARNING}WARNING: Unable to register details!{bcolors.ENDC}\n{e}")

            else:
                print(f"{bcolors.OKGREEN}INFO: Registered Details for{bcolors.ENDC} {noteName}!")
                database.db.close()

        else:
            try:
                database.db.connect(reuse_if_open=True)
                q: database.Notes = database.Notes.create(noteName = noteName, note = noteContent)
                q.save()
            except Exception as e:
                print(f"{bcolors.WARNING}WARNING: Unable to register details!{bcolors.ENDC}\n{e}")

            else:
                print(f"{bcolors.OKGREEN}INFO: Registered Details for{bcolors.ENDC} {noteName}!")
                database.db.close()

    elif values == "Launch Meeting":
        periodRequest = getInput(LaunchMeeting, "periodRequest")
        try:
            MeetingDetails: database.MeetingSession = database.MeetingSession.select().where(database.MeetingSession.period == periodRequest).get()
            subprocess.run(["open", f'{MeetingDetails.link}'])
        except Exception as e:
            print(f"{bcolors.WARNING}WARNING: Unable to launch meeting!{bcolors.ENDC}\n{e}")
        else:
            pass

    elif values == "Remove Entries":
        optionType = getInput(modifyEntry, "modifyType")
        if optionType == "Remove Meetings":

            query = getInput(searchMeeting, "meetingQuery")

            CONFIRM_REMOVE = getInput(confirmRemove, "modifyAction")
            if CONFIRM_REMOVE == True:
                try:
                    MeetingDetails: database.MeetingSession = database.MeetingSession.select().where(database.MeetingSession.period == query).get()
                    MeetingDetails.delete_instance()
                except Exception as e:
                    print(f"{bcolors.WARNING}WARNING: Unable to launch meeting!{bcolors.ENDC}\n{e}")
                else:
                    pass
            else:
                break

        else:
            query = getInput(searchNote, "noteQuery")

            CONFIRM_REMOVE = getInput(confirmRemove, "modifyAction")
            if CONFIRM_REMOVE == True:
                try:
                    NoteDetails: database.Notes = database.Notes.select().where(database.Notes.noteName == query).get()
                    NoteDetails.delete_instance()
                except Exception as e:
                    print(f"{bcolors.WARNING}WARNING: Unable to launch meeting!{bcolors.ENDC}\n{e}")
                else:
                    pass
            else:
                break
    
    elif values == "List Entries":
        listType = getInput(listType, "modifyType")
        if listType == "Meetings":
            totalMeets = []
            for meet in database.MeetingSession:
                totalMeets.append(f"Period: {meet.period} > Link: {meet.link}")

            totalOutput = '\n'.join(totalMeets)
            print(totalOutput)
                
        else:
            totalNotes = []
            query = database.Notes.select().where(database.Notes.passwordProtected == "FALSE")
            for note in query:
                totalNotes.append(f"Name: {note.noteName} > Content: {note.note}")

            totalOutput = '\n'.join(totalNotes)

            lockedNotes = []
            query = database.Notes.select().where(database.Notes.passwordProtected != "FALSE")
            for note in query:
                lockedNotes.append(f"Name: {note.noteName}")

            totalOutput2 = '\n'.join(lockedNotes)

            print("OPEN NOTES:")
            print(totalOutput)


            print(f"\nPASSWORD LOCKED NOTES:\n{totalOutput2}\n")

    elif values == "Exit":
        sys.exit(0)




   






        
