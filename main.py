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
button1_y = screen_height // 2 - 60
button1_width = 200
button1_height = 40

button2_x = screen_width // 2 - 100
button2_y = screen_height // 2 + 20
button2_width = 200
button2_height = 40


while not rl.window_should_close():
    # Update
    mouse_pos = rl.get_mouse_position()

    
    if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(button1_x, button1_y, button1_width, button1_height)) \
        and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        show_popup = True

    # Draw everything
    rl.begin_drawing()
    rl.clear_background(RAYWHITE)

    if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(button1_x, button1_y, button1_width, button1_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        print("Button 1 clicked!")
        # Start game or do something
        button2_enabled = True  # Example: Enable button 2 after button 1 is clicked

    if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(button2_x, button2_y, button2_width, button2_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        print("Button 2 clicked!")
        # Go to options or do something

    # Draw main menu buttons

    rl.draw_rectangle(button1_x, button1_y, button1_width, button1_height, DARKGRAY)
    rl.draw_text("Start Game", button1_x + 30, button1_y + 10, 20, WHITE)
    


    rl.draw_rectangle(button2_x, button2_y, button2_width, button2_height, DARKGRAY)
    rl.draw_text("Options", button2_x + 50, button2_y + 10, 20, WHITE)



    rl.end_drawing()

rl.close_window()