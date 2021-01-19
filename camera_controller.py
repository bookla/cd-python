import cv2
import uuid
from os.path import join
import time
import win32con
import win32api
import win32gui

base_dir = "/Users/book/PycharmProjects/HIS-Christmas-Dinner"

def take_photo():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cv2.imwrite(join(join(base_dir, "images"), str(uuid.uuid4().hex)[0:10]) + ".jpg", frame)
    time.sleep(0.1)
    ret, frame = cam.read()
    cv2.imwrite(join(join(base_dir, "images"), str(uuid.uuid4().hex)[0:10]) + ".jpg", frame)
    time.sleep(0.1)
    ret, frame = cam.read()
    cv2.imwrite(join(join(base_dir, "images"), str(uuid.uuid4().hex)[0:10]) + ".jpg", frame)
    cam.release()


rect = []


def get_remote_window(hwnd, extra):
    global rect
    if win32gui.GetWindowText(hwnd) == "Remote":
        rect.append((hwnd, win32gui.GetWindowRect(hwnd)))
        print(rect)


top_windows = []


def window_enumeration_handler(hwnd, special):
    global top_windows
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))


def bring_window_to_front(name):
    win32gui.EnumWindows(window_enumeration_handler, None)
    print(top_windows)
    print(rect)
    named_windows = [window for window in top_windows if window[1] == "Remote" and win32gui.GetWindowRect(window[0])[0] > 0]
    # win32gui.ShowWindow(named_windows[1][0], 5)
    win32gui.SetForegroundWindow(named_windows[0][0])


def sony_capture_command():
    win32gui.EnumWindows(get_remote_window, None)
    # win32gui.BringWindowToTop(title="Remote")
    bring_window_to_front("Remote")
    x = rect[0][1][0]
    y = rect[0][1][1]
    w = rect[0][1][2] - x
    shutter_x = int(x + w/2 - 20)
    shutter_y = int(y + 200)
    win32api.SetCursorPos((shutter_x, shutter_y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, shutter_x, shutter_y, 0, 0)
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, shutter_x, shutter_y, 0, 0)

