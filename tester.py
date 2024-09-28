"""
test app
"""

from pprint import pprint
from app import Match

def test_find_pattern():
    locations = Match.find_pattern(["../patterns/petit_truc.png"], threshold=0.8)
    pprint(locations)


test_find_pattern()