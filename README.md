# Breakout/Arkanoid Clone (Python & Pygame)

## ⚠️ IMPORTANT LEGAL NOTICE
**Please read first:** [DISCLAIMER.md](./DISCLAIMER.md)

This repository contains code I wrote while practicing Python programming.
It serves as a demonstration of my self-taught skills in software development.

## Project Overview

This is my custom clone of the game "Breakout", created using Python 3 and the Pygame library.

## What I Learned

- Object-Oriented Programming with modular class architecture
- Pygame game loop and event handling
- Keyboard and Mouse input processing
- File I/O (CSV) for high score persistence
- Loading Levels, Images and Sounds
- Calculating Physics for the Ball movement
- Collision detection algorithms
- Random number generation for gameplay mechanics
- CX-Freeze for executable packaging

<p>
  <img src="./assets/brkt_1.gif" width="40%" style="max-width: 520px; height: auto; margin-right: 20px;" />
  <img src="./assets/brkt_2.gif" width="40%" style="max-width: 520px; height: auto;" />
</p>

## How to Run

### Option 1: 📥 Download for Windows

A standalone Windows version has been created using **CX-Freeze**.
*Reference:* [CX-Freeze Documentation](https://cx-freeze.readthedocs.io)

**Windows Version v1.0.0:**
[🔽 Download breakout_win_v1.0.zip](https://github.com/pythonprojects2025/breakout/releases/download/v1.0.0/breakout_win_v1.0.zip)

**THIS IS A LEARNING PROJECT** Please read the [DISCLAIMER](./DISCLAIMER.md) first before using this software! 


### Option 2: Running from Source (Linux)

If you wish to run the code directly on Linux via Terminal, follow these steps:

#### Update your system packages
    sudo apt update
    sudo apt upgrade

#### Navigate to the project folder
    cd path/to/project

#### Create a virtual environment
    python3 -m venv venv

#### Activate the virtual environment
    source venv/bin/activate
    (On Windows, use venv\Scripts\activate)

#### Install dependencies
    pip install -r requirements.txt

#### Run the application
    python breakout.py


**For detailed documentation, including screenshots, please refer to the German documentation in the docs folder.**

<p>
  <img src="./assets/brkt_3.gif" width="40%" style="max-width: 520px; height: auto; margin-right: 20px;" />
  <img src="./assets/levelup.png" width="40%" style="max-width: 520px; height: auto;" />
</p>

<p>
  <img src="./assets/win_screen.png" width="40%" style="max-width: 520px; height: auto;margin-right: 20px;" />
  <img src="./assets/title_screen.png" width="40%" style="max-width: 520px; height: auto;" />
</p>















