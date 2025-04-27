import argparse
import sys

from datetime import datetime
from jira import JIRAError
from rhjira import login, util


def dict_to_struct(data):
    return type("", (object,), data)()


def dump_any(field, value):
    if value == None:
        return ""

    # customfield_12316840/"Bugzilla Bug"
    if field.id == "customfield_12316840":
        return value.bugid

    return value


def dump_user(field, user):
    return f"{user.displayName} <{user.emailAddress}>"


def dump_version(field, version):
    return version.name


def dump_component(field, component):
    return component.name


def dump_issuelink(field, issuelink):
    if issuelink.outwardIssue:
        return f"{issuelink.type.outward} https://issues.redhat.com/browse/{issuelink.outwardIssue.key}"
    else:
        return f"{issuelink.type.inward} https://issues.redhat.com/browse/{issuelink.inwardIssue.key}"


def dump_array(field, array):
    # customfield_12311840/"Need Info From"
    if field.id == "customfield_12311840":
        return dump_user(field, array)
    # customfield_12323140/"Target Version"
    if field.id == "customfield_12323140":
        return dump_version(field, array)
    # customfield_12315950/"Contributors"
    if field.id == "customfield_12315950":
        userstr = ""
        count = 0
        for cf in array:
            count += 1
            user = cf
            userstr = userstr + dump_user(field, user)
            if count != len(array):
                userstr = userstr + ", "
        return userstr

    if array == []:
        return ""

    if field.schema["items"] and field.schema["items"] != "worklog":
        retstr = ""
        count = 0
        for entry in array:
            count += 1
            match field.schema["items"]:
                case "component":
                    retstr = retstr + dump_component(field, entry)
                case "issuelinks":
                    retstr = retstr + dump_issuelink(field, entry)
                case "option":
                    retstr = retstr + dump_option(field, entry)
                case "worklog":
                    # currently not used in RH
                    return ""
                case "version":
                    retstr = retstr + dump_version(field, entry)
                case _:
                    print(f"PRARIT unhandled array {field.schema['items']}")
                    return ""
            if count != len(array):
                retstr = retstr + ", "
        return retstr

    return ""


def dump_securitylevel(field, security):
    return security.description


def dump_option(field, option):
    return option.value


def dump_optionwithchild(field, option):
    return f"{option.value} -  {valuse.child.value}"


def dump_votes(field, votes):
    return votes.votes


def dump_progress(field, progress):
    return f"{progress.progress}%"


def dump_watches(field, watches):
    if not watches.isWatching:
        return "0"
    return watches.watchCount


def dump_comment(field, comment):
    creator = dump_user({}, comment.author)
    timestamp = convert_jira_date(comment.created)
    return f'"Created by {creator} at {timestamp} :\\n{comment.body}\\n\\n"'


def dump_comments(field, comments):
    retstr = ""
    count = 0
    for comment in comments:
        count += 1
        retstr = retstr + dump_comment({}, comment)
        if count != len(comments):
            retstr = retstr + ", "
    return retstr


def convert_jira_date(datestr):
    date = datetime.strptime(datestr, "%Y-%m-%dT%H:%M:%S.%f%z")
    # 2024-09-03 11:34:05
    return date.strftime("%Y-%m-%d %H:%M:%S")


showcustomfields = True


def outputfield(field, data):
    if showcustomfields:
        print(f"FIELD[{field.name}|{field.id}]:", data)
    else:
        print(f"FIELD[{field.name}]:", data)


noescapedtext = True


def evaluatefield(field, value):
    schema = dict_to_struct(field.schema)
    match schema.type:
        case "any":
            outputfield(field, dump_any(field, value))
        case "array":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, dump_array(field, value))
        case "date":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, convert_jira_date(value))
        case "datetime":
            # A subtlety of date and datetime seem to be that date
            # can be None.  datetime is used for fields that MUST
            # have a date as far a I can tell.  The None check
            # below may not be strictly necessary?
            if value is None:
                outputfield(field, "")
            else:
                date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")
                # 2024-09-03 11:34:05
                outputfield(field, date.strftime("%Y-%m-%d %H:%M:%S"))
        case "issuelinks":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, dump_issuelink(field, value))
        case "issuetype":
            outputfield(field, value)
        case "number":
            if value is None:
                outputfield(field, "0")
            else:
                outputfield(field, value)
        case "sd-approvals":
            # cannot find any tickets with this field set.  For now
            # just return an empty string
            outputfield(field, "")
        case "sd-customerrequesttype":
            # cannot find any tickets with this field set.  For now
            # just return an empty string
            outputfield(field, "")
        case "sd-servicelevelagreement":
            # cannot find any tickets with this field set.  For now
            # just return an empty string
            outputfield(field, "")
        case "securitylevel":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, dump_securitylevel(field, value))
        case "string":
            if value is None:
                outputfield(field, "")
            else:
                if noescapedtext:
                    outputfield(field, value)
                else:
                    outputfield(field, value.replace("\n", "\\n"))
        case "timetracking":
            # Not currently used.  Will have to adjust this code if it is used.
            outputfield(field, "")
        case "option":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, dump_option(field, value))
        case "option-with-child":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, dump_optionwithchild(field, value))
        case "priority":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, value)
        case "project":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, value)
        case "progress":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, dump_progress(field, value))
        case "resolution":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, value)
        case "status":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, value)
        case "user":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, dump_user(field, value))
        case "version":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, dump_version(field, value))
        case "votes":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, dump_votes(field, value))
        case "watches":
            if value is None:
                outputfield(field, "")
            else:
                outputfield(field, dump_watches(field, value))
        case "comments-page":
            outputfield(field, dump_comments(field, value.comments))
        case _:
            print(
                f"ERROR undefined field type FIELD[{field.name}|{field_name}]: ",
                schema.type,
                value,
            )


def dump(jira):
    # handle arguments
    sys.argv.remove("dump")
    parser = argparse.ArgumentParser(description="Dump jira issue variables.")
    parser.add_argument("ticketID", nargs=argparse.REMAINDER)
    parser.add_argument(
        "--fields", type=str, help="specify a comma-separated list of fields for output"
    )
    parser.add_argument(
        "--noescapedtext",
        action="store_true",
        help="show dump text (ie, no escaped characters)",
    )
    parser.add_argument(
        "--showcustomfields",
        action="store_true",
        help="show the customfield IDs and the customfield names",
    )
    parser.add_argument(
        "--showemptyfields",
        action="store_true",
        help="show all fields including those that are not defined for this issue",
    )
    parser.add_argument("--json", action="store_true", help="dump issue in json format")
    args = parser.parse_args()

    userfields = args.fields
    if args.fields and len(args.fields) != 0:
        userfields = args.fields.split(",")
    global noescapedtext
    noescapedtext = args.noescapedtext
    global showcustomfields
    showcustomfields = args.showcustomfields
    showemptyfields = args.showemptyfields

    if len(args.ticketID) != 1:
        print("Error: ticketID not clear or found (ticketID must be last argument)")
        sys.exit(0)

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

    if args.json:
        util.dumpissue(issue)
        sys.exit(0)

    try:
        jirafields = jira.fields()  # this is all fields across Jira (not just project)
        util.rhjiratax()
    except JIRAError as e:
        print(f"Jira fields lookup failed: {e.status_code} {e.text}")
        sys.exit(1)

    # generate a list of fields
    fields = []
    for fielddict in jirafields:
        field = dict_to_struct(fielddict)
        if userfields and len(userfields) != 0:
            if field.id not in userfields:
                continue
        fields.append(field)

    # output the fields
    for field in fields:
        if field.id in issue.raw["fields"]:
            if issue.raw["fields"][field.id]:
                try:
                    value = getattr(issue.fields, field.id)
                except AttributeError:
                    value = ""

                evaluatefield(field, value)
            else:
                if showemptyfields:
                    outputfield(field, "")
        else:
            # For some reason the issue key field is not populated with a value.
            if field.id == "issuekey":
                outputfield(field, ticketID)
                continue
            if showemptyfields:
                outputfield(field, "")
