from grepobot.mouse_manager import MouseManager
from grepobot.screen import Screen
from grepobot.registry import Registry, build_registry, FlowHelper
from grepobot.utils.common import format_time
from wakepy import keep

import time

class Brain:
    def __init__(self, game_data):
        self.registry:Registry = build_registry()
        self.screen = Screen()
        self.mouse_manager = MouseManager()
        self.game_data = game_data

        self.round_time = game_data["round_time"]
        self.start_time = time.time()
        self.end_time = self.start_time + self.round_time * game_data["rounds"]

        self.game_actions_names = []
        self.game_events_names = []

        self.priority_list = []

        self.action_scheduler = {}
        self.event_scheduler = {}

        self.populate_actions_and_events()

    def populate_actions_and_events(self):
        for action_name in self.game_data["actions"]:
            self.game_actions_names.append(action_name)
            action = self.registry(action_name)
            if action.release_type == "cyclic":
                self.action_scheduler[action_name] = self.start_time
            if action.release_type == "event":
                event_name = action.additional_info
                if event_name in self.game_events_names:
                    continue
                event = self.registry(event_name)
                self.game_events_names.append(event_name)
                if event.running_condition == "cyclic":
                    self.event_scheduler[event_name] = self.start_time 

    def print_game_state_info(self):
        print("Current time: ", format_time(time.time()))
        print("Scheduled Actions:")
        for action, t in self.action_scheduler.items():
            print(f"Action {action} scheduled {format_time(t)}")
        print("Scheduled Events:")
        for event, t in self.event_scheduler.items():
            print(f"Event {event} scheduled {format_time(t)}")
        

    def propagate(self, action_list):
        all_results = []
        for action in action_list:
            time.sleep(0.1) # so the actions could propagate
            name = action["name"]
            service = action["service"]
            game_object = self.registry(name)
            if isinstance(game_object, FlowHelper):
                # If it's a flow helper, call it directly
                game_object(service)
                result = None
            else:
                # Otherwise, call the method corresponding to the action
                result = getattr(self, service)(game_object)
            all_results.append(result)
        return all_results
         
    def propagate_event(self, event_name):
        event = self.registry(event_name)
        propagation_result = self.propagate(event.actions)
        if propagation_result[-1] is True:
            self.registry(event_name).happening = True
            return True
        return False

    def propagate_action(self, action_name):
        action = self.registry(action_name)
        self.propagate(action.actions)

    def reset_all(self):
        for name in self.game_actions_names:
            action = self.registry(name)
            action.reset()
        for name in self.game_events_names:
            event = self.registry(name)
            event.reset()

    def check_every_event(self):
        for event_name in self.game_events_names:
            current_time = time.time()
            next_event_time = self.event_scheduler[event_name]
            if current_time >= next_event_time:
                print(f"Doing event: {event_name}")
                result = self.propagate_event(event_name)
                print(f"{event_name} is happening: {result}")

    def propagate_all_actions(self):
        for action_name in self.game_actions_names:
            action = self.registry(action_name)
            if action.release_type == "always":
                print(f"Doing action {action_name}")
                self.propagate_action(action_name)
                print(f"Finished action {action_name}")
            if action.release_type == "cyclic":
                current_time = time.time()
                next_action_time = self.action_scheduler[action_name]
                if current_time >= next_action_time:
                    print(f"Doing action {action_name}")
                    self.propagate_action(action_name)
                    finished_time = time.time()
                    self.action_scheduler[action_name] = finished_time + action.additional_info
                    print(f"Action {action_name} will run next in {format_time(self.action_scheduler[action_name])} (curr: {format_time(finished_time)})")
                else:
                    print(f"Action {action_name} waiting.")
            if action.release_type == "event":
                event_name = action.additional_info
                event = self.registry(event_name)
                if event.happening:
                    print(f"Doing action {action_name}")
                    self.propagate_action(action_name)
                    event.set_happening(False)
                    print(f"Action {action_name} reacted to {event_name}.")
                
    def run(self):
        with keep.presenting():
            while self.round_time < self.end_time:
                self.current_round_time = time.time()
                print("NEXT TURN")
                self.print_game_state_info()
                self.check_every_event()
                self.propagate_all_actions()
                self.reset_all()
                self.sleep_until_end_of_round()

    def click(self, game_object):
        print(f"Clicking on game object: {game_object.name}")
        try:
            coords = game_object.get_obj_coors(self.screen)
            self.mouse_manager.move_mouse(coords)
            self.mouse_manager.click()
        except Exception as e:
            print(f"While clicking on game object {game_object.name}: {e}")
        

    def hover(self, game_object):
        print(f"Hovering on game object: {game_object.name}")
        try:
            coords = game_object.get_obj_coors(self.screen)
            self.mouse_manager.move_mouse(coords)
        except Exception as e:
            print(f"While hovering on game object {game_object.name}: {e}")

    def check(self, game_object):
        print(f"Checking game object: {game_object.name}")
        if not game_object.is_obj_on_screen(self.screen):
            return False
        return True
    
    def sleep_until_end_of_round(self):
        elapsed_time = time.time() - self.current_round_time
        if elapsed_time < self.round_time:
            sleep_time = self.round_time - elapsed_time
            print(f"Sleeping for {sleep_time} seconds until the end of the round.")
            time.sleep(sleep_time)
        else:
            print("Round time has already passed, no need to sleep.")
        

