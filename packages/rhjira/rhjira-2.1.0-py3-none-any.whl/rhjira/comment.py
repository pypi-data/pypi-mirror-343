import argparse
import os
import sys

from jira import JIRAError
from rhjira import login, util


def comment(jira):
    # handle arguments
    sys.argv.remove("comment")
    parser = argparse.ArgumentParser(description="Comment on an RH jira ticket")
    parser.add_argument("-f", "--file", type=str, help="file containing comment")
    parser.add_argument(
        "--noeditor",
        action="store_true",
        help="when set the editor will not be invoked",
    )
    parser.add_argument("ticketID", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    if len(args.ticketID) != 1:
        print("Error: ticketID not clear or found (ticketID must be last argument)")
        sys.exit(1)

    filename = args.file
    noeditor = args.noeditor

    ticketID = args.ticketID[0]

    if jira == None:
        try:
            jira = login.login()
        except JIRAError as e:
            print(f"Jira login failed: {e.status_code} {e.text}")
            sys.exit(1)

    try:
        issue = jira.issue(ticketID)
        util.rhjiratax()
    except JIRAError as e:
        print(f"Jira lookup for {ticketID} failed: {e.status_code} {e.text}")
        sys.exit(1)

    editorText = "# Lines beginning with '#' will be ignored"
    if filename:
        # read the saved contents of $filename
        try:
            with open(filename, "r") as file:
                editorText = file.read()
        except Exception as error:
            print(f"Unable to open {args.template}")
            sys.exit(1)

    savedText = editorText
    if not args.noeditor:
        savedText = util.editFile("rhjira", editorText)
        if len(savedText) == 0:
            print("Empty comment buffer ... aborting.")
            os.Exit(1)

    try:
        jira.add_comment(ticketID, savedText)
    except JIRAError as e:
        print(f"Failed to add comment to {ticketID}: {e.status_code} {e.text}")
        print("")
        print("Comment text:")
        print(savedText)
        sys.exit(1)

    print(f"https://issues.redhat.com/browse/{ticketID}")
