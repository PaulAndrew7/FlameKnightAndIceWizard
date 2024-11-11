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
button1_x = screen_width // 2 - 100
button1_y = 360
button1_width = 200
button1_height = 70

button2_x = screen_width // 2 - 100
button2_y = 500
button2_width = 200
button2_height = 70

mainmenu_texture = rl.load_texture("assets/menus/main menu.png")

# Audio
rl.init_audio_device()
background_music = rl.load_music_stream("assets/sounds/mainmenu.mp3")
rl.set_music_volume(background_music, 0.3)
rl.play_music_stream(background_music)

while not rl.window_should_close():

    rl.update_music_stream(background_music)

    # Mouse position update
    mouse_pos = rl.get_mouse_position()

    # Draw everything
    rl.begin_drawing()
    rl.clear_background(RAYWHITE)

    if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(button1_x, button1_y, button1_width, button1_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        print("Button 1 clicked!")
        # Start game or do something
        rl.close_window()
        subprocess.run(["python", "levels.py"])

    if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(button2_x, button2_y, button2_width, button2_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        print("Button 2 clicked!")
        r1.close_window()
        # Go to options or do something

    # Draw main menu buttons

    rl.draw_rectangle(button1_x, button1_y, button1_width,
                      button1_height, DARKGRAY)

    rl.draw_rectangle(button2_x, button2_y, button2_width,
                      button2_height, DARKGRAY)

    rl.draw_texture(mainmenu_texture, 0, 0, WHITE)

    rl.end_drawing()

rl.close_window()
