import pygame
import keyboard
import sys
import time
import os

# Initialize sound system
pygame.mixer.init()

# --- Find MP3 files (works for script and .exe) ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- Define the 5 sound files (added 'space') ---
sound_files = {
    'default': 'default.mp3',
    'enter': 'enter.mp3',
    'backspace': 'backspace.mp3',
    'capslock': 'capslock.mp3',
    'space': 'space.mp3'  # <-- NEW SPACE SOUND
}

# --- Load all sounds and create channels for each ---
sounds = {}
channels = {}

for name, filename in sound_files.items():
    file_path = resource_path(filename)
    if not os.path.exists(file_path):
        print(f"ERROR: Cannot find {filename}!")
        print(f"Looking in: {file_path}")
        sys.exit(1)
    sounds[name] = pygame.mixer.Sound(file_path)
    channels[name] = pygame.mixer.find_channel()
    if channels[name] is None:
        channels[name] = pygame.mixer.Channel(0)
    print(f"Loaded: {filename}")

print("=========================================")
print("  GLOBAL TYPEWRITER SOUNDS ACTIVATED!    ")
print("  - ENTER       -> enter.mp3             ")
print("  - BACKSPACE   -> backspace.mp3         ")
print("  - CAPSLOCK    -> capslock.mp3          ")
print("  - SPACE       -> space.mp3             ")  # <-- NEW
print("  - ALL OTHERS  -> default.mp3           ")
print("  Press 'ESC' to stop the program.       ")
print("=========================================")

# --- Helper function to play sound without overlapping ---
def play_sound(name):
    sound = sounds[name]
    channel = channels[name]
    if channel.get_busy():
        channel.stop()
    channel.play(sound)

# --- This runs every time you press a key ---
def on_press(e):
    if e.name == 'esc':
        keyboard.unhook_all()
        pygame.mixer.quit()
        os._exit(0)
        return

    # Play the right sound for each key
    if e.name == 'enter':
        play_sound('enter')
    elif e.name == 'backspace':
        play_sound('backspace')
    elif e.name == 'caps lock' or e.name == 'caps_lock':
        play_sound('capslock')
    elif e.name == 'space':  # <-- NEW SPACE CHECK
        play_sound('space')
    else:
        play_sound('default')

# Hook into Windows globally
keyboard.on_press(on_press)

# Keep running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit(0)