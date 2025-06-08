from easydict import EasyDict

class Action:
    def __init__(self, action_metadata: EasyDict, list_of_actions):
        self.current_id = 0
        self.release_type = action_metadata.get("release_type", "one_time")
        self.additional_info = None
        if self.release_type == "cyclic":
            self.additional_info = action_metadata.get("additional_info", 0)
        elif self.release_type == "event":
            self.additional_info = action_metadata.get("additional_info")
        elif self.release_type == "always":
            pass
        else: 
            raise ValueError(f"Unknown release type: {self.release_type}")
            
        self.actions = list_of_actions

    def __len__(self):
        return len(self.actions)

    def step(self):
        if self.current_id < len(self.actions):
            action = self.actions[self.current_id]
            self.current_id += 1
            return action
        else:
            raise StopIteration("No more actions in the process.")
        
    def reset(self):
        self.current_id = 0
        return self.actions