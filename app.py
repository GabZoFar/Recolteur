from typing import List
import pyautogui
import cv2
import numpy as np
import time
from collections import deque

class Match:
    """Renvoie les coordonnées d'un pattern trouvé avec son pattern"""
    def __init__(self, location, template_path, h, w, value):
        self.x = int(location[0])
        self.y = int(location[1])
        self.template_path = template_path
        self.h = h
        self.w = w
        self.value = value
    
    def __repr__(self):
        return f"Match(location=({self.x}, {self.y}), template_path={self.template_path}, " \
            f"h={self.h}, w={self.w}, value={self.value})"

    @staticmethod
    def make_screenshot(region=None):
        """Effectue le screenshot"""
        return pyautogui.screenshot(region=region)
    

    @classmethod
    def find_pattern(cls, template_paths, in_ = None, region=None, threshold=0.7):
        
        """
        Recherche des motifs dans une capture d'écran.

        Args:
            template_paths (list): Liste des chemins vers les images de motifs à rechercher.
            in_ : Pillow image ou path pour trouver le template. Si None, effectue un screenshot
            region: Region à analyser dans l’image
            threshold (float, optional): Seuil de correspondance pour la détection des motifs. Par défaut à 0.7.

        Returns:
            list: Liste des objets Match trouvés

        Note:
            Cette fonction utilise la correspondance de modèle OpenCV pour trouver les motifs.
            Elle convertit l'image de l'écran en BGR pour la compatibilité avec OpenCV.
        """
        
        if in_ is None:
            screen = cls.make_screenshot(region=region)
        else:
            if isinstance(in_, str):
                screen = cv2.imread(in_)
            else:
                screen = in_
        # Capture screen
        
        screen = np.array(screen)
        screen_bgr = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)

        all_locations = []
        for template_path in template_paths:
            # Load template image
            template = cv2.imread(template_path)
            if not template.any():
                raise ValueError(f"Template {template_path} not found")
            
            h, w = template.shape[:2]

            # Perform template matching
            result = cv2.matchTemplate(screen_bgr, template, cv2.TM_CCOEFF_NORMED)
            print("result", result)
            print("len(result)", len(result))
            locations = np.where(result >= threshold)
            if locations:
                print(f"Found {len(locations[0])} instances of {template_path}")
                locations = list(zip(*locations[::-1]))
                for location in locations:
                    all_locations.append(Match(location, template_path, h, w, value=result[location[1], location[0]]))
        return all_locations
    

def show_pattern_locations(locations: List[Match], screen   ):
    """
    Affiche les emplacements des motifs sur l'écran
    """
    for location in locations:
        cv2.rectangle(screen, (location.x, location.y), (location.x + location.w, location.y + location.h), (0, 0, 255), 2)
    cv2.imshow("Pattern Locations", screen)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def click_pattern(location: Match):
    """
    Clic sur le pattern (au centre du pattern)
    """
    
    center_x = location.x + location.w // 2
    center_y = location.y + location.h // 2

    pyautogui.moveTo(center_x, center_y)
    pyautogui.click()


def find_nearest_unclicked(locations: List[Match], clicked_locations, not_near_than=70): #increased max dist from 10 to 50
    current_pos = pyautogui.position()
    nearest_location = None
    min_distance = float('inf')

    for loc in locations:
        if not any(abs(loc.x - c.x) < not_near_than and abs(loc.y - c.y) < not_near_than for c in clicked_locations):
            distance = ((current_pos.x - loc.x)**2 + (current_pos.y - loc.y)**2)**0.5
            if distance < min_distance:
                min_distance = distance
                nearest_location = loc

    return nearest_location

class Recolter:

    def __init__(self, 
                 patterns1 = None, 
                 pattern2 = None):

        self.patterns1 = patterns1 if patterns1 is not None else ['Chanvre1.png', 'Chanvre2.png', 'Chanvre3.png', 'Chanvre4.png', 'Chanvre6.png', 'Chanvre7.png', 'Chanvre8.png', 'Chanvre10.png']  # Multiple images for first pattern
        self.pattern2 = pattern2 if pattern2 is not None else 'Faucher.png'
        self.max_retries = 5  # Maximum number of retries for the first pattern to find


    def run(self, worker=None):
        """Démarre l’action de faucher"""


        print("Main function started")
        print("Starting in 2 seconds...")
        time.sleep(2)
        print("Script is now running.")
        clicked_locations = deque(maxlen=2) # store last 2 clicked locations
        while worker is None or worker.running:
            
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
                click_pattern(nearest2, self.pattern2)
            else:
                print("Second pattern not found")

            # Wait before starting the next iteration
            time.sleep(1)
            print("Starting next iteration...")

        print("Fin de la récolte")


if __name__ == "__main__":
    Recolter().run()