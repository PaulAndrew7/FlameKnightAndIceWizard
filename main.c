#include "raylib.h"

#define MAX_PLATFORMS 10

typedef struct Player {
    Vector2 position;
    Vector2 size;
    Vector2 speed;
    Color color;
} Player;

typedef struct Platform {
    Rectangle rect;
    Color color;
} Platform;

void MovePlayer(Player *player, bool isFireboy);

bool CheckCollisionPlayerPlatform(Player *player, Platform *platform);

int main(void) {
    const int screenWidth = 800;
    const int screenHeight = 600;
    
    InitWindow(screenWidth, screenHeight, "Fireboy and Watergirl - Simple Version");

    // Define Fireboy
    Player fireboy = {{100, screenHeight - 50}, {40, 60}, {0, 0}, RED};

    // Define Watergirl
    Player watergirl = {{200, screenHeight - 50}, {40, 60}, {0, 0}, BLUE};

    // Platforms
    Platform platforms[MAX_PLATFORMS] = {
        {{0, screenHeight - 20, screenWidth, 20}, DARKGRAY}, // Ground
        {{150, 450, 200, 20}, DARKGRAY},
        {{400, 350, 200, 20}, DARKGRAY},
        {{650, 250, 100, 20}, DARKGRAY}
    };

    const int platformCount = 4;

    SetTargetFPS(60);

    while (!WindowShouldClose()) {
        // Move Fireboy and Watergirl
        MovePlayer(&fireboy, true);
        MovePlayer(&watergirl, false);

        // Gravity and collision with platforms for Fireboy
        fireboy.speed.y += 0.5; // Simple gravity
        for (int i = 0; i < platformCount; i++) {
            if (CheckCollisionPlayerPlatform(&fireboy, &platforms[i])) {
                fireboy.speed.y = 0;
                fireboy.position.y = platforms[i].rect.y - fireboy.size.y;
            }
        }

        // Gravity and collision with platforms for Watergirl
        watergirl.speed.y += 0.5; // Simple gravity
        for (int i = 0; i < platformCount; i++) {
            if (CheckCollisionPlayerPlatform(&watergirl, &platforms[i])) {
                watergirl.speed.y = 0;
                watergirl.position.y = platforms[i].rect.y - watergirl.size.y;
            }
        }

        // Draw
        BeginDrawing();
        ClearBackground(RAYWHITE);

        // Draw Platforms
        for (int i = 0; i < platformCount; i++) {
            DrawRectangleRec(platforms[i].rect, platforms[i].color);
        }

        // Draw Fireboy and Watergirl
        DrawRectangleV(fireboy.position, fireboy.size, fireboy.color);
        DrawRectangleV(watergirl.position, watergirl.size, watergirl.color);

        EndDrawing();
    }

    CloseWindow();

    return 0;
}

void MovePlayer(Player *player, bool isFireboy) {
    // Fireboy controls (WASD)
    if (isFireboy) {
        if (IsKeyDown(KEY_A)) player->position.x -= 4;
        if (IsKeyDown(KEY_D)) player->position.x += 4;
        if (IsKeyDown(KEY_W) && player->speed.y == 0) player->speed.y = -10;
    }
    // Watergirl controls (Arrow Keys)
    else {
        if (IsKeyDown(KEY_LEFT)) player->position.x -= 4;
        if (IsKeyDown(KEY_RIGHT)) player->position.x += 4;
        if (IsKeyDown(KEY_UP) && player->speed.y == 0) player->speed.y = -10;
    }

    // Update position based on speed
    player->position.y += player->speed.y;
}

bool CheckCollisionPlayerPlatform(Player *player, Platform *platform) {
    Rectangle playerRect = {player->position.x, player->position.y, player->size.x, player->size.y};
    return CheckCollisionRecs(playerRect, platform->rect);
}
