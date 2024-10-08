from typing import List
import pyautogui
import cv2
import numpy as np
import time
from collections import deque
from match import Match, find_nearest_unclicked, click_pattern

class Combat:


    # check carré rouge
    # si carré rouge -> appuyer sur la touche 1, option
    # appuyer sur 4
    # check aura bleue
    # cliquer sur aura bleue
    # check resultat du combat
    # appuyer sur echap
    # appuyer sur 2
    # recommencer la recolte