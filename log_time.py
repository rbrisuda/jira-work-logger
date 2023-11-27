from jproperties import Properties
import getpass

import getopt
from datetime import datetime
from datetime import date
import calendar
import sys

from jira import JIRA

cal = calendar.Calendar()
today = datetime.today()
configs = Properties()


def open_jira(input_jira_password, jira_url, jira_user):
    return JIRA(server=jira_url, basic_auth=(jira_user, input_jira_password))


def log_time(jira, user, issue, timeSpent, log_date):
    jira.add_worklog(issue=issue, timeSpent=timeSpent, started=log_date, user=user)


def working_days_iterator(year, month):
    for day in cal.itermonthdays(year, month):
        if day != 0:
            day_date = date(year, month, day)
            if day_date.weekday() < 5:  # 5 is Saturday
                yield date(year, month, day)


def non_working_day(input_absences, date):
    if input_absences is None:
        return False
    day = date.day
    for input_absence in input_absences:
        left, right = resolve_range(input_absence)
        if left <= day <= right:
            return True
    return False


def get_working_days(input_month, input_skip_days, input_vacations, year):
    work_days = []
    for day in working_days_iterator(year, input_month):
        if not non_working_day(input_vacations, day) and not non_working_day(input_skip_days, day):
            work_days.append(datetime(day.year, day.month, day.day, today.hour, today.minute, today.second))
    return work_days


def get_vacation_days(input_month, input_vacations, year):
    vacation_days = []
    if input_vacations is None:
        return vacation_days

    for input_vacation in input_vacations:
        left, right = resolve_range(input_vacation)
        for day in range(left, right + 1):
            vacation_days.append(datetime(year, input_month, day, today.hour, today.minute, today.second))
    return vacation_days


def resolve_range(input_vacation):
    range_pair = input_vacation.split("-")
    left = int(range_pair[0])
    right = left if len(range_pair) == 1 else int(range_pair[1])
    return left, right


def load_config():
    with open('config.properties', 'rb') as config_file:
        configs.load(config_file)
    time_spent = configs['JIRA_WORK_MD'].data
    jira_url = configs['JIRA_URL'].data
    jira_user = configs['JIRA_USER'].data
    jira_work_issue = configs['JIRA_WORK_ISSUE'].data
    jira_absence_issue = configs['JIRA_ABSENCE_ISSUE'].data
    return jira_url, jira_user, jira_work_issue, jira_absence_issue, time_spent


def load_input(argv):
    year = today.year  # not input
    input_month = today.month
    input_vacations = None
    input_skip_days = None
    input_dry = False
    opts, args = getopt.getopt(argv, "m:v:s:d:", ["month=", "vacations=", "skip=", "dry="])
    for opt, arg in opts:
        if opt == '-h':
            print('log_time.py -m 12 -v 1,10-12 -s 17')
            sys.exit()
        elif opt in ("-m", "--month"):
            input_month = arg
        elif opt in ("-v", "--vacations"):
            input_vacations = arg.split(",")
        elif opt in ("-s", "--skip"):
            input_skip_days = arg.split(",")
        elif opt in ("-d", "--dry"):
            input_dry = arg == "true"
    input_jira_password = getpass.getpass()
    return int(year), int(input_month), input_vacations, input_skip_days, input_dry, input_jira_password


def main(argv):
    year, input_month, input_vacations, input_skip_days, input_dry, input_jira_password = load_input(argv)
    jira_url, jira_user, jira_work_issue, jira_absence_issue, time_spent = load_config()

    work_days = get_working_days(input_month, input_skip_days, input_vacations, year)
    vacation_days = get_vacation_days(input_month, input_vacations, year)

    jira = None
    if not input_dry:
        jira = open_jira(input_jira_password, jira_url, jira_user)

    print('Logging work:')
    for day in work_days:
        print(f'{day}: {time_spent}')
        if not input_dry:
            log_time(jira, jira_user, jira_work_issue, time_spent, day)

    print('Logging vacations:')
    for day in vacation_days:
        print(f'{day}: {time_spent}')
        if not input_dry:
            log_time(jira, jira_user, jira_absence_issue, time_spent, day)


if __name__ == "__main__":
    main(sys.argv[1:])
