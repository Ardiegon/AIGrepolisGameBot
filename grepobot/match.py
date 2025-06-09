import cv2
import numpy as np

class TemplateMatcher:
    def load_image(self, screenshot_path):
        image = cv2.imread(screenshot_path, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError(f"Screenshot image not found at {screenshot_path}")
        return image
    
    def correct_format(self, image):
        if isinstance(image, str):
            image = self.load_image(image)
        elif isinstance(image, np.ndarray):
            pass
        else:
            raise ValueError("Image must be a file path or a numpy array.")
        image = image
        return image

    def match(self, screenshot, template):
        template = self.correct_format(template)
        screenshot = self.correct_format(screenshot)
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        return result

    def get_best_match_location(self, result):
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        return max_loc
    
    def is_object_on_screen(self, result, threshold=0.43):
        _, max_val, _, _ = cv2.minMaxLoc(result)
        print("robability of match: ", max_val, ", treshold: ", threshold)
        return max_val >= threshold

    def get_middle_coordinates(self, screenshot, template):
        template = self.correct_format(template)
        screenshot = self.correct_format(screenshot)

        result = self.match(screenshot, template)

        if not self.is_object_on_screen(result):
            return None

        max_loc = self.get_best_match_location(result)
        
        h, w, _ = template.shape
        middle_x = max_loc[0] + w // 2
        middle_y = max_loc[1] + h // 2
        
        return (middle_x, middle_y)


