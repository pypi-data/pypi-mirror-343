import json
import os
import re
import shlex
import subprocess
import time


def convertdescription(description):
    return description.replace(r"\n", "\n")


def dumpissue(issue):
    print(json.dumps(issue.raw, indent=4))


def rhjiratax():
    # RH's Jira instance has a 2/second/node rate limit.  To avoid
    # this the code has to implement a 1 second delay at times.
    time.sleep(1)


def removecomments(intext):
    # remove all lines beginning with # (hash)
    outtext = re.sub(r"^#.*\n", "", intext, flags=re.MULTILINE)
    return outtext


def isGitRepo():
    try:
        with open(os.devnull, "w") as devnull:
            subprocess.check_call(
                ["git", "-C", "./", "rev-parse", "--is-inside-work-tree"],
                stdout=devnull,
                stderr=devnull,
            )
        return True
    except subprocess.CalledProcessError:
        return False


def geteditor():
    editor = os.environ.get("GIT_EDITOR") or os.environ.get("EDITOR") or "vi"
    if not editor:
        print("Could not determine editor.  Please set GIT_EDITOR or EDITOR.")
        sys.exit(1)

    return editor


def editFile(fileprefix, message):
    editor = geteditor()
    command = shlex.split(editor)

    if isGitRepo():
        workingdir = os.getcwd()
    else:
        workingdir = "/tmp"

    filename = workingdir + "/" + f"{fileprefix}_EDITMSG"

    command.append(filename)

    # prepopulate the file with message
    if message:
        with open(filename, "w") as file:
            file.write(message)

    # open the editor and save the contents in $filename
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Editor open failed with: {e}")
        os.remove(filename)
        sys.exit(1)

    # read the saved contents of $filename
    with open(filename, "r") as file:
        intext = file.read()

    # cleanup
    os.remove(filename)

    intext = removecomments(intext)
    intext = re.sub(r"^#.*\n", "", intext, flags=re.MULTILINE)

    return intext
