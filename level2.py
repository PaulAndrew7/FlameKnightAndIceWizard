import raylibpy as rl
import json
from raylib.colors import *

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

class Elevator:
    def __init__(self, rect, color, range_y=100):  # Default range_y is 100 if not provided
        self.rect = rect
        self.color = color
        self.range_y = range_y  # This is the range of vertical movement
        self.start_y = rect.y
        self.current_y = rect.y
        self.direction = 1

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
    

# Border collision check
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


def handle_lever1(player):
    global elevator1_active  # Declare elevator1_active as global
    
    player_rect = rl.Rectangle(player.position.x, player.position.y, player.size.x, player.size.y)

    if rl.check_collision_recs(player_rect, lever1):
        if (rl.is_key_pressed(rl.KEY_S) and player == flame_knight) or \
           (rl.is_key_pressed(rl.KEY_DOWN) and player == ice_wizard):
            # Toggle the elevator's active state
            elevator1_active = not elevator1_active

def update_elevator1(elevator, elevator_active):
    
    max_y = elevator.start_y  # Calculate max_y relative to start_y
    min_y = elevator.start_y - elevator.range_y  # Calculate min_y relative to start_y

    if elevator_active:
        if elevator.current_y > max_y:
            elevator.direction = -1  # Move up
        elif elevator.current_y < min_y:
            elevator.direction = 1   # Move down
        
        elevator.current_y += elevator.direction  # Adjust speed as needed
    

    elevator.rect.y = elevator.current_y

def update_elevator2(elevator, elevator_active):
    max_y = elevator.start_y - elevator.range_y  # Highest position (top of the range)
    min_y = elevator.start_y  # Starting position (lowest point)

    if elevator_active:
        # Move up until reaching max_y
        if elevator.current_y > max_y:
            elevator.direction = -1  # Move up
            elevator.current_y += elevator.direction  # Adjust speed as needed
    else:
        # Move down until reaching min_y, then stop
        if elevator.current_y < min_y:
            elevator.current_y += 1  # Move down slowly
        else:
            elevator.current_y = min_y  # Snap to starting position to ensure it stays there

    # Update the elevator's rectangle position
    elevator.rect.y = elevator.current_y


def handle_buttons(button, player):
    # Check if a given player is colliding with the button
    player_rect = rl.Rectangle(player.position.x, player.position.y, player.size.x, player.size.y)
    return rl.check_collision_recs(player_rect, button)


# Screen setup
screen_width = 800
screen_height = 600
ground_level = screen_height - 35
rl.init_window(screen_width, screen_height, "Flame Knight And Ice Wizard")

# Players setup
# 100, 500
flame_knight = Player(rl.Vector2(200, 200), rl.Vector2(20, 35), BLACK)
ice_wizard = Player(rl.Vector2(200, 500), rl.Vector2(20, 35), BLACK)

# Load the JSON level file
with open('map/level1.json', 'r') as f:
    level_data = json.load(f)

# Extract the foreground layer 
foreground_layer = level_data['layers'][1]  # Adjust index based on your JSON structure

# Tile size (adjust to your actual tile size)
tile_width = 25
tile_height = 25

# Create platforms based on the foreground layer (tiles with value != 0)
platforms = []
for y in range(foreground_layer['height']):
    for x in range(foreground_layer['width']):
        tile_id = foreground_layer['data'][y * foreground_layer['width'] + x]
        if tile_id != 0:  #
            # Non-zero value means a tile is present here
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
            platform_rect = rl.Rectangle(x * tile_width, (y * tile_height) + (tile_height // 2) + 1, tile_width, tile_height // 2)
            platform_color = BLUE  
            waters.append(Platform(platform_rect, platform_color))

lavas = []
lava_layer = level_data['layers'][3]
for y in range(lava_layer['height']):
    for x in range(lava_layer['width']):
        tile_id = lava_layer['data'][y * lava_layer['width'] + x]
        if tile_id != 0:  
            platform_rect = rl.Rectangle(x * tile_width, (y * tile_height) + (tile_height // 2) + 1, tile_width, tile_height // 2)
            platform_color = ORANGE  
            lavas.append(Platform(platform_rect, platform_color))

goos = []
goo_layer = level_data['layers'][4]
for y in range(goo_layer['height']):
    for x in range(goo_layer['width']):
        tile_id = goo_layer['data'][y * goo_layer['width'] + x]
        if tile_id != 0:  
            platform_rect = rl.Rectangle(x * tile_width,(y * tile_height) + (tile_height // 2) + 1, tile_width, tile_height // 2)
            platform_color = GREEN  
            goos.append(Platform(platform_rect, platform_color))

lever_layer = level_data['layers'][7]
for y in range(lever_layer['height']):
    for x in range(lever_layer['width']):
        tile_id = lever_layer['data'][y * lever_layer['width'] + x]
        if tile_id != 0:  # Non-zero value means a tile is present here
            lever1 = rl.Rectangle(x * tile_width, y * tile_height, tile_width, tile_height)


# Elevator 1 

elevator_layer = level_data['layers'][8]  # Your elevator layer
for y in range(elevator_layer['height']):
    x = 0
    while x < elevator_layer['width']:
        tile_id = elevator_layer['data'][y * elevator_layer['width'] + x]
        if tile_id != 0:  # Non-zero tile means part of the elevator
            width_count = 1
            while (x + width_count < elevator_layer['width'] and 
                   elevator_layer['data'][y * elevator_layer['width'] + x + width_count] != 0 and 
                   width_count < 4):
                width_count += 1

            # Create a single elevator platform rectangle
            elevator_rect = rl.Rectangle(x * tile_width, y * tile_height, width_count * tile_width, tile_height)
            elevator_color = BROWN
            # Create the elevator and append it to the list
            elevator1 = Elevator(elevator_rect, elevator_color, 80)

            x += width_count
        else:
            x += 1
            
elevator1_active = False  # Single boolean variable for the elevator

# Elevator 2

elevator_layer = level_data['layers'][10]  # Your elevator layer
for y in range(elevator_layer['height']):
    x = 0
    while x < elevator_layer['width']:
        tile_id = elevator_layer['data'][y * elevator_layer['width'] + x]
        if tile_id != 0:  # Non-zero tile means part of the elevator
            width_count = 1
            while (x + width_count < elevator_layer['width'] and 
                   elevator_layer['data'][y * elevator_layer['width'] + x + width_count] != 0 and 
                   width_count < 4):
                width_count += 1

            # Create a single elevator platform rectangle
            elevator_rect = rl.Rectangle(x * tile_width, y * tile_height, width_count * tile_width, tile_height)
            elevator_color = BROWN
            # Create the elevator and append it to the list
            elevator2 = Elevator(elevator_rect, elevator_color, 50)

            x += width_count
        else:
            x += 1
            
elevator2_active = False  # Single boolean variable for the elevator

# Button 1
buttons = []
button_layer = level_data['layers'][9]
for y in range(button_layer['height']):
    for x in range(button_layer['width']):
        tile_id = button_layer['data'][y * lever_layer['width'] + x]
        if tile_id != 0:  # Non-zero value means a tile is present here
            buttons.append(rl.Rectangle(x * tile_width, y * tile_height, tile_width, tile_height))
button1 = buttons[0]
button2 = buttons[1]

# Flags to check if players reached the goal
flame_knight_reached_goal = False
ice_wizard_reached_goal = False

# Set the target FPS
rl.set_target_fps(60)

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

    
    # Update jump timers
    flame_knight.jump_timer += rl.get_frame_time()
    ice_wizard.jump_timer += rl.get_frame_time()

    # Check if both players have reached their respective goals
    flame_knight_reached_goal = rl.check_collision_recs(flame_knight_rect, red_goal)
    ice_wizard_reached_goal = rl.check_collision_recs(ice_wizard_rect, blue_goal)

    # --- Lever and Elevator Logic ---
    
    handle_lever1(flame_knight)
    handle_lever1(ice_wizard)

    update_elevator1(elevator1, elevator1_active)
    handle_platform_collision(flame_knight, elevator1)  # Handle collision with the elevator
    handle_platform_collision(ice_wizard, elevator1)   # Handle collision with the elevator 

    # --- End of Lever and Elevator Logic ---
    
    # Hazard collision detection

    
    for water in waters:
        rl.draw_rectangle_rec(water.rect, water.color)

    for water in waters:
        if rl.check_collision_recs(flame_knight_rect, water.rect):
            print("Flame Knight touched water! Game Over!")
            flame_knight.position = rl.Vector2(100, 500) 
            ice_wizard.position = rl.Vector2(200, 500)
        elif rl.check_collision_recs(ice_wizard_rect, water.rect):
            ice_wizard.can_jump = True

    for lava in lavas:
        rl.draw_rectangle_rec(lava.rect, lava.color)

    for lava in lavas:
        if rl.check_collision_recs(ice_wizard_rect, lava.rect):
            print("Ice Wizard touched lava! Game Over!")
            flame_knight.position = rl.Vector2(100, 500)
            ice_wizard.position = rl.Vector2(200, 500)
        elif rl.check_collision_recs(flame_knight_rect, lava.rect):
            flame_knight.can_jump = True
    for goo in goos:
        rl.draw_rectangle_rec(goo.rect, goo.color)

    for goo in goos:
        if rl.check_collision_recs(flame_knight_rect, goo.rect) or \
           rl.check_collision_recs(ice_wizard_rect, goo.rect):
            print("Player touched goo! Game Over!")
            flame_knight.position = rl.Vector2(100, 500)
            ice_wizard.position = rl.Vector2(200, 500)

    # Draw everything
    rl.begin_drawing()
    rl.clear_background(RAYWHITE)

    # Draw platforms
    for platform in platforms:
        rl.draw_rectangle_rec(platform.rect, platform.color)

    # Draw the elevator
    rl.draw_rectangle_rec(elevator1.rect, elevator1.color)

    # Draw players
    rl.draw_rectangle_rec(flame_knight_rect, flame_knight.color)
    rl.draw_rectangle_rec(ice_wizard_rect, ice_wizard.color)

    # Draw goals
    rl.draw_rectangle_rec(red_goal, RED)
    rl.draw_rectangle_rec(blue_goal, BLUE)

    # Draw levers
    rl.draw_rectangle_rec(lever1, DARKGREEN)

    # Draw second elevator
    rl.draw_rectangle_rec(elevator2.rect, elevator2.color)

    # Draw buttons
    rl.draw_rectangle_rec(button1, YELLOW)
    rl.draw_rectangle_rec(button2, YELLOW)

    # Button Handling
    elevator2_active = False

# Check each player for collisions with buttons
    if handle_buttons(button1, flame_knight) or handle_buttons(button1, ice_wizard):
        elevator2_active = True

    # Do the same for other buttons if needed, such as button2
    if handle_buttons(button2, flame_knight) or handle_buttons(button2, ice_wizard):
        elevator2_active = True
    
    update_elevator2(elevator2, elevator2_active)
    handle_platform_collision(flame_knight, elevator2)  # Handle collision with the elevator
    handle_platform_collision(ice_wizard, elevator2)

    # Display level complete message
    if flame_knight_reached_goal and ice_wizard_reached_goal:
        rl.draw_text("Level Complete!", screen_width // 2 - 100, screen_height // 2, 20, GREEN)

    rl.draw_rectangle_lines(0, 0, screen_width, screen_height, BLACK)

    rl.end_drawing()

# Close window
rl.close_window()