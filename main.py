import pyray as rl
import json
from raylib.colors import *

MAX_PLATFORMS = 20

class Player:
    def __init__(self, position, size, color):
        self.position = position
        self.size = size
        self.speed = rl.Vector2(0, 0)
        self.color = color
        self.can_jump = True
        self.jump_timer = 0.0

class Platform:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

def move_player(player, is_flame_knight):
    if is_flame_knight:
        if rl.is_key_down(rl.KEY_A):
            player.position.x -= 4
        if rl.is_key_down(rl.KEY_D):
            player.position.x += 4
        if rl.is_key_down(rl.KEY_W) and player.can_jump and player.jump_timer >= 0.5:
            player.speed.y = -10
            player.can_jump = False
            player.jump_timer = 0.0
    else:
        if rl.is_key_down(rl.KEY_LEFT):
            player.position.x -= 4
        if rl.is_key_down(rl.KEY_RIGHT):
            player.position.x += 4
        if rl.is_key_down(rl.KEY_UP) and player.can_jump and player.jump_timer >= 0.5:
            player.speed.y = -10
            player.can_jump = False
            player.jump_timer = 0.0

    player.position.y += player.speed.y

def handle_platform_collision(player, platform):
    player_rect = rl.Rectangle(player.position.x, player.position.y, player.size.x, player.size.y)

    if rl.check_collision_recs(player_rect, platform.rect):
        overlap_top = player.position.y + player.size.y - platform.rect.y
        overlap_bottom = platform.rect.y + platform.rect.height - player.position.y
        overlap_left = player.position.x + player.size.x - platform.rect.x
        overlap_right = platform.rect.x + platform.rect.width - player.position.x

        if overlap_top < overlap_bottom and overlap_top < overlap_left and overlap_top < overlap_right:
            player.position.y = platform.rect.y - player.size.y
            player.speed.y = 0
            player.can_jump = True
        elif overlap_bottom < overlap_top and overlap_bottom < overlap_left and overlap_bottom < overlap_right:
            player.position.y = platform.rect.y + platform.rect.height
            player.speed.y = 0
        elif overlap_left < overlap_right:
            player.position.x = platform.rect.x - player.size.x
            player.speed.x = 0
        else:
            player.position.x = platform.rect.x + platform.rect.width
            player.speed.x = 0


# Screen setup
screen_width = 800
screen_height = 600
rl.init_window(screen_width, screen_height, "Flame Knight And Ice Wizard")

# Players setup
flame_knight = Player(rl.Vector2(100, 500), rl.Vector2(20, 35), ORANGE)
ice_wizard = Player(rl.Vector2(200, 500), rl.Vector2(20, 35), SKYBLUE)

# Load the JSON level file
with open('map/level1.json', 'r') as f:
    level_data = json.load(f)

# Extract the foreground layer (assuming it's the second layer in the JSON)
foreground_layer = level_data['layers'][1]  # Adjust index based on your JSON structure

# Tile size (adjust to your actual tile size)
tile_width = 25
tile_height = 25

# Create platforms based on the foreground layer (tiles with value != 0)
platforms = []
for y in range(foreground_layer['height']):
    for x in range(foreground_layer['width']):
        tile_id = foreground_layer['data'][y * foreground_layer['width'] + x]
        if tile_id != 0:  # Non-zero value means a tile is present here
            platform_rect = rl.Rectangle(x * tile_width, y * tile_height, tile_width, tile_height)
            platform_color = DARKGRAY  # Default color for the platforms
            platforms.append(Platform(platform_rect, platform_color))

# Defining Goals
flame_goal_layer = level_data['layers'][5]
for y in range(flame_goal_layer['height']):
    for x in range(flame_goal_layer['width']):
        tile_id = flame_goal_layer['data'][y * flame_goal_layer['width'] + x]
        if tile_id != 0:  # Non-zero value means a tile is present here
            red_goal = rl.Rectangle(x * tile_width, y * tile_height, tile_width, tile_height)

ice_goal_layer = level_data['layers'][6]
for y in range(ice_goal_layer['height']):
    for x in range(ice_goal_layer['width']):
        tile_id = ice_goal_layer['data'][y * ice_goal_layer['width'] + x]
        if tile_id != 0:  # Non-zero value means a tile is present here
            blue_goal = rl.Rectangle(x * tile_width, y * tile_height, tile_width, tile_height)

# Defining Hazards



# Flags to check if players reached the goal
flame_knight_reached_goal = False
ice_wizard_reached_goal = False

# Set the target FPS
rl.set_target_fps(60)

# Game loop
while not rl.window_should_close():
    move_player(flame_knight, True)
    move_player(ice_wizard, False)

    # Code for mouse pos
    #mouse_x, mouse_y = rl.get_mouse_x(), rl.get_mouse_y()
    #rl.draw_text(f"X: {mouse_x} Y: {mouse_y}", mouse_x + 10, mouse_y + 10, 10, rl.RED)

    flame_knight.speed.y += 0.5
    ice_wizard.speed.y += 0.5

    flame_knight_rect = rl.Rectangle(flame_knight.position.x, flame_knight.position.y, flame_knight.size.x, flame_knight.size.y)
    ice_wizard_rect = rl.Rectangle(ice_wizard.position.x, ice_wizard.position.y, ice_wizard.size.x, ice_wizard.size.y)

    for platform in platforms:
        handle_platform_collision(flame_knight, platform)
        handle_platform_collision(ice_wizard, platform)

    flame_knight.position.x = max(0, min(screen_width - flame_knight.size.x, flame_knight.position.x))
    ice_wizard.position.x = max(0, min(screen_width - ice_wizard.size.x, ice_wizard.position.x))

    flame_knight.jump_timer += rl.get_frame_time()
    ice_wizard.jump_timer += rl.get_frame_time()

    flame_knight_reached_goal = rl.check_collision_recs(flame_knight_rect, red_goal)
    ice_wizard_reached_goal = rl.check_collision_recs(ice_wizard_rect, blue_goal)

    rl.begin_drawing()
    rl.clear_background(RAYWHITE)

    # Draw the level platforms created from the JSON data
    for platform in platforms:
        rl.draw_rectangle_rec(platform.rect, platform.color)

    # Draw players
    rl.draw_rectangle_rec(flame_knight_rect, flame_knight.color)
    rl.draw_rectangle_rec(ice_wizard_rect, ice_wizard.color)

    # Draw the goals
    rl.draw_rectangle_rec(red_goal, RED)
    rl.draw_rectangle_rec(blue_goal, BLUE)

    # Display message if both players reached their goals
    if flame_knight_reached_goal and ice_wizard_reached_goal:
        rl.draw_text("Level Complete!", screen_width // 2 - 100, screen_height // 2, 20, GREEN)

    rl.end_drawing()

# Close window
rl.close_window()
