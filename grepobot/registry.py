import os
import yaml
import time
from enum import Enum

from grepobot.game_object import GameObject
from grepobot.action import Action
from grepobot.event import Event
from grepobot.config import OBJECTS_IMAGE_PATH, ACTIONS_CONFIG_PATH, EVENTS_CONFIG_PATH

class RegistryType(Enum):
    OBJECT = "object"
    ACTION = "action"

class FlowType(Enum):
    WAIT = "WAIT"

class FlowHelper:
    def __init__(self, flow_type):
        self.type = flow_type

    def __call__(self, value):
        getattr(self, self.type.name)(value)
    
    def WAIT(self, value):
        time.sleep(value)


class Registry:
    def __init__(self):
        self.objects = {}
        self.actions = {}
        self.events = {}

    def register_game_object(self, name):
        if name not in self.objects:
            self.objects[name] = GameObject(name)
    
    def register_action(self, action_name, action_metadata, list_of_actions):
        if action_name not in self.actions:
            self.actions[action_name] = Action(action_metadata, list_of_actions)

    def register_event(self, event_name, event_metadata, list_of_actions):
        if event_name not in self.events:
            self.events[event_name] = Event(event_metadata, list_of_actions)

    def __call__(self, name):
        if name in self.objects.keys():
            return self.objects[name]
        elif name in self.actions.keys():
            return self.actions[name]
        elif name in self.events.keys():
            return self.events[name]
        elif name in FlowType.__members__.keys():
            return FlowHelper(FlowType[name])
        else:
            raise ValueError(f"Unknown type: {type}")
    
    def __repr__(self):
        result = "Registry Contents:\n"
        result += "Objects:\n"
        for name, obj in self.objects.items():
            result+= f"Object: {name}, Path: {obj.path}\n"
            result+="-" * 20 + "\n"
        result += "Actions:\n"
        for name, action in self.actions.items():
            result+=f"Action: {name}, Metadata: {action.release_type}, More: {action.additional_info}\n"
            result+=f"Actions: {action.actions}\n"
            result+="-" * 20 + "\n"
        result += "Events:\n"
        for name, event in self.events.items():
            result+=f"Event: {name}, Metadata: {event.running_condition}, More: {event.additional_info}\n"
            result+=f"Actions: {event.actions}\n"
            result+="-" * 20 + "\n"
        return result

    def untangle_action(self, actions):
        """
        Untangles a list of actions, so it contents is made only from game objects.
        """
        def until_done_untangle_action(tangled_actions):
            untangled_actions = []
            action_in_current_actions = False
            for action in tangled_actions:
                if action["name"].isupper(): # if Flow Helper, let it pass unchanged
                    untangled_actions += [action]
                elif action["service"] == "action":
                    action_in_current_actions = True
                    tangled_action_name = action["name"]
                    new_actions = self.actions[tangled_action_name].actions
                    untangled_actions += new_actions
                else:
                    untangled_actions += [action]
            if action_in_current_actions:
                return until_done_untangle_action(untangled_actions)
            else:
                return untangled_actions
            
        result = until_done_untangle_action(actions)
        return result
    
def build_registry():
    registry = Registry()
    
    for filename in os.listdir(OBJECTS_IMAGE_PATH):
        if filename.endswith(".png"):
            name = filename[:-4]
            registry.register_game_object(name)
    
    with open(ACTIONS_CONFIG_PATH, 'r') as file:
        actions_config = yaml.safe_load(file)
        for action_name, action in actions_config.items():
            untangled_actions = registry.untangle_action(action["actions"])
            registry.register_action(action_name, action["metadata"], untangled_actions)
    
    with open(EVENTS_CONFIG_PATH, 'r') as file:
        events_config = yaml.safe_load(file)
        for event_name, event in events_config.items():
            untangled_actions = registry.untangle_action(event["actions"])
            registry.register_event(event_name, event["metadata"], untangled_actions)

    return registry


if __name__ == "__main__":
    print(FlowType.__members__.keys())
    name = "WAIT"
    print(FlowType[name])

    waithelper = FlowHelper(FlowType.WAIT)
    waithelper(0.2)  # This will wait for 2 seconds

    print(FlowType[name])
    # Example usage of the registry
    registry = build_registry()
    print(registry)  # This will print the contents of the registry

    action = registry("GetResources")
    print(action.current_id)

    event = registry("CaptchaOnTheScreen")
    print(registry("CaptchaOnTheScreen").happening)
    event.happening = True
    print(registry("CaptchaOnTheScreen").happening)
    event.reset()
    print(registry("CaptchaOnTheScreen").happening)