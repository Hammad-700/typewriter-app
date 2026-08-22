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

# --- Define the 4 sound files ---
sound_files = {
    'default': 'default.mp3',
    'enter': 'enter.mp3',
    'backspace': 'backspace.mp3',
    'capslock': 'capslock.mp3'
}

# --- Load all sounds and create channels for each ---
sounds = {}
channels = {}  # This stores a separate channel for each sound

for name, filename in sound_files.items():
    file_path = resource_path(filename)
    if not os.path.exists(file_path):
        print(f"ERROR: Cannot find {filename}!")
        print(f"Looking in: {file_path}")
        sys.exit(1)
    sounds[name] = pygame.mixer.Sound(file_path)  
    # Find a free channel for this sound
    channels[name] = pygame.mixer.find_channel()
    # If no channel is free, pygame will auto-create one, so this is safe
    if channels[name] is None:
        # Fallback: just use the default channel behavior
        channels[name] = pygame.mixer.Channel(0)
    print(f"Loaded: {filename}")

print("=========================================")
print("  GLOBAL TYPEWRITER SOUNDS ACTIVATED!    ")
print("  - ENTER       -> enter.mp3             ")
print("  - BACKSPACE   -> backspace.mp3         ")
print("  - CAPSLOCK    -> capslock.mp3          ")
print("  - ALL OTHERS  -> default.mp3           ")
print("  Press 'ESC' to stop the program.       ")
print("=========================================")

# --- Helper function to play sound without overlapping ---
def play_sound(name):
    """Plays a sound, stopping any previous playback of that same sound."""
    sound = sounds[name]
    channel = channels[name]
    
    # If this sound is currently playing, stop it first
    if channel.get_busy():
        channel.stop()
    
    # Play the sound from the beginning
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