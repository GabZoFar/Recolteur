from typing import List
import pyautogui
import cv2
import numpy as np
import time
from collections import deque
from match import Match, find_nearest_unclicked, click_pattern
from combat import Combat
class Recolter:

    def __init__(self, 
                 patterns1 = None, 
                 pattern2 = None):

        self.patterns1 = patterns1 if patterns1 is not None else ['Chanvre1.png', 'Chanvre2.png', 'Chanvre3.png', 'Chanvre4.png', 'Chanvre6.png', 'Chanvre7.png', 'Chanvre8.png', 'Chanvre10.png']  # Multiple images for first pattern
        self.pattern2 = pattern2 if pattern2 is not None else 'Faucher.png'
        self.max_retries = 5  # Maximum number of retries for the first pattern to find


    def run(self, worker=None):
        """Démarre l'action de faucher"""


        print("Main function started")
        print("Starting in 2 seconds...")
        time.sleep(2)
        print("Script is now running.")
        clicked_locations = deque(maxlen=2) # store last 2 clicked locations
        while worker is None or worker.running:
            if Combat.find_red_square():
                Combat.execute_combat_sequence(worker)
            
            # Look for the first pattern with retries
            first_pattern_found = False
            for attempt in range(self.max_retries):
                t = time.time()
                locations1 = Match.find_pattern(self.patterns1, threshold=0.7)
                print(f"Time taken to find first pattern: {time.time() - t} seconds")
                nearest1 = find_nearest_unclicked(locations1, clicked_locations)
                
                if nearest1:
                    print(f"First pattern found and clicked (attempt {attempt + 1})")
                    click_pattern(nearest1)
                    clicked_locations.append(nearest1)
                    first_pattern_found = True
                    break
                else:
                    print(f"First pattern not found (attempt {attempt + 1})")
                    time.sleep(0.1)  # Wait a bit before retrying
                if worker and not worker.running:
                    break
            if worker and not worker.running:
                break
            
            if not first_pattern_found:
                print("First pattern not found after all retries")
                time.sleep(1)
                continue  # Start the next iteration of the main loop
            
            # Look for the second pattern
            time.sleep(0.1)
            locations2 = Match.find_pattern([self.pattern2], threshold=0.8)
            nearest2 = find_nearest_unclicked(locations2, clicked_locations)
            
            if worker and not worker.running:
                break
            if nearest2:
                print("Second pattern found and clicked")
                click_pattern(nearest2)
            else:
                print("Second pattern not found")

            # Wait before starting the next iteration
            time.sleep(1)
            print("Starting next iteration...")

        print("Fin de la récolte")


if __name__ == "__main__":
    Recolter().run()