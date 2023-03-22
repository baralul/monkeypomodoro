import json


activity = "any"
year = "any"
month = "any"
week = "any"
date = "any"
day = "any"
hour = "any"


def calculate_activity_duration(act="any", yea="any", mon="any", wee="any", dt="any", dy="any", hou="any"):
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
            if (d["year"] == yea or yea == "any") and \
               (d["month"] == mon or mon == "any") and \
               (d["week"] == wee or wee == "any") and \
               (d["date"] == dt or dt == "any") and \
               (d["day"] == dy or dy == "any") and \
               (d["hour"] == hou or hou == "any"):
                # check if the activity matches the specified activity or "any"
                if act == "any" or d["activity"] == act:
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


output = (calculate_activity_duration(act=activity, yea=year, mon=month, wee=week, dt=date, dy=day, hou=hour))

print(output)


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