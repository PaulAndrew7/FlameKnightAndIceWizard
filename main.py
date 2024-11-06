import pyray as rl
from raylib.colors import *

MAX_PLATFORMS = 10

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


screen_width = 800
screen_height = 600
rl.init_window(screen_width, screen_height, "Flame Knight And Ice Wizard")

flame_knight = Player(rl.Vector2(100, 500), rl.Vector2(40, 60), ORANGE)
ice_wizard = Player(rl.Vector2(200, 500), rl.Vector2(40, 60), SKYBLUE)
platforms = [
Platform(rl.Rectangle(0, 580, 800, 20), DARKGRAY),
    Platform(rl.Rectangle(150, 450, 200, 20), DARKGRAY),
    Platform(rl.Rectangle(400, 350, 200, 20), DARKGRAY),
    Platform(rl.Rectangle(650, 250, 100, 20), DARKGRAY)
]
red_goal = rl.Rectangle(750, 100, 30, 80)
blue_goal = rl.Rectangle(720, 100, 30, 80)

flame_knight_reached_goal = False
ice_wizard_reached_goal = False

rl.set_target_fps(60)

while not rl.window_should_close():
    move_player(flame_knight, True)
    move_player(ice_wizard, False)

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

    for platform in platforms:
        rl.draw_rectangle_rec(platform.rect, platform.color)

    rl.draw_rectangle_rec(flame_knight_rect, flame_knight.color)
    rl.draw_rectangle_rec(ice_wizard_rect, ice_wizard.color)

    rl.draw_rectangle_rec(red_goal, RED)
    rl.draw_rectangle_rec(blue_goal, BLUE)

    if flame_knight_reached_goal and ice_wizard_reached_goal:
        rl.draw_text("Level Complete!", screen_width // 2 - 100, screen_height // 2, 20, GREEN)

    rl.end_drawing()

rl.close_window()


