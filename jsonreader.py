import json


def calculate_activity_duration(activity="any", year="any", month="any", week="any", date="any", day="any", hour="any"):
    # read data from a JSON file
    with open("pomodoro_report.json", "r") as f:
        data = json.load(f)

    # create a dictionary to store the total duration for each activity
    activity_duration = {}

    # loop through each dictionary in the list of data
    for d in data:
        # check if all the required key-value pairs are present in the dictionary
        if all(key in d for key in ["activity", "duration", "year", "month", "week", "date", "day", "hour"]):
            # check if the values for year, month, date, day, and hour match the specified values or "any"
            if (d["year"] == year or year == "any") and \
               (d["month"] == month or month == "any") and \
               (d["week"] == week or week == "any") and \
               (d["date"] == date or date == "any") and \
               (d["day"] == day or day == "any") and \
               (d["hour"] == hour or hour == "any"):
                # check if the activity matches the specified activity or "any"
                if activity == "any" or d["activity"] == activity:
                    # get the activity and duration values
                    activity_name = d["activity"]
                    duration = d["duration"]
                    # add the duration to the total for the activity
                    if activity_name in activity_duration:
                        activity_duration[activity_name] += duration
                    else:
                        activity_duration[activity_name] = duration

    # return the activity duration dictionary
    return activity_duration


print(calculate_activity_duration(activity="any",
                                  year="any",
                                  month="any",
                                  week="any",
                                  date="any",
                                  day="any",
                                  hour="any"))

"""
or 

import json

def calculate_activity_duration(filename, activity="any", year="any", month="any", week="any", date="any", day="any", hour="any"):
    with open(filename, "r") as f:
        data = json.load(f)
    total_duration = 0
    for d in data:
        if (not year or d.get("year", "any") == year) and \
           (not month or d.get("month", "any") == month) and \
           (not week or d.get("week", "any") == week) and \
           (not date or d.get("date", "any") == date) and \
           (not day or d.get("day", "any") == day) and \
           (not hour or d.get("hour", "any") == hour) and \
           (not activity or d.get("activity", "any") == activity):
            total_duration += d["duration"]
    return total_duration

whatever works I guess
"""