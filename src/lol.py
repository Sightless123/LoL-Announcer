import time
import webbrowser
import subprocess
import os
import json
import requests

from lcu_driver import Connector
from cursesmenu import CursesMenu
from cursesmenu.items import FunctionItem, SubmenuItem, ExitItem
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import game_sounds
from utils import play_sound

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


PROJECT_URL = "https://github.com/Sightless123/LoL-Announcer"
LOCALGAME_URL = "https://127.0.0.1:2999/liveclientdata/allgamedata"


class GameMenu:
    announcer_volume = 1.0
    lcu_client = Connector()

    def __init__(self):
        self.announcer = Announcer()

    def show_menu(self):
        # Prepare main menu items
        self.menu = CursesMenu("Game Menu", "Select an option:", show_exit_item = False)
        item1 = FunctionItem("Turn on League of Legends", self.start_league)
        item2 = FunctionItem("Start announcer", self.start_announcer)
        item3 = FunctionItem("Auto accept match", self.start_auto_accept)
        item4 = FunctionItem("Open the Github project", self.open_github)
        exit_program = ExitItem("Exit")
        # Options submenu items
        submenu = CursesMenu("Options", "Select an option:", show_exit_item = False)
        submenu_item = SubmenuItem("Options", submenu, menu=self.menu)
        sound_adjustment = FunctionItem("Adjust announcer volume", self.start_volume_adjustment)
        toggle_native_announcer = FunctionItem("Toggle default LoL announcer mute", self.toggle_native_announcer_mute)
        submenu_exit = ExitItem("Exit")
        # Attach options to menus
        self.menu.items.append(item1)
        self.menu.items.append(item2)
        self.menu.items.append(item3)
        self.menu.items.append(item4)
        self.menu.items.append(submenu_item)
        self.menu.items.append(exit_program)
        submenu.items.append(sound_adjustment)
        submenu.items.append(toggle_native_announcer)
        submenu.items.append(submenu_exit)
        self.menu.show()

    def start_announcer(self):
        self.menu.pause()
        self.announcer.start(self.announcer_volume)
        self.menu.resume()

    def find_file_path(self, file_name, search_in_config=False):
        base_paths = [
            os.path.join("C:", "ProgramFiles", "Riot Games", "League of Legends"),
            os.path.join("C:", "ProgramFiles(x86)", "Riot Games", "League of Legends"),
            os.path.join("D:", "ProgramFiles", "Riot Games", "League of Legends"),
            os.path.join("D:", "ProgramFiles(x86)", "Riot Games", "League of Legends"),
            os.path.join("C:", "Riot Games", "League of Legends"),
            os.path.join("D:", "Riot Games", "League of Legends")
        ]

        if search_in_config:
            base_paths = [
                os.path.join(path, "Config") for path in base_paths
            ]

        possible_paths = [
            os.path.join(path, file_name) for path in base_paths
        ]

        for path in possible_paths:
            if os.path.isfile(path):
                return path

        return None

    def toggle_native_announcer_mute(self):
        self.menu.pause()
        file_name = "PersistedSettings.json"
        file_path = self.find_file_path(file_name, search_in_config=True)

        with open(file_path, "r") as json_file:
            data = json.load(json_file)

        for file_data in data["files"]:
            if file_data["name"] == "Game.cfg":
                for section in file_data["sections"]:
                    if section["name"] == "Volume":
                        for setting in section["settings"]:
                            if setting["name"] == "AnnouncerMute":
                                current_value = setting["value"]
                                setting["value"] = "1" if current_value == "0" else "0"
                                if setting["value"] == "0":
                                    print("Announcer unmuted.")
                                else:
                                    print("Announcer muted.")

        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
            time.sleep(2)
            self.menu.resume()

    def start_league(self):
        self.menu.pause()
        file_name = "LeagueClient.exe"
        file_path = self.find_file_path(file_name)

        if file_path:
            try:
                subprocess.run(file_path)
                print("Opening League of Legends!")
            except FileNotFoundError:
                print("File found but unable to execute.")
        else:
            print("League of Legends executable not found.")
        time.sleep(2)
        self.menu.resume()

    def start_volume_adjustment(self):
        self.menu.pause()
        sound_volume = 100
        while True:
            user_input = input("Enter '+' to increase volume, '-' to decrease, or 'q' to quit: ")
            if user_input == "+":
                sound_volume = (min(100, round(sound_volume + 10)))
                print("Volume increased. Durrent volume: ", sound_volume)
            elif user_input == "-":
                sound_volume = (max(0, round(sound_volume - 10)))
                print("Volume decreased. Current volume: ", sound_volume)
            elif user_input.lower() == "q":
                break
            else:
                print("Invalid input. Try again.")
        print("Volume adjustment finished.")
        self.announcer_volume = sound_volume / 100
        time.sleep(2)
        self.menu.resume()

    def open_github(self):
        webbrowser.open(PROJECT_URL)

    def start_auto_accept(self):
        # Needed to be in scope of this function to access self(.lcu_client) to exit
        @self.lcu_client.ws.register("/lol-matchmaking/v1/ready-check", event_types=("UPDATE",))
        async def auto_accept_match(connection, event):
            if event.data["playerResponse"] == "None":
                await connection.request("post", "/lol-matchmaking/v1/ready-check/accept")

        @self.lcu_client.ws.register("/lol-gameflow/v1/session", event_types=("UPDATE",))
        async def is_in_game(connection, event):
            if event.data["gameClient"]["running"]:
                await self.lcu_client.stop()

        print("Matches are being auto-accepted!")
        self.lcu_client.start()

class Announcer:
    last_processed_event_index = 0
    volume = 1.0
    game_is_over = False

    def __init__(self):
        self.event_handlers = {
            "DragonKill": self.handle_dragon_kill,
            "BaronKill": self.handle_baron_kill,
            "HeraldKill": self.handle_herald_kill,
            "ChampionKill": self.handle_champion_kill,
            "FirstBlood": self.handle_first_blood,
            "Ace": self.handle_ace,
            "Multikill": self.handle_multikill,
            "FirstBrick": self.handle_first_brick,
            "TurretKilled": self.handle_turret_killed,
            "InhibKilled": self.handle_inhib_killed,
            "InhibRespawningSoon": self.handle_inhib_respawning_soon,
            "InhibRespawned": self.handle_inhib_respawned,
            "GameStart": self.handle_game_start,
            "MinionsSpawning": self.handle_minions_spawning,
            "GameEnd": self.handle_game_end
        }

    def detect_game(self):
        for _ in range(30):
            try:
                res = self.get_game_data()
                if res.status_code == 200:
                    return True
            except:
                print("Looking for running game...")
                time.sleep(1)
        print("No game found!")
        time.sleep(3)

    def get_game_data(self):
        return requests.get(LOCALGAME_URL, verify=False,
            timeout= 30
        )

    def get_player_team(self, player_name):
        for player in self.game_data["allPlayers"]:
            if player["summonerName"] == player_name:
                return player["team"]

    def process_event(self, event):
        event_name = event["EventName"]
        if event_name in self.event_handlers:
            self.event_handlers[event_name](event)

    def is_objective_stolen(self, event):
        if event["Stolen"] == "True":
            if self.get_player_team(event["KillerName"]) == self.local_player_team:
                stolen_sound = game_sounds.steal_sounds["ally"]
            else:
                stolen_sound = game_sounds.steal_sounds["enemy"]

            return stolen_sound

    def handle_dragon_kill(self, event):
        dragon_type = event["DragonType"]
        killer_team = self.get_player_team(event["KillerName"])
        player_team = self.local_player_team
        team_type = "ally" if killer_team == player_team else "enemy"
        if dragon_type in game_sounds.dragon_sounds:
            dragon = game_sounds.dragon_sounds[dragon_type]

            stolen_sound = self.is_objective_stolen(event)
            if stolen_sound:
                team_type = "ally" if killer_team == player_team else "enemy"
                print(f"The {dragon_type} dragon has been stolen, playing {team_type} steal sound!")
                play_sound(stolen_sound, self.volume)
            else:
                kill_sound = dragon["ally"] if killer_team == player_team else dragon["enemy"]
                print(f"{dragon_type} dragon has been slain, playing {team_type} {dragon_type} dragon kill sound!")
                play_sound(kill_sound, self.volume)
        else:
            print(f"Dragon type '{dragon_type}' not found in game sounds dictionary.")

    def handle_baron_kill(self, event):
        killer_team = self.get_player_team(event["KillerName"])
        player_team = self.local_player_team
        team_type = "ally" if killer_team == player_team else "enemy"
        baron_sound = game_sounds.baron_sounds
        stolen_sound = self.is_objective_stolen(event)
        if stolen_sound:
            print(f"Baron Nashor has been stolen, playing {team_type} steal sound!")
            play_sound(stolen_sound, self.volume)
        else:
            kill_sound = baron_sound["ally"] if killer_team == player_team else baron_sound["enemy"]
            print(f"Baron Nashor has been slain, playing {team_type} kill sound!")
            play_sound(kill_sound, self.volume)

    def handle_herald_kill(self, event):
        killer_team = self.get_player_team(event["KillerName"])
        player_team = self.local_player_team
        herald_sound = game_sounds.herald_sounds
        stolen_sound = self.is_objective_stolen(event)
        team_type = "ally" if killer_team == player_team else "enemy"
        if stolen_sound:
            print(f"Herald has been stolen, playing {team_type} steal sound!")
            play_sound(stolen_sound, self.volume)
        else:
            kill_sound = herald_sound["ally"] if killer_team == player_team else herald_sound["enemy"]
            print(f"Herald has been slain, playing {team_type} kill sound!")
            play_sound(kill_sound, self.volume)

    def handle_champion_kill(self, event):
        killer_team = self.get_player_team(event["KillerName"])
        player_team = self.local_player_team
        execute_sound = game_sounds.champion_kill_sounds["Execute"]
        champion_sound = game_sounds.champion_kill_sounds["ChampionKill"]
        if "_" in event["KillerName"]:
            print("A player has been executed, playing execute sound")
            play_sound(execute_sound, self.volume)
        else:
            kill_sound = champion_sound["ally"] if killer_team == player_team else champion_sound["enemy"]
            team_type = "ally" if killer_team == player_team else "enemy"
            print(f"A champion has been slain, playing {team_type} kill sound!")
            play_sound(kill_sound, self.volume)

    def handle_first_blood(self, event):
        first_blood_sound = game_sounds.first_blood_sound
        print("First blood has been spilled, playing first blood sound!")
        play_sound(first_blood_sound, self.volume)

    def handle_ace(self, event):
        ace_sound = game_sounds.ace_sound
        print("All players have been exterminated, playing ace sound!")
        play_sound(ace_sound, self.volume)

    def handle_multikill(self, event):
        multikill_streak = event["KillStreak"]
        killer_team = self.get_player_team(event["KillerName"])
        player_team = self.local_player_team
        if multikill_streak in game_sounds.killstreak_sounds:
            killstreak = game_sounds.killstreak_sounds[multikill_streak]
            kill_sound = killstreak[f"ally{multikill_streak}"] if killer_team == player_team else killstreak[f"enemy{multikill_streak}"]
            team_type = "ally" if killer_team == player_team else "enemy"
            print(f"An {team_type} has achieved a kill combo of {multikill_streak}, playing {team_type} sound!")
            play_sound(kill_sound, self.volume)

    def handle_first_brick(self, event):
        killer_team = self.get_player_team(event["KillerName"])
        player_team = self.local_player_team
        first_brick_sound = game_sounds.first_brick_sounds
        if "Minion_T" in event["KillerName"]:
            first_brick_sound = game_sounds.minions_sounds["first_brick"]
            print("A minion has destroyed the first turret, playing minion first turret sound!")
            play_sound(first_brick_sound, self.volume)
            time.sleep(1)
        else:
            if killer_team == player_team:
                play_sound(first_brick_sound["ally"], self.volume)
            else:
                play_sound(first_brick_sound["enemy"], self.volume)
            team_type = "ally" if killer_team == player_team else "enemy"
            print(f"The {team_type} has destroyed the first turret, playing first turret sound!")
            time.sleep(1)

    def handle_turret_killed(self, event):
        killer_team = self.get_player_team(event["KillerName"])
        player_team = self.local_player_team
        turret_killed_sound = game_sounds.turret_killed_sounds
        if "Minion_T" in event["KillerName"]:
            turret_killed_sound = game_sounds.minions_sounds["turret"]
            print("A minion has destroyed a turret, playing minion turret sound!")
            play_sound(turret_killed_sound, self.volume)
        else:
            if killer_team == player_team:
                play_sound(turret_killed_sound["ally"], self.volume)
            else:
                play_sound(turret_killed_sound["enemy"], self.volume)
            team_type = "ally" if killer_team == player_team else "enemy"
            print(f"The {team_type} has destroyed a turret, playing turret sound!")

    def handle_inhib_killed(self, event):
        killer_team = self.get_player_team(event["KillerName"])
        player_team = self.local_player_team
        inhib_killed_sound = game_sounds.inhib_killed_sounds
        if "Minion_T" in event["KillerName"]:
            inhib_killed_sound = game_sounds.minions_sounds["inhib"]
            print("A minion has destroyed an inhibitor, playing minion inhibitor sound!")
            play_sound(inhib_killed_sound, self.volume)
        else:
            kill_sound = inhib_killed_sound["ally"] if killer_team == player_team else inhib_killed_sound["enemy"]
            team_type = "ally" if killer_team == player_team else "enemy"
            print(f"The {team_type} has destroyed an inhibitor, playing inhibitor sound!")
            play_sound(kill_sound, self.volume)

    def handle_inhib_respawning_soon(self, event):
        player_team = self.local_player_team
        inhib_respawning_soon_sound = game_sounds.inhib_respawning_soon_sounds
        if "_T1_" in event["InhibRespawningSoon"]:
            inhibitor_team = "ORDER"
        elif "_T2_" in event["InhibRespawningSoon"]:
            inhibitor_team = "CHAOS"
        if player_team == inhibitor_team:
            inhib_respawning_soon_sound = game_sounds.inhib_respawning_soon_sounds["ally"]
            print("An inhibitor is respawning soon, playing inhibitor respawning soon sound!")
            play_sound(inhib_respawning_soon_sound, self.volume)
        else:
            inhib_respawning_soon_sound = game_sounds.inhib_respawning_soon_sounds["enemy"]
            print("An enemy inhibitor is respawning soon, playing inhibitor respawning soon sound!")
            play_sound(inhib_respawning_soon_sound, self.volume)

    def handle_inhib_respawned(self, event):
        player_team = self.local_player_team
        inhib_respawned_sound = game_sounds.inhib_respawning_soon_sounds
        if "_T1_" in event["InhibRespawned"]:
            inhibitor_team = "ORDER"
        elif "_T2_" in event["InhibRespawned"]:
            inhibitor_team = "CHAOS"

        if player_team == inhibitor_team:
            inhib_respawned_sound = game_sounds.inhib_respawned_sounds["ally"]
            print("An inhibitor has respawned, playing inhibitor respawn sound!")
            play_sound(inhib_respawned_sound, self.volume)
        else:
            inhib_respawned_sound = game_sounds.inhib_respawned_sounds["enemy"]
            print("An enemy inhibitor has respawned, playing inhibitor respawn sound!")
            play_sound(inhib_respawned_sound, self.volume)

    def handle_game_start(self, event):
        game_start_sound = game_sounds.game_state_sounds["GameStart"]
        print("The game has started, playing start sound!")
        play_sound(game_start_sound, self.volume)

    def handle_minions_spawning(self, event):
        minions_spawning_sound = game_sounds.game_state_sounds["MinionsSpawning"]
        print("The minions have spawned, playing minion spawn sound!")
        play_sound(minions_spawning_sound, self.volume)

    def handle_game_end(self, event):
        if event["Result"] == "Win":
            game_end_sound = game_sounds.game_state_sounds["GameEnd"]["win"]
            print("You have won the game, playing win sound!")
            play_sound(game_end_sound, self.volume)
            self.game_is_over = True
        elif event["Result"] == "Lose":
            game_end_sound = game_sounds.game_state_sounds["GameEnd"]["lose"]
            print("You have lost the game, playing loss sound!")
            play_sound(game_end_sound, self.volume)
            self.game_is_over = True

    def start(self, volume):
        self.volume = volume
        if self.detect_game():
            self.game_data = self.get_game_data().json()
            self.local_player_team = self.get_player_team(self.game_data["activePlayer"]["summonerName"])
            self.last_processed_event_index = 0
            while True:
                game_data_res = self.get_game_data()
                if game_data_res.status_code == 200:
                    self.game_data = game_data_res.json()
                    # Extract the list of events
                    events = self.game_data["events"]["Events"]

                    # Process new events from the last processed index
                    for i in range(self.last_processed_event_index, len(events)):
                        self.process_event(events[i])

                    if self.game_is_over: break

                    # Update the index to the latest event
                    self.last_processed_event_index = len(events)
                time.sleep(1)

if __name__ == "__main__":
    menu = GameMenu()
    menu.show_menu()
