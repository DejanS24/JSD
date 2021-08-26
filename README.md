# pygame_sl
Project for faculty subject JSD

pygame_sl is a Domain-Specific Language (DSL) for generating 2D platform games in python using pygame library.
It is meant to enable anyone to design their own 2D platform game.

The pygame_sl is meant to be easy to understand and use, to design the player avater, levels and rules of the 2D platform game.

# Installation:
- Requirements for installing: `textX` and `jinja2`
- `pip install -e .` to install the project in development mode

# Usage:
- `textx generate <path_to_.pg_file> --target python [--output-path <path>]`
- Requirements to run generated python file: `pygame`
- `python <path_to_generated_.py_file>`

# Features:
- Modify player avatar and dimensions
- Add additional images for player avatar to enable animations
- Define pickup items (point or speed boost)
- Define levels with image or color backgrounds
- Add platforms to levels (define textures and dimensions) and defined items on specified coordinates
- Define sounds to be played during game or on specific actions (jump, items pickup, game end)
- Define custom settings for the game in general: custom title, fps, default move speed, screen size, default colors and font name

# Example of a .pg file:
```
game "2D Platformer"

player {
    color blue
    height 75
    width 50
}

level Level1 {
    background color yellow
    platform {
        position 300 420
        height 50
        width 80
    }
}

level Level2 {
    background color yellow
    platform {
        position 300 420
        height 50
        width 80
    }
}
```