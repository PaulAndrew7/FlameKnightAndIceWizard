::@echo off
:: > Setup required Environment
:: -------------------------------------
set COMPILER_DIR=C:\raylib\w64devkit\bin
set PATH=%PATH%;%COMPILER_DIR%
cd %~dp0
:: .
:: > Compile simple .rc file
:: ----------------------------
cmd /c windres ..\..\src\flameknightandicewizard.rc -o ..\..\src\flameknightandicewizard.rc.data
:: .
:: > Generating project
:: --------------------------
cmd /c mingw32-make -f ..\..\src\Makefile ^
PROJECT_NAME=flameknightandicewizard ^
PROJECT_VERSION=1.0 ^
PROJECT_DESCRIPTION="A 2-D co-op platformer game made using Raylib and C" ^
PROJECT_INTERNAL_NAME=flameknightandicewizard ^
PROJECT_PLATFORM=PLATFORM_DESKTOP ^
PROJECT_SOURCE_FILES="flameknightandicewizard.c" ^
BUILD_MODE="RELEASE" ^
BUILD_WEB_ASYNCIFY=FALSE ^
BUILD_WEB_MIN_SHELL=TRUE ^
BUILD_WEB_HEAP_SIZE=268435456 ^
RAYLIB_MODULE_AUDIO=TRUE ^
RAYLIB_MODULE_MODELS=TRUE
