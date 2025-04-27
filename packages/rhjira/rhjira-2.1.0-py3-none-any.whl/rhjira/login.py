import keyring
import getpass
import os
import sys

from keyring.errors import NoKeyringError
from jira import JIRA, JIRAError
from rhjira import util


def login():

    # check the keyring first
    token = None
    try:
        token = keyring.get_password("rhjira", os.getlogin())
    except NoKeyringError as e:
        print("Warning: Unable to find a valid keyring (ex. seahorse).  Trying to use JIRA_TOKEN (less secure than keyring)....")

    if token == None or token == "":
        token = os.getenv("JIRA_TOKEN")
        if token == None or token == "":
            print(f"Error: JIRA_TOKEN not set")
            sys.exit(1)

    jira = JIRA(server="https://issues.redhat.com", token_auth=token)
    try:
        jira.myself()
        util.rhjiratax()
    except JIRAError as e:
        print(
            f"Jira myself test failed (possible permissions or login error): {e.status_code} {e.text}"
        )
        print("Suggestion: Verify that your Red Hat Jira token is valid.")
        sys.exit(1)

    return jira


def setpassword():
    token = getpass.getpass("Enter in token (hit ENTER to abort):")
    if token.strip() == "":
        print("No token entered ... aborting")
        sys.exit(1)

    username = os.getlogin()
    print(f"Attempting to save token to {username}'s keyring ....")
    keyring.set_password("rhjira", username, token)
    print("testing login with token ....")

    login()

    print(f"Login succeeded.  Token is saved in keyring as ('{username}' on 'rhjira').")
