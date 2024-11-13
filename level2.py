import raylibpy as rl
import json
from raylib.colors import *
import time
import subprocess
from math import fabs


class Player:
    def __init__(self, position, size, color):
        self.position = position
        self.size = size
        self.speed = rl.Vector2(0, 0)
        self.color = color
        self.can_jump = True
        self.jump_timer = 0.0
        self.facing_right = True
        self.facing_left = False


class Enemy:
    def __init__(self, position, size, detection_range_size, color, speed):
        self.position = position
        self.size = size
        self.detection_range_size = detection_range_size
        self.detection_range_position = rl.Vector2(
            position.x - (detection_range_size.x - size.x) / 2, position.y - (detection_range_size.y - size.y) / 2)
        self.color = color
        self.speed = rl.Vector2(speed, speed)
        self.active = False
        self.gravity = 0.5
        self.openeyes = True

    def update(self, flame_knight, ice_wizard):
        # Update detection range position to stay above the enemy
        self.detection_range_position.x = self.position.x - \
            (self.detection_range_size.x - self.size.x) / 2
        self.detection_range_position.y = (
            self.position.y - (self.detection_range_size.y - self.size.y) / 2) - 10

        # Gravity
        self.speed.y += self.gravity
        self.position.y += self.speed.y

        # Platform Collision Handling
        for platform in platforms:
            handle_platform_collision(self, platform)

        # Elevator collision handling
        handle_platform_collision(self, elevator1)
        handle_platform_collision(self, elevator2)
        handle_platform_collision(self, elevator3)
        handle_platform_collision(self, elevator4)
        handle_platform_collision(self, elevator5)
        handle_platform_collision(self, elevator6)

        # Check if players are in detection range
        flame_knight_in_range = rl.check_collision_recs(
            rl.Rectangle(self.detection_range_position.x, self.detection_range_position.y,
                         self.detection_range_size.x, self.detection_range_size.y),
            rl.Rectangle(flame_knight.position.x, flame_knight.position.y,
                         flame_knight.size.x, flame_knight.size.y)
        )

        ice_wizard_in_range = rl.check_collision_recs(
            rl.Rectangle(self.detection_range_position.x, self.detection_range_position.y,
                         self.detection_range_size.x, self.detection_range_size.y),
            rl.Rectangle(ice_wizard.position.x, ice_wizard.position.y,
                         ice_wizard.size.x, ice_wizard.size.y)
        )

        # Activate if any player is in detection range
        if not self.active:
            self.active = flame_knight_in_range or ice_wizard_in_range

        # Calculate distances to each player
        dist_flame_knight = abs(self.position.x - flame_knight.position.x) + \
            abs(self.position.y - flame_knight.position.y)
        dist_ice_wizard = abs(self.position.x - ice_wizard.position.x) + \
            abs(self.position.y - ice_wizard.position.y)

        # Choose the closest player
        target_player = flame_knight if dist_flame_knight < dist_ice_wizard else ice_wizard

        # Only move if active, player is outside detection range, and player's y-position is in range
        if self.active and (self.position.y >= target_player.position.y >= self.position.y - 50):
            if self.position.x < target_player.position.x:
                if not target_player.facing_left:
                    self.position.x += self.speed.x
                    self.openeyes = True
                else:
                    self.openeyes = False
            elif self.position.x > target_player.position.x:
                if target_player.facing_left:
                    self.position.x -= self.speed.x
                    self.openeyes = True
                else:
                    self.openeyes = False
        self.rect = rl.Rectangle(
            self.position.x, self.position.y, self.size.x, self.size.y)
        if rl.check_collision_recs(flame_knight_rect, self.rect) or rl.check_collision_recs(ice_wizard_rect, self.rect):
            global show_over
            show_over = True

    def draw(self):
        # Draw enemy structure
        if self.active:
            if self.openeyes:
                rl.draw_texture_pro(
                    enemy_active_texture,
                    rl.Rectangle(0, 0, enemy_active_texture.width,
                                 enemy_active_texture.height),
                    rl.Rectangle(self.position.x, self.position.y,
                                 self.size.x, self.size.y),
                    rl.Vector2(0, 0),
                    0,
                    WHITE
                )
            else:
                rl.draw_texture_pro(
                    enemy_inactive_texture,
                    rl.Rectangle(0, 0, enemy_inactive_texture.width,
                                 enemy_inactive_texture.height),
                    rl.Rectangle(self.position.x, self.position.y,
                                 self.size.x, self.size.y),
                    rl.Vector2(0, 0),
                    0,
                    WHITE
                )
        else:
            rl.draw_texture_pro(
                enemy_inactive_texture,
                rl.Rectangle(0, 0, enemy_inactive_texture.width,
                             enemy_inactive_texture.height),
                rl.Rectangle(self.position.x, self.position.y,
                             self.size.x, self.size.y),
                rl.Vector2(0, 0),
                0,
                WHITE
            )

        # Draw detection range (optional for debugging)
        """rl.draw_rectangle_lines_ex(
            rl.Rectangle(self.detection_range_position.x, self.detection_range_position.y, 
                         self.detection_range_size.x, self.detection_range_size.y), 1, rl.RED
        )"""


enemy1 = Enemy(rl.Vector2(400, 300), rl.Vector2(
    30, 30), rl.Vector2(200, 60), rl.RED, 1)
enemy2 = Enemy(rl.Vector2(450, 350), rl.Vector2(
    30, 30), rl.Vector2(200, 60), rl.RED, 1)


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

# Write level data


def write_levels(data):
    filename = "assets/levels.txt"
    with open(filename, "w") as file:
        for level, status in data.items():
            file.write(f"{level} = {str(status).lower()}\n")
    print("Level data written to file.")

# Platform and player collision handling


def handle_platform_collision(player, platform):
    player_rect = rl.Rectangle(
        player.position.x, player.position.y, player.size.x, player.size.y)

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

    # Flame Knight border collision
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


# Handling interaction with lever 1
def handle_lever1(player):
    global elevator1_active
    global interact_sound_played

    player_rect = rl.Rectangle(
        player.position.x, player.position.y, player.size.x, player.size.y)

    if rl.check_collision_recs(player_rect, lever1):
        if (rl.is_key_pressed(rl.KEY_S) and player == flame_knight) or \
           (rl.is_key_pressed(rl.KEY_DOWN) and player == ice_wizard):
            # Toggle the elevator's active state
            elevator1_active = not elevator1_active
            rl.play_sound(interact_sound)

# Handling interaction with lever 2


def handle_lever2(player):
    global elevator4_active
    global interact_sound_played

    player_rect = rl.Rectangle(
        player.position.x, player.position.y, player.size.x, player.size.y)

    if rl.check_collision_recs(player_rect, lever2):
        if (rl.is_key_pressed(rl.KEY_S) and player == flame_knight) or \
           (rl.is_key_pressed(rl.KEY_DOWN) and player == ice_wizard):
            # Toggle the elevator's active state
            elevator4_active = not elevator4_active
            rl.play_sound(interact_sound)


# Elevator type 1 updates
def update_elevator1(elevator, elevator_active):

    max_y = elevator.start_y
    min_y = elevator.start_y - elevator.range_y

    if elevator_active:
        if elevator.current_y > max_y:
            elevator.direction = -1  # Move up
        elif elevator.current_y < min_y:
            elevator.direction = 1   # Move down

        elevator.current_y += elevator.direction

    elevator.rect.y = elevator.current_y

# Elevator type 2 updates


def update_elevator2(elevator, elevator_active):

    max_y = elevator.start_y - elevator.range_y
    min_y = elevator.start_y  #

    if elevator_active:

        if elevator.current_y > max_y:
            elevator.direction = -1  # Move up
            elevator.current_y += elevator.direction
    else:

        if elevator.current_y < min_y:
            elevator.current_y += 1
        else:
            elevator.current_y = min_y

    elevator.rect.y = elevator.current_y


# Check player collision with button
def handle_buttons(button, player):
    player_rect = rl.Rectangle(
        player.position.x, player.position.y, player.size.x, player.size.y)
    return rl.check_collision_recs(player_rect, button)


# Screen setup
screen_width = 800
screen_height = 600
ground_level = screen_height - 35
rl.init_window(screen_width, screen_height, "Flame Knight And Ice Wizard")


# Loading textures
level2_texture = rl.load_texture("assets/textures/level2.png")
elevator_texture = rl.load_texture("assets/textures/elevator.png")
elevatorflipped_texture = rl.load_texture(
    "assets/textures/elevatorflipped.png")
button_on_texture = rl.load_texture("assets/textures/button_on.png")
button_off_texture = rl.load_texture("assets/textures/button_off.png")
button2_on_texture = rl.load_texture("assets/textures/button2_on.png")
button2_off_texture = rl.load_texture("assets/textures/button2_off.png")
button3_on_texture = rl.load_texture("assets/textures/button3_on.png")
button3_off_texture = rl.load_texture("assets/textures/button3_off.png")
lever_on_texture = rl.load_texture("assets/textures/lever_on.png")
lever_off_texture = rl.load_texture("assets/textures/lever_off.png")
flame_knight_texture1 = rl.load_texture("assets/characters/flameknight1.png")
flame_knight_texture2 = rl.load_texture("assets/characters/flameknight2.png")
ice_wizard_texture1 = rl.load_texture("assets/characters/icewizard1.png")
ice_wizard_texture2 = rl.load_texture("assets/characters/icewizard2.png")
pause_texture = rl.load_texture("assets/menus/pause.png")
complete_texture = rl.load_texture("assets/menus/complete.png")
gameover_texture = rl.load_texture("assets/menus/gameover.png")
enemy_inactive_texture = rl.load_texture("assets/textures/enemy_inactive.png")
enemy_active_texture = rl.load_texture("assets/textures/enemy_active.png")
# Animation Speed for characters
animation_speed = 10

# Audio
rl.init_audio_device()
background_music = rl.load_music_stream("assets/sounds/level1.mp3")
rl.set_music_volume(background_music, 0.9)
rl.play_music_stream(background_music)

# Sound Effects
flame_knight_jump_sound = rl.load_sound("assets/sounds/flame_knight_jump.wav")
ice_wizard_jump_sound = rl.load_sound("assets/sounds/ice_wizard_jump.wav")
interact_sound = rl.load_sound("assets/sounds/interact.ogg")
interact_sound_played = False
button1_last_state = False
button2_last_state = False
button3_last_state = False

# Set volume
rl.set_music_volume(background_music, 0.8)


# Popup Window status
show_pause = False
show_over = False
show_complete = False

# Character Animation
last_texture_swap_time_fk = time.time()
current_texture_fk = flame_knight_texture1


def animate_flame_knight(player, current_texture_fk):

    if rl.is_key_down(rl.KEY_W):
        if player.facing_left:
            source_rect = rl.Rectangle(
                0, 0, -flame_knight_texture1.width, flame_knight_texture1.height)
            return flame_knight_texture2, source_rect

        else:
            source_rect = rl.Rectangle(
                0, 0, flame_knight_texture1.width, flame_knight_texture1.height)
            return flame_knight_texture2, source_rect

    elif rl.is_key_down(rl.KEY_A):
        player.facing_left = True
        source_rect = rl.Rectangle(
            0, 0, -flame_knight_texture1.width, flame_knight_texture1.height)
        return current_texture_fk, source_rect

    elif rl.is_key_down(rl.KEY_D):
        player.facing_left = False
        source_rect = rl.Rectangle(
            0, 0, flame_knight_texture1.width, flame_knight_texture1.height)
        return current_texture_fk, source_rect

    else:
        if player.facing_left:
            source_rect = rl.Rectangle(
                0, 0, -flame_knight_texture1.width, flame_knight_texture1.height)
            return flame_knight_texture1, source_rect

        else:
            source_rect = rl.Rectangle(
                0, 0, flame_knight_texture1.width, flame_knight_texture1.height)
            return flame_knight_texture1, source_rect


last_texture_swap_time_iw = time.time()
current_texture_iw = ice_wizard_texture1


def animate_ice_wizard(player, current_texture_iw):

    if rl.is_key_down(rl.KEY_UP):
        if player.facing_left:
            source_rect = rl.Rectangle(
                0, 0, -ice_wizard_texture1.width, ice_wizard_texture1.height)
            return ice_wizard_texture2, source_rect

        else:
            source_rect = rl.Rectangle(
                0, 0, ice_wizard_texture1.width, ice_wizard_texture1.height)
            return ice_wizard_texture2, source_rect

    elif rl.is_key_down(rl.KEY_LEFT):
        player.facing_left = True
        source_rect = rl.Rectangle(
            0, 0, -ice_wizard_texture1.width, ice_wizard_texture1.height)
        return current_texture_iw, source_rect

    elif rl.is_key_down(rl.KEY_RIGHT):
        player.facing_left = False
        source_rect = rl.Rectangle(
            0, 0, ice_wizard_texture1.width, ice_wizard_texture1.height)
        return current_texture_iw, source_rect

    else:
        if player.facing_left:
            source_rect = rl.Rectangle(
                0, 0, -ice_wizard_texture1.width, ice_wizard_texture1.height)
            return ice_wizard_texture1, source_rect

        else:
            source_rect = rl.Rectangle(
                0, 0, ice_wizard_texture1.width, ice_wizard_texture1.height)
            return ice_wizard_texture1, source_rect

# Character movement


def move_player(player, is_flame_knight):

    current_time = time.time()
    if is_flame_knight:
        global last_texture_swap_time_fk
        global current_texture_fk
        if current_time - last_texture_swap_time_fk >= 1 / animation_speed:
            last_texture_swap_time_fk = current_time
            if current_texture_fk == flame_knight_texture1:
                current_texture_fk = flame_knight_texture2
            else:
                current_texture_fk = flame_knight_texture1

        if rl.is_key_down(rl.KEY_A):
            player.position.x -= 3
            player.facing_left = True

        if rl.is_key_down(rl.KEY_D):
            player.position.x += 3
            player.facing_left = False

        if rl.is_key_down(rl.KEY_W) and player.can_jump and player.jump_timer >= 0.5:
            global flame_knight_sound_played
            rl.play_sound(flame_knight_jump_sound)

            player.speed.y = -5
            player.can_jump = False
            player.jump_timer = 0.0

        tex, rec = animate_flame_knight(player, current_texture_fk)
        rl.draw_texture_pro(
            tex,
            rec,
            flame_knight_rect,
            rl.Vector2(0, 0),
            0,
            WHITE
        )

    else:
        global last_texture_swap_time_iw
        global current_texture_iw
        if current_time - last_texture_swap_time_iw >= 1 / animation_speed:
            last_texture_swap_time_iw = current_time
            if current_texture_iw == ice_wizard_texture1:
                current_texture_iw = ice_wizard_texture2
            else:
                current_texture_iw = ice_wizard_texture1

        if rl.is_key_down(rl.KEY_LEFT):
            player.position.x -= 3
            player.facing_left = True
        if rl.is_key_down(rl.KEY_RIGHT):
            player.position.x += 3
            player.facing_left = False
        if rl.is_key_down(rl.KEY_UP) and player.can_jump and player.jump_timer >= 0.5:
            rl.play_sound(ice_wizard_jump_sound)
            player.speed.y = -5
            player.can_jump = False
            player.is_jumping = True
            player.jump_timer = 0.0

        tex, rec = animate_ice_wizard(player, current_texture_iw)
        rl.draw_texture_pro(
            tex,
            rec,
            ice_wizard_rect,
            rl.Vector2(0, 0),
            0,
            WHITE
        )

    player.position.y += player.speed.y


# Spawn positions
flame_knight_spawnx, flame_knight_spawny = 30, 510
ice_wizard_spawnx, ice_wizard_spawny = 30, 510

# Players setup
flame_knight = Player(rl.Vector2(flame_knight_spawnx,
                      flame_knight_spawny), rl.Vector2(25, 40), ORANGE)
ice_wizard = Player(rl.Vector2(ice_wizard_spawnx,
                    ice_wizard_spawny), rl.Vector2(25, 40), SKYBLUE)

# Load the JSON level file
with open('map/level2.json', 'r') as f:
    level_data = json.load(f)


# Tile size
tile_width = 25
tile_height = 25

# Create platforms
foreground_layer = level_data['layers'][1]
platforms = []
for y in range(foreground_layer['height']):
    for x in range(foreground_layer['width']):
        tile_id = foreground_layer['data'][y * foreground_layer['width'] + x]
        if tile_id != 0:  #
            # Non-zero value means a tile is present here
            platform_rect = rl.Rectangle(
                x * tile_width, y * tile_height, tile_width, tile_height)
            platform_color = DARKGRAY  # Default color for the platforms
            platforms.append(Platform(platform_rect, platform_color))

# Create Goals
flame_goal_layer = level_data['layers'][5]
for y in range(flame_goal_layer['height']):
    for x in range(flame_goal_layer['width']):
        tile_id = flame_goal_layer['data'][y * flame_goal_layer['width'] + x]
        if tile_id != 0:
            red_goal = rl.Rectangle(
                x * tile_width, y * tile_height, tile_width, tile_height)

ice_goal_layer = level_data['layers'][6]
for y in range(ice_goal_layer['height']):
    for x in range(ice_goal_layer['width']):
        tile_id = ice_goal_layer['data'][y * ice_goal_layer['width'] + x]
        if tile_id != 0:
            blue_goal = rl.Rectangle(
                x * tile_width, y * tile_height, tile_width, tile_height)

# Create Hazards
waters = []
water_layer = level_data['layers'][2]
for y in range(water_layer['height']):
    for x in range(water_layer['width']):
        tile_id = water_layer['data'][y * water_layer['width'] + x]
        if tile_id != 0:
            platform_rect = rl.Rectangle(
                x * tile_width, (y * tile_height) + (tile_height // 2) + 1, tile_width, tile_height // 2)
            platform_color = BLUE
            waters.append(Platform(platform_rect, platform_color))

lavas = []
lava_layer = level_data['layers'][3]
for y in range(lava_layer['height']):
    for x in range(lava_layer['width']):
        tile_id = lava_layer['data'][y * lava_layer['width'] + x]
        if tile_id != 0:
            platform_rect = rl.Rectangle(
                x * tile_width, (y * tile_height) + (tile_height // 2) + 1, tile_width, tile_height // 2)
            platform_color = ORANGE
            lavas.append(Platform(platform_rect, platform_color))

goos = []
goo_layer = level_data['layers'][4]
for y in range(goo_layer['height']):
    for x in range(goo_layer['width']):
        tile_id = goo_layer['data'][y * goo_layer['width'] + x]
        if tile_id != 0:
            platform_rect = rl.Rectangle(
                x * tile_width, (y * tile_height) + (tile_height // 2) + 1, tile_width, tile_height // 2)
            platform_color = GREEN
            goos.append(Platform(platform_rect, platform_color))

lever_layer = level_data['layers'][7]
for y in range(lever_layer['height']):
    for x in range(lever_layer['width']):
        tile_id = lever_layer['data'][y * lever_layer['width'] + x]
        if tile_id != 0:  # Non-zero value means a tile is present here
            lever1 = rl.Rectangle(x * tile_width, y *
                                  tile_height, tile_width, tile_height)


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
            elevator_rect = rl.Rectangle(
                x * tile_width, y * tile_height, width_count * tile_width, tile_height)
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
            elevator_rect = rl.Rectangle(
                x * tile_width, y * tile_height, width_count * tile_width, tile_height)
            elevator_color = BROWN
            # Create the elevator and append it to the list
            elevator2 = Elevator(elevator_rect, elevator_color, 50)

            x += width_count
        else:
            x += 1

elevator2_active = False  # Single boolean variable for the elevator

# Button 1
button_layer = level_data['layers'][9]
for y in range(button_layer['height']):
    for x in range(button_layer['width']):
        tile_id = button_layer['data'][y * lever_layer['width'] + x]
        if tile_id != 0:  # Non-zero value means a tile is present here
            button1 = rl.Rectangle(x * tile_width, y *
                                   tile_height, tile_width, tile_height)

# Lever 2
lever_layer = level_data['layers'][11]
for y in range(lever_layer['height']):
    for x in range(lever_layer['width']):
        tile_id = lever_layer['data'][y * lever_layer['width'] + x]
        if tile_id != 0:  # Non-zero value means a tile is present here
            lever2 = rl.Rectangle(x * tile_width, y *
                                  tile_height, tile_width, tile_height)

# Elevator 3
elevator_layer = level_data['layers'][12]  # Your elevator layer
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
            elevator_rect = rl.Rectangle(
                x * tile_width, y * tile_height, width_count * tile_width, tile_height)
            elevator_color = BROWN
            # Create the elevator and append it to the list
            elevator3 = Elevator(elevator_rect, elevator_color, 50)

            x += width_count
        else:
            x += 1

elevator3_active = False

# Button 2
button_layer = level_data['layers'][13]
for y in range(button_layer['height']):
    for x in range(button_layer['width']):
        tile_id = button_layer['data'][y * lever_layer['width'] + x]
        if tile_id != 0:  # Non-zero value means a tile is present here
            button2 = rl.Rectangle(x * tile_width, y *
                                   tile_height, tile_width, tile_height)

# Elevator 4
elevator_layer = level_data['layers'][14]  # Your elevator layer

for x in range(elevator_layer['width']):
    y = 0
    while y < elevator_layer['height']:
        tile_id = elevator_layer['data'][y * elevator_layer['width'] + x]
        if tile_id != 0:  # Non-zero tile means part of the elevator
            height_count = 1
            while (y + height_count < elevator_layer['height'] and
                   elevator_layer['data'][(y + height_count) * elevator_layer['width'] + x] != 0 and
                   height_count < 4):  # Adjust '4' for max vertical size
                height_count += 1

            # Create a single elevator platform rectangle
            elevator_rect = rl.Rectangle(
                x * tile_width, y * tile_height, tile_width, height_count * tile_height)
            elevator_color = BROWN
            # Create the elevator and append it to the list
            # Adjust '50' for vertical speed
            elevator4 = Elevator(elevator_rect, elevator_color, 50)

            y += height_count
        else:
            y += 1

elevator4_active = False


# Button 3
button_layer = level_data['layers'][15]
for y in range(button_layer['height']):
    for x in range(button_layer['width']):
        tile_id = button_layer['data'][y * lever_layer['width'] + x]
        if tile_id != 0:  # Non-zero value means a tile is present here
            button3 = rl.Rectangle(x * tile_width, y *
                                   tile_height, tile_width, tile_height)

# Elevator 5
elevator_layer = level_data['layers'][16]  # Your elevator layer
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
            elevator_rect = rl.Rectangle(
                x * tile_width, y * tile_height, width_count * tile_width, tile_height)
            elevator_color = BROWN
            # Create the elevator and append it to the list
            elevator5 = Elevator(elevator_rect, elevator_color, 50)

            x += width_count
        else:
            x += 1

elevator5_active = False

elevator_layer = level_data['layers'][17]  # Your elevator layer

for x in range(elevator_layer['width']):
    y = 0
    while y < elevator_layer['height']:
        tile_id = elevator_layer['data'][y * elevator_layer['width'] + x]
        if tile_id != 0:  # Non-zero tile means part of the elevator
            height_count = 1
            while (y + height_count < elevator_layer['height'] and
                   elevator_layer['data'][(y + height_count) * elevator_layer['width'] + x] != 0 and
                   height_count < 4):  # Adjust '4' for max vertical size
                height_count += 1

            # Create a single elevator platform rectangle
            elevator_rect = rl.Rectangle(
                x * tile_width, y * tile_height, tile_width, height_count * tile_height)
            elevator_color = BROWN
            # Create the elevator and append it to the list
            # Adjust '50' for vertical speed
            elevator6 = Elevator(elevator_rect, elevator_color, 50)

            y += height_count
        else:
            y += 1

elevator6_active = False


# Flags to check if players reached goal
flame_knight_reached_goal = False
ice_wizard_reached_goal = False

# Set target FPS
rl.set_target_fps(60)

# Game loop
while not rl.window_should_close():

    rl.update_music_stream(background_music)

    # Begin Drawing
    rl.begin_drawing()
    rl.clear_background(RAYWHITE)

    # Draw level texture
    rl.draw_texture(level2_texture, 0, 0, WHITE)

    # Update player rectangles for collision detection
    flame_knight_rect = rl.Rectangle(
        flame_knight.position.x, flame_knight.position.y, flame_knight.size.x, flame_knight.size.y)
    ice_wizard_rect = rl.Rectangle(
        ice_wizard.position.x, ice_wizard.position.y, ice_wizard.size.x, ice_wizard.size.y)

    # Draw elevator 1
    rl.draw_texture_pro(
        elevator_texture,
        rl.Rectangle(0, 0, elevator_texture.width, elevator_texture.height),
        elevator1.rect,
        rl.Vector2(0, 0),
        0,
        WHITE
    )

    # Draw elevator 2
    rl.draw_texture_pro(
        elevator_texture,
        rl.Rectangle(0, 0, elevator_texture.width, elevator_texture.height),
        elevator2.rect,
        rl.Vector2(0, 0),
        0,
        WHITE
    )

    # Draw elevator 3
    rl.draw_texture_pro(
        elevator_texture,
        rl.Rectangle(0, 0, elevator_texture.width, elevator_texture.height),
        elevator3.rect,
        rl.Vector2(0, 0),
        0,
        WHITE
    )

    # Draw elevator 4
    rl.draw_texture_pro(
        elevatorflipped_texture,
        rl.Rectangle(0, 0, elevatorflipped_texture.width,
                     elevatorflipped_texture.height),
        elevator4.rect,
        rl.Vector2(0, 0),
        0,
        WHITE
    )

    # Draw elevator 5
    rl.draw_texture_pro(
        elevator_texture,
        rl.Rectangle(0, 0, elevator_texture.width, elevator_texture.height),
        elevator5.rect,
        rl.Vector2(0, 0),
        0,
        WHITE
    )

    # Draw elevator 6
    rl.draw_texture_pro(
        elevatorflipped_texture,
        rl.Rectangle(0, 0, elevatorflipped_texture.width,
                     elevatorflipped_texture.height),
        elevator6.rect,
        rl.Vector2(0, 0),
        0,
        WHITE
    )

    # Draw button 1
    if rl.check_collision_recs(flame_knight_rect, button1) or rl.check_collision_recs(ice_wizard_rect, button1):

        rl.draw_texture_pro(
            button_on_texture,
            rl.Rectangle(0, 0, button_on_texture.width,
                         button_on_texture.height),
            button1,
            rl.Vector2(0, 0),
            0,
            WHITE
        )
    else:
        rl.draw_texture_pro(
            button_off_texture,
            rl.Rectangle(0, 0, button_off_texture.width,
                         button_off_texture.height),
            button1,
            rl.Vector2(0, 0),
            0,
            WHITE
        )

    # Draw button 2
    if rl.check_collision_recs(flame_knight_rect, button2) or rl.check_collision_recs(ice_wizard_rect, button2):
        rl.draw_texture_pro(
            button2_on_texture,
            rl.Rectangle(0, 0, button_on_texture.width,
                         button_on_texture.height),
            button2,
            rl.Vector2(0, 0),
            0,
            WHITE
        )
    else:
        rl.draw_texture_pro(
            button2_off_texture,
            rl.Rectangle(0, 0, button_off_texture.width,
                         button_off_texture.height),
            button2,
            rl.Vector2(0, 0),
            0,
            WHITE
        )

    # Draw button 3
    if rl.check_collision_recs(flame_knight_rect, button3) or rl.check_collision_recs(ice_wizard_rect, button3):
        rl.draw_texture_pro(
            button3_on_texture,
            rl.Rectangle(0, 0, button_on_texture.width,
                         button_on_texture.height),
            button3,
            rl.Vector2(0, 0),
            0,
            WHITE
        )
    else:
        rl.draw_texture_pro(
            button3_off_texture,
            rl.Rectangle(0, 0, button_off_texture.width,
                         button_off_texture.height),
            button3,
            rl.Vector2(0, 0),
            0,
            WHITE
        )

    # Draw lever 1
    if elevator1_active:
        rl.draw_texture_pro(
            lever_on_texture,
            rl.Rectangle(0, 0, lever_on_texture.width,
                         lever_on_texture.height),
            lever1,
            rl.Vector2(0, 0),
            0,
            WHITE
        )
    else:
        rl.draw_texture_pro(
            lever_off_texture,
            rl.Rectangle(0, 0, lever_off_texture.width,
                         lever_off_texture.height),
            lever1,
            rl.Vector2(0, 0),
            0,
            WHITE
        )

    # Draw lever 2
    if elevator4_active:
        rl.draw_texture_pro(
            lever_on_texture,
            rl.Rectangle(0, 0, lever_on_texture.width,
                         lever_on_texture.height),
            lever2,
            rl.Vector2(0, 0),
            0,
            WHITE
        )
    else:
        rl.draw_texture_pro(
            lever_off_texture,
            rl.Rectangle(0, 0, lever_off_texture.width,
                         lever_off_texture.height),
            lever2,
            rl.Vector2(0, 0),
            0,
            WHITE
        )

    enemy1.update(flame_knight, ice_wizard)
    enemy1.draw()

    enemy2.update(flame_knight, ice_wizard)
    enemy2.draw()

    # Draw and move players
    move_player(flame_knight, True)
    move_player(ice_wizard, False)

    # Update vertical movement (gravity effect)
    flame_knight.speed.y += 0.2
    ice_wizard.speed.y += 0.2

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
    flame_knight_reached_goal = rl.check_collision_recs(
        flame_knight_rect, red_goal)
    ice_wizard_reached_goal = rl.check_collision_recs(
        ice_wizard_rect, blue_goal)

    # Lever 1 Logic
    handle_lever1(flame_knight)
    handle_lever1(ice_wizard)

    # Elevator 1 logic
    update_elevator1(elevator1, elevator1_active)

    # Handle collision with the elevator
    handle_platform_collision(flame_knight, elevator1)
    handle_platform_collision(ice_wizard, elevator1)

    # Lever 2 logic
    handle_lever2(flame_knight)
    handle_lever2(ice_wizard)

    # Elevator 4 logic
    elevator4.range_y = 100
    update_elevator2(elevator4, elevator4_active)

    # Handle collision with the elevator
    handle_platform_collision(flame_knight, elevator4)
    handle_platform_collision(ice_wizard, elevator4)

    # Button 1 logic
    elevator2_active = False
    elevator3_active = False

    if handle_buttons(button1, flame_knight) or handle_buttons(button1, ice_wizard):
        if not button1_last_state:  # Check if the button was not pressed before
            if not interact_sound_played:  # Ensure the sound is played only once
                rl.play_sound(interact_sound)
                interact_sound_played = True
        elevator2_active = True  # Activate the elevator
        elevator3_active = True
        button1_last_state = True  # Update button press state
    else:
        button1_last_state = False  # Reset state when not pressing the button
        interact_sound_played = False  # Reset sound flag when button is released

    elevator2.range_y = 100
    elevator3.range_y = 100
    update_elevator2(elevator2, elevator2_active)

    # Handle collision with the elevator
    handle_platform_collision(flame_knight, elevator2)
    handle_platform_collision(ice_wizard, elevator2)

    update_elevator2(elevator3, elevator3_active)

    # Handle collision with the elevator
    handle_platform_collision(flame_knight, elevator3)
    handle_platform_collision(ice_wizard, elevator3)

    # Button 2 logic
    elevator5_active = False

    if handle_buttons(button2, flame_knight) or handle_buttons(button2, ice_wizard):
        if not button2_last_state:  # Check if the button was not pressed before
            if not interact_sound_played:  # Ensure the sound is played only once
                rl.play_sound(interact_sound)
                interact_sound_played = True
        elevator5_active = True  # Activate the elevator
        button2_last_state = True  # Update button press state
    else:
        button2_last_state = False  # Reset state when not pressing the button
        interact_sound_played = False  # Reset sound flag when button is released

    elevator5.range_y = 150
    update_elevator2(elevator5, elevator5_active)

    # Handle collision with the elevator
    handle_platform_collision(flame_knight, elevator5)
    handle_platform_collision(ice_wizard, elevator5)

    # Button 3 Logic
    elevator6_active = False

    if handle_buttons(button3, flame_knight) or handle_buttons(button3, ice_wizard):
        if not button3_last_state:  # Check if the button was not pressed before
            if not interact_sound_played:  # Ensure the sound is played only once
                rl.play_sound(interact_sound)
                interact_sound_played = True
        elevator6_active = True  # Activate the elevator
        button3_last_state = True  # Update button press state
    else:
        button3_last_state = False  # Reset state when not pressing the button
        interact_sound_played = False  # Reset sound flag when button is released

    update_elevator2(elevator6, elevator6_active)

    # Handle collision with the elevator
    handle_platform_collision(flame_knight, elevator6)
    handle_platform_collision(ice_wizard, elevator6)

    # Game over handling and popup
    if not show_over:

        for water in waters:
            if rl.check_collision_recs(flame_knight_rect, water.rect):
                print("Flame Knight touched water! Game Over!")
                show_over = True

            elif rl.check_collision_recs(ice_wizard_rect, water.rect):
                ice_wizard.can_jump = True

        for lava in lavas:
            if rl.check_collision_recs(ice_wizard_rect, lava.rect):
                print("Ice Wizard touched lava! Game Over!")
                show_over = True
            elif rl.check_collision_recs(flame_knight_rect, lava.rect):
                flame_knight.can_jump = True

        for goo in goos:
            if rl.check_collision_recs(flame_knight_rect, goo.rect) or \
                    rl.check_collision_recs(ice_wizard_rect, goo.rect):
                print("Player touched goo! Game Over!")
                show_over = True

    if show_over:
        if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(popup_button1_x, popup_button1_y, popup_button1_width,
                                                                popup_button1_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            print("Retry")

            enemy1 = Enemy(rl.Vector2(400, 300), rl.Vector2(
                30, 30), rl.Vector2(200, 60), rl.RED, 1)
            enemy2 = Enemy(rl.Vector2(450, 350), rl.Vector2(
                30, 30), rl.Vector2(200, 60), rl.RED, 1)
            # Reset elevators
            elevator1_active = False
            elevator2_active = False
            elevator3_active = False
            elevator4_active = False
            elevator5_active = False
            elevator6_active = False

            enemy1.active = False
            enemy2.active = False

            show_over = False
            flame_knight.position = rl.Vector2(
                flame_knight_spawnx, flame_knight_spawny)
            ice_wizard.position = rl.Vector2(
                ice_wizard_spawnx, ice_wizard_spawny)

        if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(popup_button2_x, popup_button2_y, popup_button2_width, popup_button2_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            print("Quit")
            rl.close_window()
            subprocess.run(["python", "main.py"])

        popup_rect = rl.Rectangle(popup_x, popup_y, popup_width, popup_height)

        rl.draw_texture_pro(
            gameover_texture,
            rl.Rectangle(0, 0, popup_width, popup_height),
            popup_rect,
            rl.Vector2(0, 0),
            0,
            WHITE
        )

    popup_x = screen_width // 2 - 150
    popup_y = screen_height // 2 - 100
    popup_width = 300
    popup_height = 300

    # Popup button positions and sizes
    popup_button1_x = popup_x + 80
    popup_button1_y = popup_y + 125
    popup_button1_width = 150
    popup_button1_height = 50

    popup_button2_x = popup_x + 80
    popup_button2_y = popup_y + 225
    popup_button2_width = 150
    popup_button2_height = 50

    # Pause Menu
    mouse_pos = rl.get_mouse_position()
    if not show_pause:
        if rl.is_key_down(rl.KEY_P):
            show_pause = True

    if show_pause:
        if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(popup_button1_x, popup_button1_y, popup_button1_width,
                                                                popup_button1_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            print("Retry")
            enemy1 = Enemy(rl.Vector2(400, 300), rl.Vector2(
                30, 30), rl.Vector2(200, 60), rl.RED, 1)
            enemy2 = Enemy(rl.Vector2(450, 350), rl.Vector2(
                30, 30), rl.Vector2(200, 60), rl.RED, 1)
            # Reset elevators
            elevator1_active = False
            elevator2_active = False
            elevator3_active = False
            elevator4_active = False
            elevator5_active = False
            elevator6_active = False

            enemy1.active = False
            enemy2.active = False
            show_pause = False
            rl.end_drawing()

        if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(popup_button2_x, popup_button2_y, popup_button2_width, popup_button2_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            print("Popup Button 2 clicked!")
            # Do something (e.g., start game as Ice Wizard)
            rl.close_window()
            subprocess.run(["python", "main.py"])

        popup_rect = rl.Rectangle(popup_x, popup_y, popup_width, popup_height)

        rl.draw_texture_pro(
            pause_texture,
            rl.Rectangle(0, 0, popup_width, popup_height),
            popup_rect,
            rl.Vector2(0, 0),
            0,
            WHITE
        )

    # Display level complete message
    if not show_complete:
        if flame_knight_reached_goal and ice_wizard_reached_goal:
            show_complete = True

    if show_complete:

        # Writing level data
        level_data = {
            "level1": True,
            "level2": True,
            "level3": False
        }

        write_levels(level_data)

        if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(popup_button1_x, popup_button1_y, popup_button1_width,
                                                                popup_button1_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            print("Next")

            show_complete = False
            rl.close_window()
            subprocess.run(["python", "level2.py"])

        if rl.check_collision_point_rec(mouse_pos, rl.Rectangle(popup_button2_x, popup_button2_y, popup_button2_width, popup_button2_height)) and rl.is_mouse_button_pressed(rl.MOUSE_BUTTON_LEFT):
            print("Quit")
            rl.close_window()
            subprocess.run(["python", "main.py"])

        popup_rect = rl.Rectangle(popup_x, popup_y, popup_width, popup_height)

        rl.draw_texture_pro(
            complete_texture,
            rl.Rectangle(0, 0, popup_width, popup_height),
            popup_rect,
            rl.Vector2(0, 0),
            0,
            WHITE
        )

    rl.end_drawing()

# Close window
rl.unload_music_stream(background_music)
rl.close_window()
