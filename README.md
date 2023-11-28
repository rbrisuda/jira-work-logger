# jira-work-logger

Script for logging time in JIRA in bulks on monthly basis.
Script by default logs every single working day to single jira issue and can be configured to
skip vacation days (vacation days can are logged to different jira issue) or skip logging fully.

Usage:

1. Clone repository.
2. Configure properties in config.properties file which are static:

```properties
JIRA_URL=<<JIRA ORGANIZATION URL>>
JIRA_WORK_MD=<<WORKING TIME>>
JIRA_USER=<<JIRA USER NAME>>
JIRA_WORK_ISSUE=<<JIRA ISSUE FOR LOGGING TIME>>
JIRA_ABSENCE_ISSUE=<<JIRA ISSUE FOR LOGGING VACATIONS>>
```
Example:
```properties
JIRA_URL=https://jira-company-url.com
JIRA_WORK_MD=8h
JIRA_USER=username
JIRA_WORK_ISSUE=XYZ-564
JIRA_ABSENCE_ISSUE=XYZ-123
```

3. Run command to install required python modules: `pip install -r requirements.txt`
4. Run command for logging time: `python3 log_time.py`
5. Script asks to input password for JIRA, after ENTER time is logged on configured issues.
6. All other adjustments must be done in JIRA manually.

Available script options:

1. **-m** (optional, which month should be processed - number from 1 to 12, default is current month)
2. **-d** (optional, dry run - if `true` set, script prints only dates which would be logged, password can be invalid for testing)
3. **-v** (optional, vacations - comma separated list - e.g.: `1,15-20,25`. Supported single days and also ranges.)
4. **-s** (optional, skip - comma separated list which times are skipped for logging. Format the same like for vacations)

Example: 

```python3 log_time.py -m 12 -v 27-29 -s 25,26```

Provided command will log whole December into work issue except days: 27, 28 ,29 which are logged to absence issue,
days 25,26 are national holidays, logging is skipped.
