import time
import pyautogui
import subprocess
import os
import cv2
import numpy as np
import pygetwindow as gw
from PIL import ImageGrab
import pytesseract

# Global speed delay (in seconds)
execution_speed = 0  # Default: no delay (0 seconds)


class DeskAutomation:

    def __init__(self):
        self.image_folder = ""

    def _delay(self):
        time.sleep(execution_speed)

    def Set_Execution_Speed(self, time_str):
        global execution_speed
        if isinstance(time_str, str):
            time_str = time_str.lower()
            if time_str.endswith("ms"):
                execution_speed = float(time_str.replace("ms", "")) / 1000
            elif time_str.endswith("s"):
                execution_speed = float(time_str.replace("s", ""))  # Extracting seconds
            else:
                execution_speed = float(time_str)
        else:
            execution_speed = float(time_str)

    def SetImageFolder(self, folder_path):
        self.image_folder = folder_path
        self._delay()

    def Open_Application(self, app_path):
        subprocess.Popen(app_path)
        self._delay()

    def MaximizeApplication(self):
        window = gw.getActiveWindow()
        if window:
            window.maximize()
        self._delay()

    def Close_Application(self, app_name):
        os.system(f"taskkill /f /im {app_name}")
        self._delay()

    def InputText(self, text):
        pyautogui.typewrite(text)
        self._delay()

    def Shortcut(self, *keys):
        pyautogui.hotkey(*keys)
        self._delay()

    def PressKey(self, key):
        key = key.upper()
        if key == "CAPSLOCK":
            pyautogui.press("capslock")
        else:
            pyautogui.press(key)
        self._delay()

    def Click_Image(self, image_name):
        path = os.path.join(self.image_folder, image_name)
        location = pyautogui.locateCenterOnScreen(path)
        if location:
            pyautogui.click(location)
        self._delay()

    def DoubleClick_Image(self, image_name):
        path = os.path.join(self.image_folder, image_name)
        location = pyautogui.locateCenterOnScreen(path)
        if location:
            pyautogui.doubleClick(location)
        self._delay()

    def RightClick_Image(self, image_name):
        path = os.path.join(self.image_folder, image_name)
        location = pyautogui.locateCenterOnScreen(path)
        if location:
            pyautogui.rightClick(location)
        self._delay()

    def _find_text_location(self, search_text):
        screenshot = ImageGrab.grab()
        text_data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT)
        for i, word in enumerate(text_data["text"]):
            if word.strip().lower() == search_text.strip().lower():
                x, y, w, h = text_data["left"][i], text_data["top"][i], text_data["width"][i], text_data["height"][i]
                return x + w // 2, y + h // 2
        return None

    def Click_Text(self, text):
        location = self._find_text_location(text)
        if location:
            pyautogui.click(location)
        self._delay()

    def DoubleClick_Text(self, text):
        location = self._find_text_location(text)
        if location:
            pyautogui.doubleClick(location)
        self._delay()

    def RightClick_Text(self, text):
        location = self._find_text_location(text)
        if location:
            pyautogui.rightClick(location)
        self._delay()

    def Text_On_Image(self, image_name, text):
        path = os.path.join(self.image_folder, image_name)
        location = pyautogui.locateCenterOnScreen(path)
        if location:
            pyautogui.click(location)
            self.InputText(text)
        self._delay()

    def WaitUntilVisible(self, locator, timeout="10s"):
        timeout = int(timeout.replace("s", ""))  # Extracting seconds from timeout string
        start_time = time.time()
        while time.time() - start_time < timeout:
            if locator.lower().endswith(('.png', '.jpg', '.jpeg')):  # Checking if locator is an image
                path = os.path.join(self.image_folder, locator)
                if pyautogui.locateOnScreen(path):  # Wait until image is found on screen
                    break
            else:
                if self._find_text_location(locator):  # Wait until text is found on screen
                    break
            time.sleep(0.1)
        self._delay()

    def ClearText(self, *args):
        image = None
        text = None
        for arg in args:
            if arg.lower().endswith((".png", ".jpg", ".jpeg")):  # Checking for image
                image = os.path.join(self.image_folder, arg)
            elif arg.startswith('"') and arg.endswith('"'):  # Checking for text
                text = arg.strip('"')

        if image:
            location = pyautogui.locateCenterOnScreen(image)
            if location:
                pyautogui.click(location)
                time.sleep(0.5)
            else:
                raise Exception(f'Image "{image}" not found on screen.')

        if text:
            location = self._find_text_location(text)
            if location:
                pyautogui.click(location)
                pyautogui.hotkey("ctrl", "shift", "right")
                pyautogui.press("backspace")
            else:
                raise Exception(f'Text "{text}" not found on screen.')

        if not text:
            pyautogui.hotkey("ctrl", "a")
            pyautogui.press("backspace")

        self._delay()
