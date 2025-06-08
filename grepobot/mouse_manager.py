from abc import ABC, abstractmethod
from platform import system

which_system = system()
if which_system == "Darwin":
    import pynput.mouse as macos_mouse_module
elif which_system == "Windows":
    import mouse as windows_mouse_module
    import pyautogui
elif which_system == "Linux":
    print("Warning! Code was not tested with Linux OS, may produce errors.")
    import mouse as windows_mouse_module
    import pyautogui

class Mouse(ABC):
    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def move(self, x, y, absolute = False):
        pass

    @abstractmethod
    def click(self, side):
        pass

    @abstractmethod
    def double_click(self, side):
        pass

    @abstractmethod
    def scroll(self):
        pass

    @abstractmethod
    def move_to(self, x, y):
        pass

class WindowsMouse(Mouse):
    def __init__(self) -> None:
        super().__init__()
        self.platform = "Windows"
    
    def move(self, x, y, absolute=False):
        windows_mouse_module.move(x, y, absolute=absolute)

    def move_to(self, x, y):
        windows_mouse_module.move(x, y, absolute=True)

    def click(self, side):
        windows_mouse_module.click(side)

    def double_click(self, side):
        windows_mouse_module.double_click(side)

    def scroll(self, val):
        windows_mouse_module.wheel(-val/30)

    def hold(self):
        pyautogui.mouseDown(button='left')

    def release(self):
        pyautogui.mouseUp(button='left')

class MacosMouse(Mouse):
    def __init__(self) -> None:
        super().__init__()
        
        self.platform = "Darwin"
        self.controller = macos_mouse_module.Controller()

    def move(self, x, y, absolute=False):
        self.controller.move(x, y)
    
    def click(self, side):
        if side == "left":
            self.controller.click(macos_mouse_module.Button.left)
        else:
            self.controller.click(macos_mouse_module.Button.right)

    def double_click(self, side):
        if side == "left":
            self.controller.click(macos_mouse_module.Button.left, 2)
        else:
            self.controller.click(macos_mouse_module.Button.right, 2)

    def scroll(self, val):
        self.controller.scroll(0, val//30)

    def hold(self):
        self.controller.press(macos_mouse_module.Button.left)

    def release(self):
        self.controller.release(macos_mouse_module.Button.left)

class MouseManager():
    def __init__(self):
        self.platform = which_system

        if self.platform == "Darwin":
            self.mouse = MacosMouse()
        elif self.platform == "Windows":
            self.mouse = WindowsMouse()
        elif self.platform == "Linux":
            print("Warning! Code was not tested with Linux OS, may produce errors.")
            self.mouse = WindowsMouse()

    def move_mouse(self, move):
        self.mouse.move_to(move[0], move[1])

    def move_mouse_relative(self, move):
        self.mouse.move(move[0], move[1], absolute=False) 

    def click(self):
        self.mouse.click("left")


if __name__ == "__main__":
    mouse_manager = MouseManager()
    mouse_manager.move_mouse((100, 100))
    mouse_manager.click()
    print(f"Mouse moved to (100, 100) and clicked on {mouse_manager.platform} platform.")

