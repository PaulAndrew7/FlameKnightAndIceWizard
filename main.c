#include "raylib.h"

#define MAX_PLATFORMS 10

typedef struct Player {
    Vector2 position;
    Vector2 size;
    Vector2 speed;
    Color color;
    bool canJump;
    float jumpTimer;
} Player;

typedef struct Platform {
    Rectangle rect;
    Color color;
} Platform;

void MovePlayer(Player *player, bool isFlameKnight);
void HandlePlatformCollision(Player *player, Platform *platform);

int main(void) {
    const int screenWidth = 800;
    const int screenHeight = 600;

    InitWindow(screenWidth, screenHeight, "Flame Knight And Ice Wizard");

    Player flameKnight = {{100, 500}, {40, 60}, {0, 0}, ORANGE, true, 0.0f};
    Player iceWizard = {{200, 500}, {40, 60}, {0, 0}, SKYBLUE, true, 0.0f};

    Platform platforms[MAX_PLATFORMS] = {
        {{0, 580, 800, 20}, DARKGRAY},
        {{150, 450, 200, 20}, DARKGRAY},
        {{400, 350, 200, 20}, DARKGRAY},
        {{650, 250, 100, 20}, DARKGRAY}
    };
    const int platformCount = 4;

    // Define goals
    Rectangle redGoal = {750, 100, 30, 80};   // Goal for Flame Knight
    Rectangle blueGoal = {720, 100, 30, 80};  // Goal for Ice Wizard

    bool flameKnightReachedGoal = false;
    bool iceWizardReachedGoal = false;

    // Create player rectangles for reuse
    Rectangle flameKnightRect = {flameKnight.position.x, flameKnight.position.y, flameKnight.size.x, flameKnight.size.y};
    Rectangle iceWizardRect = {iceWizard.position.x, iceWizard.position.y, iceWizard.size.x, iceWizard.size.y};

    SetTargetFPS(60);

    while (!WindowShouldClose()) {
        // Update player positions and handle movement
        MovePlayer(&flameKnight, true);
        MovePlayer(&iceWizard, false);

        flameKnight.speed.y += 0.5; // Gravity
        iceWizard.speed.y += 0.5;

        // Update player rectangles based on current positions
        flameKnightRect.x = flameKnight.position.x;
        flameKnightRect.y = flameKnight.position.y;
        iceWizardRect.x = iceWizard.position.x;
        iceWizardRect.y = iceWizard.position.y;

        // Handle platform collisions
        for (int i = 0; i < platformCount; i++) {
            HandlePlatformCollision(&flameKnight, &platforms[i]);
            HandlePlatformCollision(&iceWizard, &platforms[i]);
        }

        // Keep characters within screen bounds
        if (flameKnight.position.x < 0) flameKnight.position.x = 0;
        if (flameKnight.position.x > screenWidth - flameKnight.size.x) flameKnight.position.x = screenWidth - flameKnight.size.x;
        if (iceWizard.position.x < 0) iceWizard.position.x = 0;
        if (iceWizard.position.x > screenWidth - iceWizard.size.x) iceWizard.position.x = screenWidth - iceWizard.size.x;

        flameKnight.jumpTimer += GetFrameTime();
        iceWizard.jumpTimer += GetFrameTime();

        // Check if players reached their goals using updated rectangles
        flameKnightReachedGoal = CheckCollisionRecs(flameKnightRect, redGoal);
        iceWizardReachedGoal = CheckCollisionRecs(iceWizardRect, blueGoal);

        BeginDrawing();
        ClearBackground(RAYWHITE);

        // Draw platforms
        for (int i = 0; i < platformCount; i++) {
            DrawRectangleRec(platforms[i].rect, platforms[i].color);
        }

        // Draw players using their rectangles
        DrawRectangleRec(flameKnightRect, flameKnight.color);
        DrawRectangleRec(iceWizardRect, iceWizard.color);

        // Draw goals
        DrawRectangleRec(redGoal, RED);
        DrawRectangleRec(blueGoal, BLUE);

        // Game over condition
        if (flameKnightReachedGoal && iceWizardReachedGoal) {
            DrawText("Level Complete!", screenWidth / 2 - 100, screenHeight / 2, 20, GREEN);
        }

        EndDrawing();
    }

    CloseWindow();
    return 0;
}

void MovePlayer(Player *player, bool isFlameKnight) {
    if (isFlameKnight) {
        if (IsKeyDown(KEY_A)) player->position.x -= 4;
        if (IsKeyDown(KEY_D)) player->position.x += 4;
        if (IsKeyDown(KEY_W) && player->canJump && player->jumpTimer >= 0.5f) {
            player->speed.y = -10;
            player->canJump = false;
            player->jumpTimer = 0.0f;
        }
    } else {
        if (IsKeyDown(KEY_LEFT)) player->position.x -= 4;
        if (IsKeyDown(KEY_RIGHT)) player->position.x += 4;
        if (IsKeyDown(KEY_UP) && player->canJump && player->jumpTimer >= 0.5f) {
            player->speed.y = -10;
            player->canJump = false;
            player->jumpTimer = 0.0f;
        }
    }
    player->position.y += player->speed.y;
}

void HandlePlatformCollision(Player *player, Platform *platform) {
    Rectangle playerRect = {player->position.x, player->position.y, player->size.x, player->size.y};

    if (CheckCollisionRecs(playerRect, platform->rect)) {
        // Calculate the depth of overlap on each side
        float overlapTop = player->position.y + player->size.y - platform->rect.y;
        float overlapBottom = platform->rect.y + platform->rect.height - player->position.y;
        float overlapLeft = player->position.x + player->size.x - platform->rect.x;
        float overlapRight = platform->rect.x + platform->rect.width - player->position.x;

        // Resolve collision by moving player out of platform in the smallest overlap direction
        if (overlapTop < overlapBottom && overlapTop < overlapLeft && overlapTop < overlapRight) {
            // Top collision (player hits the top of the platform)
            player->position.y = platform->rect.y - player->size.y;
            player->speed.y = 0;
            player->canJump = true;
        } 
        else if (overlapBottom < overlapTop && overlapBottom < overlapLeft && overlapBottom < overlapRight) {
            // Bottom collision (player hits the bottom of the platform)
            player->position.y = platform->rect.y + platform->rect.height;
            player->speed.y = 0;
        } 
        else if (overlapLeft < overlapRight) {
            // Left collision (player hits the left side of the platform)
            player->position.x = platform->rect.x - player->size.x;
            player->speed.x = 0;
        } 
        else {
            // Right collision (player hits the right side of the platform)
            player->position.x = platform->rect.x + platform->rect.width;
            player->speed.x = 0;
        }
    }
}