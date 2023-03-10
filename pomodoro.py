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


def pomodoro(duration_in_minute, short_break_in_minute, long_break_in_minute, number_of_cycle, custom_tab1):

    # Configuration I guess
    spotify = "https://open.spotify.com/"
    monkey_type = "https://monkeytype.com/"
    google_calendar = "https://calendar.google.com/calendar/u/1/r/customday"
    duration = duration_in_minute * 60
    short_break = short_break_in_minute * 60
    long_break = long_break_in_minute * 60
    cycles = number_of_cycle
    tasks = []
    suspend_in = 60

    for i in range(cycles):

        # initializes the pygame stuff
        pygame.mixer.init()
        work_mp3 = pygame.mixer.Sound("/home/bara/Music/Pomodoro/time_to_work.mp3")
        work_mp3_length = work_mp3.get_length()
        break_mp3 = pygame.mixer.Sound("/home/bara/Music/Pomodoro/time_for_a_break.mp3")
        break_mp3_length = break_mp3.get_length()
        just_do_mp3 = pygame.mixer.Sound("/home/bara/Music/Pomodoro/just_do_it.mp3")
        just_do_mp3_length = just_do_mp3.get_length()

        # audio prompt to enter a task
        pygame.mixer.music.load("/home/bara/Music/Pomodoro/please_enter_a_task.mp3")
        print(f"\rGood luck!", end="")
        pygame.mixer.music.set_volume(1)
        time.sleep(1)
        pygame.mixer.music.play(-1)

        # prompt to enter a task
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(suspend_in)  # Set the alarm for {suspend_in} seconds
        try:
            task = input(f"\rFor the next {duration_in_minute} minutes I will work on: ")
            signal.alarm(0)  # Cancel the alarm
            pygame.mixer.music.stop()
            tasks.append(task)

            # Starting cycle
            print(f"\rStarting pomodoro #{i + 1}/{cycles}")
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

            # music etc
            pygame.mixer.music.load("/home/bara/Music/Pomodoro/ganbatte.mp3")
            pygame.mixer.music.set_volume(0.2)
            pygame.mixer.music.play()
            print(f"\r??????????????????????????????", end="")
            time.sleep(2)
            pygame.mixer.music.load("/home/bara/Music/Pomodoro/Ticking Digital Clock.mp3")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

            # start the timer loop
            start_time = time.time()
            while True:
                elapsed_time = time.time() - start_time
                if elapsed_time >= duration:
                    print(f"\rStarting short break #{i + 1}/{cycles}", end="")
                    break
                else:
                    remaining_time = duration - elapsed_time
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
                at = f"\r\"{tasks[-1]}\" Finished at [{now.date()} {now.hour}:{now.minute}:{s}] Duration: [{m}] Minutes"
                print(at)

                # report
                try:
                    with open("pomodoro_report.json", "r") as file:
                        report = json.load(file)
                except json.decoder.JSONDecodeError:
                    report = []
                hour = now.time().strftime("%H")  # %h gives the abbreviated month name for some reason
                date = now.date().strftime("%d")
                month = now.date().strftime("%m")
                y, w, dy = now.isocalendar()
                report.append({"activity": tasks[-1], "duration": m, "year": y, "month": month, "week": w, "date": date,
                               "day": dy, "hour": hour})
                with open("pomodoro_report.json", "w") as file:
                    json.dump(report, file, indent=4)

                # open browser
                pygame.mixer.music.load("/home/bara/Music/Pomodoro/stand_up.mp3")
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

                # break notification and waiting for the page
                pygame.mixer.music.load("/home/bara/Music/Pomodoro/time_for_a_break.mp3")
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
                time.sleep(1)
                print(f"\rBreak time!", end="")
                time.sleep(2)
                pygame.mixer.music.load("/home/bara/Music/Pomodoro/good-job_F6JFycP.mp3")
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play()
                print(f"\r??????????????????", end="")
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
                pygame.mixer.music.load("/home/bara/Music/Pomodoro/time_to_work.mp3")
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
                at = f"\r\"{tasks[-1]}\" Finished at [{now.date()} {now.hour}:{now.minute}:{s}] Duration: [{m}] Minutes"
                print(at)

                # report
                try:
                    with open("pomodoro_report.json", "r") as file:
                        report = json.load(file)
                except json.decoder.JSONDecodeError:
                    report = []
                hour = now.time().strftime("%H")  # %h gives the abbreviated month name for some reason
                date = now.date().strftime("%d")
                month = now.date().strftime("%m")
                y, w, dy = now.isocalendar()
                report.append({"activity": tasks[-1], "duration": m, "year": y, "month": month, "week": w, "date": date,
                               "day": dy, "hour": hour})
                with open("pomodoro_report.json", "w") as file:
                    json.dump(report, file, indent=4)

                    # open browser
                pygame.mixer.music.load("/home/bara/Music/Pomodoro/stand_up.mp3")
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
                pygame.mixer.music.load("/home/bara/Music/Pomodoro/time_for_a_break.mp3")
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
                time.sleep(1)
                print(f"\rBreak time!", end="")
                time.sleep(3)
                pygame.mixer.music.load("/home/bara/Music/Pomodoro/good-job_F6JFycP.mp3")
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play()
                print(f"\r?????????????????????", end="")
                time.sleep(2)
                pyautogui.press("space")
                pyautogui.keyDown("ctrl")
                pyautogui.press("tab")
                pyautogui.keyUp("ctrl")

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

                # music etc
                pygame.mixer.music.load("/home/bara/Music/Pomodoro/break_over.mp3")
                pygame.mixer.music.set_volume(1)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    print("\ropening firefox..", end="")
                    time.sleep(1)
                webbrowser.open_new(google_calendar)
                time.sleep(0.2)
                webbrowser.open(spotify)

                # loading the page
                pygame.mixer.music.load("/home/bara/Music/Pomodoro/time_to_work.mp3")
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
                pygame.mixer.music.load("/home/bara/Music/Pomodoro/just_do_it.mp3")
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


# "insert_a_website_url"
custom_tab = "file:///home/bara/Documents/Guitar%20stuff/eddie%20van%20der%20meer/learned/Ed_Sheeran_-_Perfect.pdf"
none = "none"
pomodoro(25, 5, 25, 2, none)  # (25, 4.6, 29, 4)/(25, 5, 25, 4, "none"/"link",)

"""
To fix:
- nothing to fix

Feature to add:
- option to pause.
- github-style heatmap data representation.

Comments:
now.date() returns only the date without any time information so strftime("%H") will always be "00". 
instead use time.now() which returns a datetime object that contains both the date and time information
"""
