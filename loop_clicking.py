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
        go1 = GameObject("loginscreen")
        val = go1.is_obj_on_screen(screen)
        if val:
            go1 = GameObject("world")
            cors = go1.get_obj_coors(screen)
            mouse_manager.move_mouse(cors)
            mouse_manager.click()
            time.sleep(2.0)
        go1 = GameObject("captcha")
        val = go1.is_obj_on_screen(screen)
        if val:
            go1 = GameObject("captchaclick")
            cors = go1.get_obj_coors(screen)
            mouse_manager.move_mouse(cors)
            mouse_manager.click()
            time.sleep(1.0) 
            go1 = GameObject("captchaconf")
            cors = go1.get_obj_coors(screen)
            mouse_manager.move_mouse(cors)
            mouse_manager.click()
            time.sleep(2.0) 
        go1 = GameObject("podglad")
        cors = go1.get_obj_coors(screen)
        mouse_manager.move_mouse(cors)
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
        time.sleep(0.5) 
        go1 = GameObject("closeall")
        cors = go1.get_obj_coors(screen) 
        mouse_manager.move_mouse(cors)
        mouse_manager.click()
        print("Mouse clicked")
        time.sleep(60*5+5)
