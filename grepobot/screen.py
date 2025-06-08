import cv2
from mss import mss
from grepobot.match import TemplateMatcher

from grepobot.config import SCREENSHOT_PATH

class Screen:
    def __init__(self):
        self.matcher = TemplateMatcher()
        self.current_screenshot = None

    def scale_cors(self, cors):
        return (int(cors[0] / 1920 * self.sc_shape[1]), int(cors[1] / 1080 * self.sc_shape[0]))

    def take_screenshot(self, filename=SCREENSHOT_PATH):
        with mss() as sct:
            path = sct.shot(output=filename)
            screenshot = cv2.imread(path, cv2.IMREAD_COLOR)
            self.sc_shape = screenshot.shape
            self.current_screenshot = cv2.resize(screenshot, (1920, 1080)) 
        return self.current_screenshot

    def is_on_screen(self, template_path):
        screenshot = self.take_screenshot()
        result = self.matcher.match(screenshot, template_path) 
        return self.matcher.is_object_on_screen(result)
    
    def get_obj_coors(self, template_path):
        screenshot = self.take_screenshot()
        middle_coords = self.matcher.get_middle_coordinates(screenshot, template_path)
        if middle_coords is None:
            raise ValueError(f"Object not found on screen for template {template_path}.")
        return self.scale_cors(middle_coords)
    
if __name__ == "__main__":
    from time import sleep
    sleep(2)  # Wait for the screen to stabilize
    screen = Screen()
    screen.take_screenshot("screenshot.png")
    print("Screenshot taken and saved as screenshot.png")
    
    # Example usage of is_on_screen and get_obj_coors
    template_path = "grepobot\\assets\\game_objects\\closeall.png"
    coords = screen.get_obj_coors(template_path)
    if coords:
        print(f"Object found at coordinates: {coords}")
    else:
        print("Object not found on screen.")

    import cv2
    # For visualization
    bias = 10
    cv2.rectangle(screen.current_screenshot, (coords[0]-bias,coords[1]-bias), (coords[0]+bias,coords[1]+bias), (255, 0, 255), -1)
    cv2.imwshow("Match.png", screen.current_screenshot)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
