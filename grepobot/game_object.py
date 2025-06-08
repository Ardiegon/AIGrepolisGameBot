import os
from grepobot.config import OBJECTS_IMAGE_PATH
from grepobot.screen import Screen

class GameObject:
    def __init__(self, name):
        self.name = name
        self.path = os.path.join(OBJECTS_IMAGE_PATH, f"{name}.png")
    
    def is_obj_on_screen(self, screen: Screen):
        is_it = screen.is_on_screen(self.path)
        return is_it
    
    def get_obj_coors(self, screen: Screen):
        coors = screen.get_obj_coors(self.path)
        if not coors:
            raise ValueError(f"Object {self.name} not found on screen.")
        return coors
    
