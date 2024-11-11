import raylibpy as rl
from raylib.colors import *
import subprocess

# Screen setup
screen_width = 800
screen_height = 600
ground_level = screen_height - 35
rl.init_window(screen_width, screen_height, "Flame Knight And Ice Wizard")

rl.set_target_fps(60)

# Button positions and sizes
button1_x = screen_width // 2 - 180
button1_y = 200
button1_width = 350
button1_height = 100

button2_x = screen_width // 2 - 180
button2_y = 400
button2_width = 350
button2_height = 100

levelselect1_texture = rl.load_texture("assets/menus/levelselect1.png")
levelselect2_texture = rl.load_texture("assets/menus/levelselect2.png")

# Audio
rl.init_audio_device()
background_music = rl.load_music_stream("assets/sounds/mainmenu.mp3")
rl.set_music_volume(background_music, 0.3)
rl.play_music_stream(background_music)


# read_levels.py

def read_levels():
    filename = "assets/levels.txt"
    level_data = {}
    with open(filename, "r") as file:
        for line in file:
            level, status = line.strip().split(" = ")
            level_data[level] = status == "true"
    return level_data


while not rl.window_should_close():

    rl.update_music_stream(background_music)

    # Mouse position update
    mouse_pos = rl.get_mouse_position()

    # Read and display levels
    levels = read_levels()
    level2 = levels['level2']

    # Draw everything
    rl.begin_drawing()
    rl.clear_background(RAYWHITE)

    if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(button1_x, button1_y, button1_width, button1_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        print("Button 1 clicked!")
        # Start game or do something
        rl.close_window()
        subprocess.run(["python", "level1.py"])

    if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(button2_x, button2_y, button2_width, button2_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        print("Button 2 clicked!")

        if level2:
            rl.close_window()
            subprocess.run(["python", "level2.py"])

    # Draw main menu buttons

    if level2:
        rl.draw_texture(levelselect2_texture, 0, 0, WHITE)
    else:
        rl.draw_texture(levelselect1_texture, 0, 0, WHITE)

    rl.end_drawing()

rl.close_window()
