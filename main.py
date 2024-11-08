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
            player.speed.y = -5
            player.can_jump = False
            player.jump_timer = 0.0
    else:
        if rl.is_key_down(rl.KEY_LEFT):
            player.position.x -= 4
        if rl.is_key_down(rl.KEY_RIGHT):
            player.position.x += 4
        if rl.is_key_down(rl.KEY_UP) and player.can_jump and player.jump_timer >= 0.5:
            player.speed.y = -5
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

def check_border_collision():
    if flame_knight.position.x < 0:
        flame_knight.position.x = 0
        flame_knight.speed.x = 0  # Stop movement left
    elif flame_knight.position.x + flame_knight.size.x > screen_width:
        flame_knight.position.x = screen_width - flame_knight.size.x
        flame_knight.speed.x = 0  # Stop movement right

    if flame_knight.position.y < 0:
        flame_knight.position.y = 0
        flame_knight.speed.y = 0  # Stop movement up
    elif flame_knight.position.y + flame_knight.size.y > screen_height:
        flame_knight.position.y = screen_height - flame_knight.size.y
        flame_knight.speed.y = 0  # Stop movement down
    
    # Ice Wizard border collision
    if ice_wizard.position.x < 0:
        ice_wizard.position.x = 0
        ice_wizard.speed.x = 0  # Stop movement left
    elif ice_wizard.position.x + ice_wizard.size.x > screen_width:
        ice_wizard.position.x = screen_width - ice_wizard.size.x
        ice_wizard.speed.x = 0  # Stop movement right

    if ice_wizard.position.y < 0:
        ice_wizard.position.y = 0
        ice_wizard.speed.y = 0  # Stop movement up
    elif ice_wizard.position.y + ice_wizard.size.y > screen_height:
        ice_wizard.position.y = screen_height - ice_wizard.size.y
        ice_wizard.speed.y = 0  # Stop movement down
        
# Screen setup
screen_width = 800
screen_height = 600
ground_level = screen_height - 35
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
        if tile_id != 0:  
            red_goal = rl.Rectangle(x * tile_width, y * tile_height, tile_width, tile_height)

ice_goal_layer = level_data['layers'][6]
for y in range(ice_goal_layer['height']):
    for x in range(ice_goal_layer['width']):
        tile_id = ice_goal_layer['data'][y * ice_goal_layer['width'] + x]
        if tile_id != 0:  
            blue_goal = rl.Rectangle(x * tile_width, y * tile_height, tile_width, tile_height)

# Defining Hazards
waters = []
water_layer = level_data['layers'][2]
for y in range(water_layer['height']):
    for x in range(water_layer['width']):
        tile_id = water_layer['data'][y * water_layer['width'] + x]
        if tile_id != 0:  
            platform_rect = rl.Rectangle(x * tile_width, y * tile_height, tile_width, tile_height)
            platform_color = BLUE  
            waters.append(Platform(platform_rect, platform_color))

lavas = []
lava_layer = level_data['layers'][3]
for y in range(lava_layer['height']):
    for x in range(lava_layer['width']):
        tile_id = lava_layer['data'][y * lava_layer['width'] + x]
        if tile_id != 0:  
            platform_rect = rl.Rectangle(x * tile_width, y * tile_height, tile_width, tile_height)
            platform_color = ORANGE  
            lavas.append(Platform(platform_rect, platform_color))

goos = []
goo_layer = level_data['layers'][4]
for y in range(goo_layer['height']):
    for x in range(goo_layer['width']):
        tile_id = goo_layer['data'][y * goo_layer['width'] + x]
        if tile_id != 0:  
            platform_rect = rl.Rectangle(x * tile_width, y * tile_height, tile_width, tile_height)
            platform_color = GREEN  
            goos.append(Platform(platform_rect, platform_color))


# Flags to check if players reached the goal
flame_knight_reached_goal = False
ice_wizard_reached_goal = False

# Set the target FPS
rl.set_target_fps(60)

# Game loop
# Game loop
while not rl.window_should_close():
    move_player(flame_knight, True)
    move_player(ice_wizard, False)

    # Update vertical movement (gravity effect)
    flame_knight.speed.y += 0.3
    ice_wizard.speed.y += 0.3

    # Update player rectangles for collision detection
    flame_knight_rect = rl.Rectangle(flame_knight.position.x, flame_knight.position.y, flame_knight.size.x, flame_knight.size.y)
    ice_wizard_rect = rl.Rectangle(ice_wizard.position.x, ice_wizard.position.y, ice_wizard.size.x, ice_wizard.size.y)

    # Collision with standard platforms
    for platform in platforms:
        handle_platform_collision(flame_knight, platform)
        handle_platform_collision(ice_wizard, platform)

    # Handle Border Collision
    check_border_collision()

    # Hazard collision detection
    for water in waters:
        rl.draw_rectangle_rec(water.rect, water.color)  # Draw water platform
        if rl.check_collision_recs(flame_knight_rect, water.rect):
            # Game over if Flame Knight touches water
            print("Flame Knight touched water! Game Over!")
            # Reset game here
            flame_knight.position = rl.Vector2(100, 500)
            ice_wizard.position = rl.Vector2(200, 500)

    for lava in lavas:
        rl.draw_rectangle_rec(lava.rect, lava.color)  # Draw lava platform
        if rl.check_collision_recs(ice_wizard_rect, lava.rect):
            # Game over if Ice Wizard touches lava
            print("Ice Wizard touched lava! Game Over!")
            # Reset game here
            flame_knight.position = rl.Vector2(100, 500)
            ice_wizard.position = rl.Vector2(200, 500)

    for goo in goos:
        rl.draw_rectangle_rec(goo.rect, goo.color)  # Draw goo platform
        if rl.check_collision_recs(flame_knight_rect, goo.rect) or rl.check_collision_recs(ice_wizard_rect, goo.rect):
            # Game over if either character touches goo
            print("Player touched goo! Game Over!")
            # Reset game here
            flame_knight.position = rl.Vector2(100, 500)
            ice_wizard.position = rl.Vector2(200, 500)

    
    # Update jump timers
    flame_knight.jump_timer += rl.get_frame_time()
    ice_wizard.jump_timer += rl.get_frame_time()

    # Check if both players have reached their respective goals
    flame_knight_reached_goal = rl.check_collision_recs(flame_knight_rect, red_goal)
    ice_wizard_reached_goal = rl.check_collision_recs(ice_wizard_rect, blue_goal)

    # Draw everything
    rl.begin_drawing()
    rl.clear_background(RAYWHITE)

    # Draw platforms
    for platform in platforms:
        rl.draw_rectangle_rec(platform.rect, platform.color)

    # Draw players
    rl.draw_rectangle_rec(flame_knight_rect, flame_knight.color)
    rl.draw_rectangle_rec(ice_wizard_rect, ice_wizard.color)

    # Draw goals
    rl.draw_rectangle_rec(red_goal, RED)
    rl.draw_rectangle_rec(blue_goal, BLUE)

    # Display level complete message
    if flame_knight_reached_goal and ice_wizard_reached_goal:
        rl.draw_text("Level Complete!", screen_width // 2 - 100, screen_height // 2, 20, GREEN)

    rl.draw_rectangle_lines(0, 0, screen_width, screen_height, BLACK)

    rl.end_drawing()

# Close window
rl.close_window()
