@echo off
title SkillConnect Platform - Quick Start

echo.
echo =====================================================
echo   SkillConnect Platform - Quick Start
echo =====================================================
echo.

echo [1] Run Setup Checker
echo [2] Install Dependencies  
echo [3] Start Application
echo [4] Open in Browser
echo [5] View Setup Guide
echo [6] Exit
echo.

set /p choice="Choose an option (1-6): "

if "%choice%"=="1" (
    echo.
    echo Running setup checker...
    powershell -ExecutionPolicy Bypass -File setup.ps1
    pause
    goto menu
)

if "%choice%"=="2" (
    echo.
    echo Installing dependencies...
    uv sync
    echo.
    echo Dependencies installed!
    pause
    goto menu
)

if "%choice%"=="3" (
    echo.
    echo Starting SkillConnect Platform...
    echo Press Ctrl+C to stop the server
    echo.
    uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
    pause
    goto menu
)

if "%choice%"=="4" (
    echo.
    echo Opening SkillConnect in your default browser...
    start http://localhost:8000
    goto menu
)

if "%choice%"=="5" (
    echo.
    echo Opening setup guide...
    start SETUP_GUIDE.md
    goto menu
)

if "%choice%"=="6" (
    echo.
    echo Thanks for using SkillConnect!
    exit
)

echo Invalid choice. Please try again.
pause

:menu
cls
goto start

:start
goto menu