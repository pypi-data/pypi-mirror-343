import argparse
import sys

from jira import JIRAError
from rhjira import login, util
from tabulate import tabulate


def list(jira):
    # handle arguments
    sys.argv.remove("list")
    parser = argparse.ArgumentParser(description="list issues")
    parser.add_argument(
        "--fields", type=str, help="specify a comma-separated list of fields for output"
    )
    parser.add_argument(
        "--numentries", type=int, help="maximum number of entries to return"
    )
    parser.add_argument(
        "--summarylength",
        type=int,
        help="Length of the summary string (default:50, do not truncate:0)",
    )
    parser.add_argument(
        "--noheader", action="store_true", help="do not display an output header"
    )
    parser.add_argument(
        "--nolinenumber", action="store_true", help="do not display leading line number"
    )
    parser.add_argument(
        "--rawoutput",
        action="store_true",
        help="do not make output pretty (useful for scripts)",
    )
    parser.add_argument("jqlstring", nargs=argparse.REMAINDER)

    args = parser.parse_args()

    if jira == None:
        try:
            jira = login.login()
        except JIRAError as e:
            print(f"Jira login failed: {e.status_code} {e.text}")
            sys.exit(1)

    try:
        issues = jira.search_issues(args.jqlstring)
        util.rhjiratax()
    except JIRAError as e:
        print(f"Jira search failed: {e.status_code} {e.text}")
        sys.exit(1)

    if len(issues) == 0:
        print("No issues found.")
        sys.exit(0)

    try:
        jirafields = jira.fields()  # this is all fields across Jira (not just project)
        util.rhjiratax()
    except JIRAError as e:
        print(f"Jira fields lookup failed: {e.status_code} {e.text}")
        sys.exit(1)

    # default is to show the issue key and the summary
    userselectedfields = ["key", "summary"]
    if args.fields:
        userselectedfields = args.fields.split(",")
        # issue key is always output
        userselectedfields.insert(0, "key")

    data = []
    count = 0
    issuekeyindex = 0  # used in table output
    for issue in issues:
        entry = []

        if not args.nolinenumber:
            issuekeyindex = 1
            entry.append(count)

        for field in userselectedfields:
            try:
                value = getattr(issue.fields, field)
                entry.append(value)
            except:
                try:
                    value = getattr(issue, field)
                    entry.append(value)
                except:
                    print(
                        f"Jira field {field} not found in issue or issue.fields structure."
                    )
                    sys.exit(1)

        data.append(entry)
        count += 1

    # issue.key is displayed as "Issue" in the first column
    userselectedfields[0] = "Issue"

    if not args.nolinenumber:
        userselectedfields.insert(0, "#")

    if args.numentries:
        data = data[: args.numentries]

    if args.rawoutput:
        for entry in data:
            print(*entry, sep="|", end="|\n")
        sys.exit(1)

    if args.noheader:
        print(tabulate(data, tablefmt="plain"))
    else:
        tableoutput = tabulate(data, headers=userselectedfields, tablefmt="plain")
        # tabulate uses the full string length to calculate column widths.
        # This causes weird table output when using the full URL length (see
        # below).  Instead, just search/replace the issuekey.
        for line in tableoutput.splitlines():
            issuekey = line.split()[issuekeyindex]
            print(
                line.replace(
                    issuekey,
                    f"\033]8;;https://issues.redhat.com/browse/{issuekey}\a{issuekey}\033]8;;\a\033[0;37m",
                )
            )
