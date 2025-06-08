
class Event:
    def __init__(self, metadata, list_of_actions):
        self.current_id = 0
        self.running_condition = metadata.get("running_condition")
        self.additional_info = None
        self.happening = False
        if self.running_condition == "cyclic":
            self.additional_info = metadata.get("additional_info")
        else: 
            raise ValueError(f"Unknown running_condition: {self.running_condition}")
            
        self.actions = list_of_actions

    def step(self):
        if self.current_id < len(self.actions):
            action = self.actions[self.current_id]
            self.current_id += 1
            return action
        else:
            raise StopIteration("No more actions in the process.")
        
    def __len__(self):
        return len(self.actions)
    
    def is_last_action(self):
        return self.current_id == len(self.actions) - 1
        
    def is_happening(self):
        return self.happening
    
    def set_happening(self, value):
        if not isinstance(value, bool):
            raise ValueError("Happening value must be a boolean.")
        self.happening = value
        
    def reset(self):
        self.current_id = 0
        self.happening = False
        return self.actions