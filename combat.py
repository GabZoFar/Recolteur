from typing import List
import pyautogui
import cv2
import numpy as np
import time
from collections import deque
from match import Match, find_nearest_unclicked, click_pattern

class Combat:
    carrerouge = ["carrerouge1.png", "carrerouge2.png", "carrerouge3.png"]
    tireloigne = "tireloigne.png"
    protector = ["protector1.png", "protector2.png", "protector3.png"]
    Fincombat = "Fincombat.png"
    def __init__(self, worker=None):
        self.worker = worker

    @classmethod
    def execute_combat_sequence(cls, worker=None):
        combat = cls(worker)
        combat.run()

    def run(self):
        pyautogui.press('1')
        time.sleep(5)
        pyautogui.press('option')
        time.sleep(12)

        while True:
            location = Match.find_pattern([self.tireloigne], threshold=0.8)
            print("location tireloigne", location)
            if location:
                click_pattern(location[0], right_click=True)
                time.sleep(2)
                break
            else:
                print("No tireloigne found")


        while True:
            pyautogui.press('4')

            location = Match.find_pattern(self.protector, threshold=0.8)
            if location:
                click_pattern(location[0])
            else:
                time.sleep(2)
                print("No protector found")

            location = Match.find_pattern([self.Fincombat], threshold=0.8)
            if location:
                time.sleep(10)

                pyautogui.press('2')
                pyautogui.press('esc')
                return
            if self.worker and not self.worker.running:
                return

    @classmethod
    def find_red_square(cls):
        if Match.find_pattern(cls.carrerouge, threshold=0.6):
            return True
        return False

    @staticmethod
    def check_pattern(pattern_name):
        return pyautogui.locateOnScreen(self.patterns[pattern_name], confidence=0.8) is not None

    def find_and_click_pattern(self, pattern_name, right_click=False):
        location = pyautogui.locateOnScreen(self.patterns[pattern_name], confidence=0.8)
        if location:
            x, y = pyautogui.center(location)
            if right_click:
                pyautogui.rightClick(x, y)
            else:
                pyautogui.click(x, y)
            return True
        return False

    def start_recolter(self):
        # Implement the logic to start the main recolter class here
        pass
