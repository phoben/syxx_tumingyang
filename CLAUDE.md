# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

"时光列车：驶向强国梦" (Time Train: Journey to a Strong Nation) is an educational interactive game built with Python and Pygame. It teaches Chinese revolutionary history through four historical periods: CCP founding (1921), PRC founding (1949), economic reform (1978+), and space exploration achievements (2003+).

## Commands

```bash
# Run the game
python main.py

# Generate TTS audio (requires MiniMax API key in .env)
python minimax-output/batch_tts_correct.py

# Generate background music
python minimax-output/generate_bgm.py
```

## Dependencies

- Python 3
- pygame (required for game runtime)
- requests (for TTS/BGM generation scripts)

## Architecture

### Scene-Based Structure

The game uses a scene-based architecture with inheritance:

- `BaseScene` (`scenes/base_scene.py`) - Abstract base class with common functionality
- Scene lifecycle: `on_enter()`, `on_exit()`, `draw()`, `update()`
- Each scene manages its own chapters, background images, and guide character states

Scene classes inherit from `BaseScene`:
- `MainScene` - Main menu with navigation buttons
- `RedboatScene` - Red Boat scene (1921 CCP founding) → "awakening" badge
- `FoundingScene` - Founding scene (1949 PRC founding) → "founding" badge
- `ReformScene` - Reform scene (1978+ economic reform) → "takeoff" badge
- `SpaceScene` - Space scene (2003+ space achievements) → "space" badge
- `EndingScene` - Celebration when all badges collected

### State Management

`GameState` (`state.py`) is a global singleton tracking:
- Current scene
- Badge collection status (awakening, founding, takeoff, space)
- Game completion status

### Audio Manager

`AudioManager` (`audio_manager.py`) handles:
- Background music with fade in/out
- Speech playback with BGM volume ducking (0.5 → 0.2 during speech)
- Sound effects and mute toggle

### Chapter System

Each historical scene has 4 chapters with:
- Title, text content
- Speech audio file (H01-H04, K01-K04, G01-G04, Y01-Y04)
- Background image file

Chapter navigation uses prev/next buttons in the narrative bubble UI.

### Guide Character States

The "Red Scarf Guide" character has three states:
- `stand` - Default standing pose
- `point` - Pointing pose (during narration)
- `celebrate` - Celebration pose (when badge earned)

Guide images are in `assets/images/characters/`.

### UI Components

Located in `ui/`:
- `Button` - Navigation buttons with hover/click animations
- `Badge` - Achievement badges with lit/dim states
- `NarrativeBubble` - Dialog box showing chapter text
- `BackButton` - Return to main menu
- `SoundToggle` - Mute/unmute button

### Asset Paths

- Images: `assets/images/` (backgrounds/, badges/, buttons/, characters/)
- Audio: `assets/audio/` (bgm/, speech/, sfx/)
- Narration segments: `minimax-output/segments.json`

## Key Configuration

Screen: 1280x720, 60 FPS, Debug mode enabled
Fonts: Windows system fonts (msyh.ttc, simhei.ttf)

## Content Generation

The `minimax-output/` directory contains scripts for generating game assets via MiniMax API:
- TTS generation for narration speech
- BGM generation for background music
- Image generation prompts