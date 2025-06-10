import time
import argparse
from grepobot.mouse_manager import MouseManager
from grepobot.game_object import GameObject
from grepobot.screen import Screen
from grepobot.utils.common import format_time
from wakepy import keep

def parse_args():
    parser = argparse.ArgumentParser(description="Grepobot CLI")
    parser.add_argument("--version", action="version", version="Grepobot 0.1.0")
    parser.add_argument("--work-hours", type=float, help="For how many hours the program should work?", default=4.0)
    
    return parser.parse_args()

def move_and_click(mouse_manager, cors):
    mouse_manager.move_mouse(cors)
    time.sleep(0.2)
    mouse_manager.click()

def single_loop(mouse_manager, screen):
    go1 = GameObject("misje")
    cors = go1.get_obj_coors(screen) 
    time.sleep(0.2)
    move_and_click(mouse_manager, cors)
    time.sleep(1.5)

    go1 = GameObject("captcha")
    val = go1.is_obj_on_screen(screen)
    time.sleep(0.2)
    flag = False
    if val:
        flag=True
        go1 = GameObject("captchaclick")
        cors = go1.get_obj_coors(screen)
        move_and_click(mouse_manager, cors)
        time.sleep(1.0) 
        go1 = GameObject("captchaconf")
        cors = go1.get_obj_coors(screen)
        move_and_click(mouse_manager, cors)
        time.sleep(2.0)

    go1 = GameObject("loginscreen")
    val = go1.is_obj_on_screen(screen)
    time.sleep(0.3) 
    if val:
        go1 = GameObject("world")
        cors = go1.get_obj_coors(screen)
        move_and_click(mouse_manager, cors)
        time.sleep(2.0)
    if not val and not flag:
        go1 = GameObject("closeall")
        cors = go1.get_obj_coors(screen) 
        move_and_click(mouse_manager, cors)

    go1 = GameObject("captcha")
    val = go1.is_obj_on_screen(screen)
    time.sleep(0.3)
    if val:
        go1 = GameObject("captchaclick")
        cors = go1.get_obj_coors(screen)
        move_and_click(mouse_manager, cors)
        time.sleep(1.0) 
        go1 = GameObject("captchaconf")
        cors = go1.get_obj_coors(screen)
        move_and_click(mouse_manager, cors)
        time.sleep(2.0) 

    go1 = GameObject("podglad")
    cors = go1.get_obj_coors(screen)
    mouse_manager.move_mouse(cors)
    time.sleep(0.5) 
    go1 = GameObject("wioski")
    cors = go1.get_obj_coors(screen) 
    move_and_click(mouse_manager, cors)
    time.sleep(0.5) 
    go1 = GameObject("wybwszystkie")
    cors = go1.get_obj_coors(screen) 
    move_and_click(mouse_manager, cors)
    time.sleep(0.5) 
    go1 = GameObject("odbierz")
    cors = go1.get_obj_coors(screen) 
    move_and_click(mouse_manager, cors)
    time.sleep(0.5) 

    go1 = GameObject("closeall")
    cors = go1.get_obj_coors(screen) 
    move_and_click(mouse_manager, cors)
    print("Mouse clicked")
    time.sleep(60*5+5)

if __name__ == "__main__":
    args = parse_args()
    start = time.time()
    work_seconds = args.work_hours*60*60
    print(f"Will work untill {format_time(start + work_seconds)}")
    time.sleep(3)
    mouse_manager = MouseManager()
    screen = Screen()
    break_counter = 0
    with keep.presenting():
        while work_seconds > time.time() - start:
            try:
                single_loop(mouse_manager, screen)
                break_counter=0
            except:
                print("Something went wrong, wait and try again")
                if break_counter > 3:
                    print("Ending, as program encountered weird error")
                    break
                time.sleep(10)
                break_counter+=1
                
            
