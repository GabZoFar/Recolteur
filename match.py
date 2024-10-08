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