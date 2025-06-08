import time
from grepobot.mouse_manager import MouseManager
from grepobot.game_object import GameObject
from grepobot.screen import Screen

# def scale_cors(cors):
#     """Scale coordinates to match the screen resolution."""
#     return (int(cors[0] / 1920 * 2560), int(cors[1] / 1080 * 1440))

if __name__ == "__main__":
    mouse_manager = MouseManager()
    screen = Screen()
    while True:
        time.sleep(0.5) 
        go1 = GameObject("podglad")
        cors = go1.get_obj_coors(screen)
        mouse_manager.move_mouse(cors)
        # mouse_manager.click()
        time.sleep(0.5)
        go1 = GameObject("wioski")
        cors = go1.get_obj_coors(screen) 
        mouse_manager.move_mouse(cors)
        mouse_manager.click()
        time.sleep(0.5) 
        go1 = GameObject("wybwszystkie")
        cors = go1.get_obj_coors(screen) 
        mouse_manager.move_mouse(cors)
        mouse_manager.click()
        time.sleep(0.5) 
        go1 = GameObject("odbierz")
        cors = go1.get_obj_coors(screen) 
        mouse_manager.move_mouse(cors)
        mouse_manager.click()
        print("Mouse clicked")
        time.sleep(60*5)
