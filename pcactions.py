import time
import pyautogui
import datetime
import os
import subprocess
import psutil
import wallpaperchange
import cv2
import pathlib
import shutil
import webbrowser
import pygetwindow


bot_path = pathlib.Path(__file__).parent.resolve()
wallpaper_path = fr"{bot_path}\wallpaperPhotos"
max_photos_in_one_folder = 5


def turn_pc_off():
    print("turning off...")
    os.system("shutdown /s /t 1")


def take_screenshot():
    screenshot_directory = fr"{bot_path}\screenshots"
    screenshot_path = fr"{screenshot_directory}\Screenshot {get_current_time()}.png"

    current_screenshot = pyautogui.screenshot()
    current_screenshot.save(screenshot_path)

    clear_excess_photos(screenshot_directory)

    return screenshot_path


def clear_excess_photos(path):
    photo_path_directory = path
    all_screenshots = os.listdir(photo_path_directory)

    while len(all_screenshots) > max_photos_in_one_folder:
        os.remove(fr"{photo_path_directory}\{all_screenshots[0]}")
        all_screenshots.pop(0)


def minimize_all_tabs():
    # filter removes "" from the list
    windows_titles = list(filter(None, pygetwindow.getAllTitles()))
    for window_title in windows_titles:
        pygetwindow.getWindowsWithTitle(window_title)[0].minimize()


def launch_wallpaper_engine():
    process_name = "wallpaper64.exe"
    subprocess.Popen(fr"{wallpaperchange.wallpaper_engine_path}\{process_name}")
    time.sleep(0.5)


def close_wallpaper_engine():
    if check_if_process_running("wallpaper32.exe"):
        subprocess.call(["taskkill", "/F", "/IM", "wallpaper32.exe"])
    if check_if_process_running("wallpaper64.exe"):
        subprocess.call(["taskkill", "/F", "/IM", "wallpaper64.exe"])
    change_wallpaper(fr"{wallpaper_path}\{os.listdir(wallpaper_path)[max_photos_in_one_folder - 1]}")


def change_wallpaper(path):
    wallpaperchange.change_wallpaper(path)


def exit_bot():
    proces_name = "python.exe"
    while check_if_process_running(proces_name):
        subprocess.call(["taskkill", "/F", "/IM", proces_name])

    # this message should never be printed
    print("Bot have been terminated")


def take_camera_photo():
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)

    result, image = cam.read()

    current_time = get_current_time()
    camera_photo_path = fr"{bot_path}\cameraPhotos\Camera {current_time}.png"
    camera_photo_directory = fr"{bot_path}\cameraPhotos"

    # this directory should not contain russian letters
    camera_directory = fr"D:\cameraPhotos\Camera {current_time}.png"

    if result:
        cv2.imwrite(camera_directory, image)
    else:
        print("No image detected. Please, try again!")

    shutil.move(camera_directory, camera_photo_path)
    clear_excess_photos(camera_photo_directory)
    return camera_photo_path


def launch_google():
    subprocess.Popen(r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe')
    time.sleep(5.0)
    for i in range(0, 3):
        pyautogui.press("tab")
    pyautogui.press("esc")


def open_website(site_url):
    webbrowser.open(site_url)


def close_google():
    process_name = "chrome.exe"
    while check_if_process_running(process_name):
        subprocess.call(["taskkill", "/F", "/IM", process_name])


def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")


def check_if_process_running(process_name):
    # Check if there is any running process that contains the given name process_name.
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def epilepsy_joke():
    open_website("https://www.youtube.com/watch?v=EkXdjnX6TmE")

    while True:
        logo = pyautogui.locateOnScreen(fr"D:\cameraPhotos\logo.png")
        if logo is not None:
            break

    print(logo)
    pyautogui.press("f")
