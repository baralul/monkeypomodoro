import time
import webbrowser
import pyautogui
import pygame
import datetime
import subprocess
import signal
import os
import json

# this is False now
pyautogui.FAILSAFE = False


def signal_handler():  # (signum, frame) < read more about this
    pass


def pomodoro(short_break_in_minute, long_break_in_minute, custom_tab1, custom_tab2):
    # get current time
    now = datetime.datetime.now()
    date = now.date().strftime("%d")
    month = now.date().strftime("%m")
    y, w, dy = now.isocalendar()

    with open("pomodoro_report.json", "r") as f:
        data = json.load(f)

    # read the number of minutes done today
    todayminute = 0
    for d in data:
        if all(key in d for key in ["year", "month", "date"]):
            if d["year"] == y and \
                    d["month"] == month and \
                    d["date"] == date:
                duration = d["duration"]
                todayminute += duration
    print(f"{todayminute}/250 Minutes done today!")

    #  prompting the user to enter the number of sessions
    while True:
        try:
            cycles = int(input("Number of session: "))
            break
        except ValueError:
            print("Please enter an integer")

    while True:
        try:
            duration = int(input("Duration of session in minute: "))
            break
        except ValueError:
            print("Please enter an integer")

    # Configuration I guess
    spotify = "https://open.spotify.com/"
    monkey_type = "https://monkeytype.com/"
    google_calendar = "https://calendar.google.com/calendar/u/0/r/week"
    duration_in_minute = duration * 60
    short_break = short_break_in_minute * 60
    long_break = long_break_in_minute * 60
    tasks = []
    suspend_in = 60

    for i in range(cycles):

        # initializes the pygame & make mp3 and its length variabless
        pygame.mixer.init()
        work_mp3 = pygame.mixer.Sound("monkeypomodoro/sounds/time_to_work.mp3")
        work_mp3_length = work_mp3.get_length()
        break_mp3 = pygame.mixer.Sound("monkeypomodoro/sounds/time_for_a_break.mp3")
        break_mp3_length = break_mp3.get_length()
        just_do_mp3 = pygame.mixer.Sound("monkeypomodoro/sounds/just_do_it.mp3")
        just_do_mp3_length = just_do_mp3.get_length()

        # audio prompt to enter a task
        pygame.mixer.music.load("monkeypomodoro/sounds/please_enter_a_task.mp3")
        print(f"\rGood luck!", end="")
        pygame.mixer.music.set_volume(1)
        time.sleep(1)
        pygame.mixer.music.play(-1)

        # prompt to enter a task
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(suspend_in)  # Set the alarm for {suspend_in} seconds
        try:
            task = input(f"\r   For the next {duration_in_minute} minutes I will be working on: ")
            signal.alarm(0)  # Cancel the alarm
            pygame.mixer.music.stop()
            tasks.append(task)

            # Starting cycle
            print(f"\r  Starting pomodoro #{i + 1}/{cycles}")
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time >= 3:
                    break
                else:
                    remaining_time = 3 - round(elapsed_time)
                    print(f"\rPomodoro starts in {remaining_time}", end="")
                    # 1 second before rechecking the elapsed time
                    time.sleep(1)

            # ticking clock
            pygame.mixer.music.load("monkeypomodoro/sounds/Clock-ticking.mp3")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

            # start the timer loop
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time >= duration_in_minute:
                    print(f"\rStarting short break #{i + 1}/{cycles}", end="")
                    break
                else:
                    remaining_time = duration_in_minute - elapsed_time
                    minutes, seconds = divmod(int(remaining_time), 60)
                    print(f"\rSession ends in {minutes:02d}:{seconds:02d}", end="")
                    # 1 second before rechecking the elapsed time
                    time.sleep(1)
            pygame.mixer.music.stop()

            # short break
            if i + 1 < cycles:
                now = datetime.datetime.now()
                s = round(now.second)
                m = duration_in_minute
                at = f"     \r\"{tasks[-1]}\" Finished at [{now.date()} {now.hour}:{now.minute}:{s}] " \
                     f"Duration: [{m}] Minutes"
                print(at)

                # report
                try:
                    with open("pomodoro_report.json", "r") as file:
                        report = json.load(file)
                except json.decoder.JSONDecodeError:
                    report = []

                # %h gives the abbreviated month. %H gives hour
                minute = now.time().strftime("%M")
                hour = now.time().strftime("%H")
                date = now.date().strftime("%d")
                month = now.date().strftime("%m")
                y, w, dy = now.isocalendar()
                report.append({"activity": tasks[-1], "duration": m, "year": y, "month": month, "week": w, "date": date,
                               "day": dy, "hour": hour, "minute": minute})
                with open("pomodoro_report.json", "w") as file:
                    json.dump(report, file, indent=4)

                # open browser
                pygame.mixer.music.load("monkeypomodoro/sounds/just_do_it.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                os.system("notify-send 'Time for a Break!'")
                while pygame.mixer.music.get_busy():
                    print("\ropening firefox..", end="")
                    time.sleep(1)
                if custom_tab1 == "none":
                    webbrowser.open_new(monkey_type)
                else:
                    webbrowser.open_new(custom_tab1)
                time.sleep(0.2)
                webbrowser.open(spotify)

                # waiting for the page
                pygame.mixer.music.load("monkeypomodoro/sounds/time_for_a_break.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    current_pos = pygame.mixer.music.get_pos()
                    current_pos = current_pos / 1000
                    remaining_time = break_mp3_length - current_pos
                    remaining_time_in_second = round(remaining_time)
                    print(f"\ralarm ends in {remaining_time_in_second}", end="")
                    # 1 second before rechecking the elapsed time
                    time.sleep(1)
                time.sleep(6)
                print(f"\rBreak time!", end="")
                time.sleep(2)
                pyautogui.press("space")
                pyautogui.keyDown("ctrl")
                pyautogui.press("tab")
                pyautogui.keyUp("ctrl")
                pyautogui.press("f11")

                # short break countdown
                start_time = time.time()
                while True:
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= short_break:
                        print("\r", end="")
                        break
                    else:
                        remaining_time = short_break - elapsed_time
                        minutes, seconds = divmod(int(remaining_time), 60)
                        print(f"\rShort break ends in {minutes:02d}:{seconds:02d}", end="")
                        # 1 second before rechecking the elapsed time
                        time.sleep(1)

                # short break ends
                pygame.mixer.music.load("monkeypomodoro/sounds/time_to_work.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                os.system("notify-send 'Time to Work!'")
                while pygame.mixer.music.get_busy():
                    current_pos = pygame.mixer.music.get_pos()
                    current_pos = current_pos / 1000
                    remaining_time = work_mp3_length - current_pos
                    remaining_time_in_second = round(remaining_time)
                    print(f"\ralarm ends in {remaining_time_in_second}", end="")
                    # 1 second before rechecking the elapsed time
                    time.sleep(1)
                time.sleep(1)
                print(f"\rWork time!", end="")
                time.sleep(2)
                # you're in monkeytype typing
                # your typing may intervene these following actions:
                pyautogui.keyDown("ctrl")
                pyautogui.press("w")
                pyautogui.press("w")
                pyautogui.keyUp("ctrl")

            # long break
            else:
                now = datetime.datetime.now()
                s = round(now.second)
                m = duration_in_minute
                at = f"     \r\"{tasks[-1]}\" Finished at [{now.date()} {now.hour}:{now.minute}:{s}] " \
                     f"Duration: [{m}] Minutes"
                print(at)

                # report
                try:
                    with open("pomodoro_report.json", "r") as file:
                        report = json.load(file)
                except json.decoder.JSONDecodeError:
                    report = []

                # %h gives the abbreviated month. %H gives hour
                minute = now.time().strftime("%M")
                hour = now.time().strftime("%H")
                date = now.date().strftime("%d")
                month = now.date().strftime("%m")
                y, w, dy = now.isocalendar()
                report.append({"activity": tasks[-1], "duration": m, "year": y, "month": month, "week": w, "date": date,
                               "day": dy, "hour": hour, "minute": minute})
                with open("pomodoro_report.json", "w") as file:
                    json.dump(report, file, indent=4)

                    # open browser
                pygame.mixer.music.load("monkeypomodoro/sounds/stand_up.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                os.system("notify-send 'Time for a Break!'")
                while pygame.mixer.music.get_busy():
                    print("\ropening firefox..", end="")
                    time.sleep(1)
                webbrowser.open_new(google_calendar)
                time.sleep(0.2)
                webbrowser.open(spotify)

                # loading the page
                pygame.mixer.music.load("monkeypomodoro/sounds/time_for_a_break.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    current_pos = pygame.mixer.music.get_pos()
                    current_pos = current_pos / 1000
                    remaining_time = break_mp3_length - current_pos
                    remaining_time_in_second = round(remaining_time)
                    print(f"\ralarm ends in {remaining_time_in_second}", end="")
                    # 1 second before rechecking the elapsed time
                    time.sleep(1)
                time.sleep(6)
                print(f"\rBreak time!", end="")
                time.sleep(2)
                pyautogui.press("space")
                pyautogui.keyDown("ctrl")
                pyautogui.press("tab")
                pyautogui.keyUp("ctrl")
                time.sleep(0.2)
                if custom_tab2 == "none":
                    pass
                else:
                    webbrowser.open_new(custom_tab2)

                # end of cycles (long break)
                print(f"\r{len(tasks)} Tasks have been completed:")
                for e, task in enumerate(tasks):
                    print(f"{e + 1}. {task}")
                start_time = time.time()
                while True:
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= long_break:
                        print("\r ")
                        break
                    else:
                        remaining_time = long_break - elapsed_time
                        minutes, seconds = divmod(int(remaining_time), 60)
                        print(f"\rLong break ends in {minutes:02d}:{seconds:02d}", end="")
                        # 1 second before rechecking the elapsed time
                        time.sleep(1)

                # long break ends
                pygame.mixer.music.load("monkeypomodoro/sounds/break_over.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    print("\ropening firefox..", end="")
                    time.sleep(1)
                webbrowser.open_new(google_calendar)
                time.sleep(0.2)
                webbrowser.open(spotify)

                # loading the page
                pygame.mixer.music.load("monkeypomodoro/sounds/time_to_work.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                os.system("notify-send 'Time to Work!'")
                while pygame.mixer.music.get_busy():
                    current_pos = pygame.mixer.music.get_pos()
                    current_pos = current_pos / 1000
                    remaining_time = work_mp3_length - current_pos
                    remaining_time_in_second = round(remaining_time)
                    print(f"\ralarm ends in {remaining_time_in_second}", end="")
                    # 1 second before rechecking the elapsed time
                    time.sleep(1)
                time.sleep(1)
                print(f"\rWork time!", end="")
                time.sleep(3)
                pyautogui.press("space")
                pyautogui.keyDown("ctrl")
                pyautogui.press("w")
                pyautogui.keyUp("ctrl")
                pygame.mixer.music.load("monkeypomodoro/sounds/just_do_it.mp3")
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    current_pos = pygame.mixer.music.get_pos()
                    current_pos = current_pos / 1000
                    remaining_time = just_do_mp3_length - current_pos
                    remaining_time_in_second = round(remaining_time)
                    print(f"\ralarm ends in {remaining_time_in_second}", end="")
                    # 1 second before rechecking the elapsed time
                    time.sleep(1)
                now = datetime.datetime.now()
                seconds = now.second
                seconds = round(seconds)
                print(f"\rLong break finished at [{now.date()} {now.hour}:{now.minute}:{seconds}]")

        # Suspend the computer when failed to enter a task [in suspend_in] seconds
        except TypeError:
            print(f"\nFailed to enter the task within {suspend_in} seconds\nproceed to suspend the computer")
            pygame.mixer.music.stop()
            subprocess.run(["systemctl", "suspend"])
            while True:
                time.sleep(60)


#  tab to open in short break (replaces monkeytype)
custom_tab_short = "insert_page_url_here"
#  tab to open in long break
custom_tab_long = "insert_page_url_here"
none = "none"
pomodoro(5, 25, none, custom_tab_long)  # (5/4.6, 25/29, "none"/"link1", "none"/"link2")

"""
To fix:
- nothing to fix

Feature to add:
- option to pause.
- github-style heatmap data representation.
- fork version into two where i can turn one to my liking and the other as general version 

Comments for commit:
"""
