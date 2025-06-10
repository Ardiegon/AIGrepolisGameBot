import time
from grepobot.mouse_manager import MouseManager
from grepobot.game_object import GameObject
from grepobot.screen import Screen
from wakepy import keep


if __name__ == "__main__":
    mouse = MouseManager()
    screen = Screen()

    for i in range(4):
        time.sleep(2.0)
        # pos = []
        # pos.append(mouse.position())
        # print(pos[-1])
        mouse.click()
    

    screenshot = screen.take_screenshot()
    shape = screen.sc_shape
    print(shape)



    