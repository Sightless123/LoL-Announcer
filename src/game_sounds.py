import os
import sys

if getattr(sys, "frozen", False):
    # for executable mode
    BASEDIR = sys._MEIPASS  
else:
    # for development mode
    BASEDIR = os.path.dirname(os.path.realpath(__file__))

ANNOUNCER_DIR = "Announcer"

dragon_sounds = {
    "Elder": {
        "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/elder_kill.wav",
        "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/elder_kill.wav"
    },
    "Fire": {
        "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/fire_dragon_kill.wav",
        "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/fire_dragon_kill.wav"
    },
    "Water": {
        "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/water_dragon_kill.wav",
        "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/water_dragon_kill.wav"
    },
    "Earth": {
        "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/earth_dragon_kill.wav",
        "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/earth_dragon_kill.wav"
    },
    "Air": {
        "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/air_dragon_kill.wav",
        "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/air_dragon_kill.wav"
    },
    "Chemtech": {
        "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/chemtech_dragon_kill.wav",
        "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/chemtech_dragon_kill.wav"
    },
    "Hextech": {
        "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/hextech_dragon_kill.wav",
        "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/hextech_dragon_kill.wav"
    }
}
baron_sounds = {
    "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/baron_kill.wav",
    "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/baron_kill.wav"
}
herald_sounds = {
    "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/herald_kill.wav",
    "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/herald_kill.wav"
}
champion_kill_sounds = {
    "ChampionKill": {
        "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/champion_kill.wav",
        "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/champion_kill.wav"
    },
    "Execute": f"{BASEDIR}/{ANNOUNCER_DIR}/execute/execute.wav"
}
steal_sounds = {
    "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/stolen/ally/ally_steal.wav",
    "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/stolen/enemy/enemy_steal.wav"
}
killstreak_sounds = {
    2: {
        "ally2": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/multikill_2.wav",
        "enemy2": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/multikill_2.wav"
    },
    3: {
        "ally3": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/multikill_3.wav",
        "enemy3": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/multikill_3.wav"
    },
    4: {
        "ally4": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/multikill_4.wav",
        "enemy4": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/multikill_4.wav"
    },
    5: {
        "ally5": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/multikill_5.wav",
        "enemy5": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/multikill_5.wav"
    }
}
minions_sounds = {
    "first_brick": f"{BASEDIR}/{ANNOUNCER_DIR}/minions/first_brick_minions.wav",
    "inhib": f"{BASEDIR}/{ANNOUNCER_DIR}/minions/inhib_killed_minions.wav",
    "turret": f"{BASEDIR}/{ANNOUNCER_DIR}/minions/turret_killed_minions.wav"
}
first_brick_sounds = {
    "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/first_brick.wav",
    "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/first_brick.wav"
}
turret_killed_sounds = {
    "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/turret_killed.wav",
    "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/turret_killed.wav"
}
inhib_killed_sounds = {
    "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/inhib_killed.wav",
    "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/inhib_killed.wav"
}
inhib_respawning_soon_sounds = {
    "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/inhib_respawning_soon.wav",
    "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/inhib_respawning_soon.wav"
}
inhib_respawned_sounds = {
    "ally": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/inhib_respawned.wav",
    "enemy": f"{BASEDIR}/{ANNOUNCER_DIR}/enemy/inhib_respawned.wav"
}
game_state_sounds = {
    "GameEnd": {
        "win": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/game_end_win.wav",
        "lose": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/game_end_lose.wav"
    },
    "MinionsSpawning": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/minions_spawning.wav",
    "GameStart": f"{BASEDIR}/{ANNOUNCER_DIR}/ally/game_start.wav"
}

first_blood_sound = f"{BASEDIR}/{ANNOUNCER_DIR}/first_blood/first_blood.wav"
ace_sound = f"{BASEDIR}/{ANNOUNCER_DIR}/ace/ace.wav"
