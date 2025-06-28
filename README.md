# Flappy Bird

A customized version of Flappy Bird built with Pygame. This version includes a settings menu, adjustable gameplay modes, sound toggles, and persistent high score tracking. It's not a polished studio build, just a solid and fun personal take on a classic game.

## Features

* Playable yellow bird with animated visuals
* Menu with options:

  * Pipe Mode: "Consistent" or "Dynamic"
  * Sound FX toggle (score, collision)
  * Background music toggle
* Score tracking with persistent high score stored in `highscore.txt`
* Pipes can appear in different combinations (solo or paired)
* Clean side-scrolling background and ground effect

## File Structure

```
├── flappybird.py           # Main game file
├── highscore.txt           # Stores high score (auto-created if missing)
├── assets/
│   ├── background-day.png
│   ├── base.png
│   ├── yellowbird-midflap.png
│   └── pipe-green.png
├── sounds/
│   ├── background.mp3
│   ├── point.wav
│   └── hit.wav
├── README.md               # You're reading it
```

## Requirements

* Python 3.x
* Pygame

Install dependencies:

```bash
pip install pygame
```

## Running the Game

```bash
python flappybird.py
```

Start at the menu, adjust settings if needed, and hit play.

## Notes

* `highscore.txt` is automatically updated whenever you beat your previous high score.
* The settings you choose are applied on your next game run.

## Reason for This Build

This wasn’t just about cloning Flappy Bird. This project was built as part of the AI-201L Lab course, where the goal was to create something modular and customizable. I focused on making a version that was both playable and tweakable. Something that served a real academic purpose while still being fun to experiment with. It is a practical build more than a polished product, but it reflects a solid grasp of both Python and Pygame fundamentals.

## License

Do what you want with it. Just don’t pretend you built it from scratch without giving a nod.
