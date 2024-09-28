import pyautogui
import cv2
import numpy as np
import time
from collections import deque

def find_pattern(template_paths, threshold=0.7):
    # Capture screen
    screen = np.array(pyautogui.screenshot())
    screen_bgr = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

    all_locations = []
    for template_path in template_paths:
        # Load template image
        template = cv2.imread(template_path)
        h, w = template.shape[:2]

        # Perform template matching
        result = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        if locations:
            print(f"Found {len(locations[0])} instances of {template_path}")
        all_locations.extend(list(zip(*locations[::-1])))  # Add (x, y) coordinates
    
    return all_locations

def click_pattern(location, template_path):
    template = cv2.imread(template_path)
    h, w = template.shape[:2]
    
    center_x = location[0] + w // 2
    center_y = location[1] + h // 2

    pyautogui.moveTo(center_x, center_y)
    pyautogui.click()

def find_nearest_unclicked(locations, clicked_locations, max_distance=70): #increased max dist from 10 to 50
    current_pos = pyautogui.position()
    nearest_location = None
    min_distance = float('inf')

    for loc in locations:
        if not any(abs(loc[0] - c[0]) < max_distance and abs(loc[1] - c[1]) < max_distance for c in clicked_locations):
            distance = ((current_pos.x - loc[0])**2 + (current_pos.y - loc[1])**2)**0.5
            if distance < min_distance:
                min_distance = distance
                nearest_location = loc

    return nearest_location

def main(worker=None):
    print("Main function started")
    print("Starting in 2 seconds...")
    time.sleep(2)
    print("Script is now running.")
    while worker is None or worker.running:
        patterns1 = ['Chanvre1.png', 'Chanvre2.png', 'Chanvre3.png', 'Chanvre4.png', 'Chanvre6.png', 'Chanvre7.png', 'Chanvre8.png', 'Chanvre10.png']  # Multiple images for first pattern
        pattern2 = 'Faucher.png'
        clicked_locations = deque(maxlen=10)  # Store last 10 clicked locations
        max_retries = 5  # Maximum number of retries for the first pattern

       

        # Look for the first pattern with retries
        first_pattern_found = False
        for attempt in range(max_retries):
            t = time.time()
            locations1 = find_pattern(patterns1, threshold=0.7)
            print(f"Time taken to find first pattern: {time.time() - t} seconds")
            nearest1 = find_nearest_unclicked(locations1, clicked_locations)
            
            if nearest1:
                print(f"First pattern found and clicked (attempt {attempt + 1})")
                click_pattern(nearest1, patterns1[0])  # Use the first pattern image for clicking
                clicked_locations.append(nearest1)
                first_pattern_found = True
                break
            else:
                print(f"First pattern not found (attempt {attempt + 1})")
                time.sleep(0.1)  # Wait a bit before retrying
        
        if not first_pattern_found:
            print("First pattern not found after all retries")
            time.sleep(1)
            continue  # Start the next iteration of the main loop
        
        # Look for the second pattern
        time.sleep(0.1)
        locations2 = find_pattern([pattern2], threshold=0.8)
        nearest2 = find_nearest_unclicked(locations2, clicked_locations)
        
        if nearest2:
            print("Second pattern found and clicked")
            click_pattern(nearest2, pattern2)
            # clicked_locations.append(nearest2)
        else:
            print("Second pattern not found")

        # Wait before starting the next iteration
        time.sleep(1)
        print("Starting next iteration...")
    print("Fin de la récolte")
if __name__ == "__main__":
    main()