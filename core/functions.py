from PyInquirer import print_json, prompt
import json
from prompt_toolkit.validation import ValidationError, Validator

class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



def getInput(questions, value):
    try:
        answers = prompt(questions)
        y = json.dumps(answers)
        x = json.loads(y)
        return x[value]
    except:
        return

def retriveInput(answers, value):
    try:
        y = json.dumps(answers)
        x = json.loads(y)
        return x[value]
    except:
        return

questions = [
    {
        'type': "list",
        'name': "startAction",
        'message': "What would you like to do today?",
        'choices': ['Launch Meeting', 'Create Entry', 'Remove Entries', "List Entries","Setup", "Misc", "Exit"]
    }
]

listType = [
    {
    'type': "list",
    'name': "modifyType",
    'message': "What would you like to list?",
    'choices': ['Meetings', "Notes"]
    }
]

modifyEntry = [
    {
    'type': "list",
    'name': "modifyType",
    'message': "What would you like to Remove?",
    'choices': ['Remove Meetings', "Remove Notes"]
    }
]

searchMeeting = [
    {
    'type': "input",
    'name': "meetingQuery",
    'message': "Search Query: (Searching by period)"
    }
]

searchNote = [
    {
    'type': "input",
    'name': "noteQuery",
    'message': "Search Query: (Searching by note name)"
    }
]

confirmRemove = [
    {
    'type': "confirm",
    'name': "modifyAction",
    'message': "Are you sure you want to remove this?",
    "default": False
    }
]

numberValue = [
    {
    'type': 'input',
    'name': 'quantity',
    'message': 'How many classes do you have in total?',
    'validate': NumberValidator,
    'filter': lambda val: int(val)
    }
]

classSetup = [
    {
    'type': 'input',
    'name': 'period',
    'message': 'When do you have this class? (Ex: 1A)'
    },

    {
    'type': 'input',
    'name': 'day',
    'message': 'What day do you have this class? (Block Scheduling)'
    },

    {
    'type': 'input',
    'name': 'link',
    'message': 'Enter the meeting link!'
    },

    {
    'type': 'input',
    'name': 'timeStart',
    'message': 'When does this class start? (24 Hour Time Format)'
    },
]

NoteSetup = [
    {
    'type': 'input',
    'name': 'noteName',
    'message': 'Enter a Name for this Note:'
    },
    {
    'type': 'input',
    'name': 'noteContent',
    'message': 'Enter Content:'
    },
    {
    'type': 'confirm',
    'name': 'passwordProtected',
    'message': 'Should this note be password protected?',
    'default': False
    }
]

NotePassword = [
    {
    'type': 'password',
    'name': 'password',
    'message': 'Enter a Password for this Note:'
    }
]

LaunchMeeting = [
    {
    'type': 'input',
    'name': 'periodRequest',
    'message': 'Enter Period to Launch:'
    }
]