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

# Popup window variables
show_popup = False
popup_x = screen_width // 2 - 150
popup_y = screen_height // 2 - 100
popup_width = 300
popup_height = 200

# Popup button positions and sizes
popup_button1_x = popup_x + 50
popup_button1_y = popup_y + 100
popup_button1_width = 80
popup_button1_height = 30

popup_button2_x = popup_x + 170
popup_button2_y = popup_y + 100
popup_button2_width = 80
popup_button2_height = 30

button1_enabled = True
button2_enabled = False  # Initially disabled

while not rl.window_should_close():
    # Update
    mouse_pos = rl.get_mouse_position()

    if not show_popup:
        # Check main menu button clicks
        if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(button1_x, button1_y, button1_width, button1_height)) \
            and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            show_popup = True
    else:
        # Check popup button clicks
        if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(popup_button1_x, popup_button1_y, popup_button1_width,
        popup_button1_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            print("Popup Button 1 clicked!")
            # Do something (e.g., start game as Flame Knight)
            subprocess.run(["python", "level1.py"])
            show_popup = False

        if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(popup_button2_x, popup_button2_y, popup_button2_width, popup_button2_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            print("Popup Button 2 clicked!")
            # Do something (e.g., start game as Ice Wizard)
            subprocess.run(["python", "level2.py"])
            show_popup = False

    # Draw everything
    rl.begin_drawing()
    rl.clear_background(RAYWHITE)

    if button1_enabled and rl.check_collision_point_rec(mouse_pos, rl.Rectangle(button1_x, button1_y, button1_width, button1_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        print("Button 1 clicked!")
        # Start game or do something
        button2_enabled = True  # Example: Enable button 2 after button 1 is clicked

    if button2_enabled and rl.check_collision_point_rec(mouse_pos, rl.Rectangle(button2_x, button2_y, button2_width, button2_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
        print("Button 2 clicked!")
        # Go to options or do something

    # Draw main menu buttons
    if button1_enabled:
        rl.draw_rectangle(button1_x, button1_y, button1_width, button1_height, DARKGRAY)
        rl.draw_text("Start Game", button1_x + 30, button1_y + 10, 20, WHITE)
    else:
        rl.draw_rectangle(button1_x, button1_y, button1_width, button1_height, LIGHTGRAY)
        rl.draw_text("Start Game", button1_x + 30, button1_y + 10, 20, GRAY)

    if button2_enabled:
        rl.draw_rectangle(button2_x, button2_y, button2_width, button2_height, DARKGRAY)
        rl.draw_text("Options", button2_x + 50, button2_y + 10, 20, WHITE)
    else:
        rl.draw_rectangle(button2_x, button2_y, button2_width, button2_height, LIGHTGRAY)
        rl.draw_text("Options", button2_x + 50, button2_y + 10, 20, GRAY)

    # Draw popup window
    if show_popup:
        rl.draw_rectangle(popup_x, popup_y, popup_width, popup_height, LIGHTGRAY)
        rl.draw_text("Choose your character:", popup_x + 40, popup_y + 40, 20, BLACK)

        rl.draw_rectangle(popup_button1_x, popup_button1_y, popup_button1_width, popup_button1_height, GRAY)
        rl.draw_text("Flame Knight", popup_button1_x + 10, popup_button1_y + 8, 10, WHITE)

        rl.draw_rectangle(popup_button2_x, popup_button2_y, popup_button2_width, popup_button2_height, GRAY)
        rl.draw_text("Ice Wizard", popup_button2_x + 10, popup_button2_y + 8, 10, WHITE)

    rl.end_drawing()

rl.close_window()