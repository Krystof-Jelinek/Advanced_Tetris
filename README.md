# Tetris with Abilities

A Tetris implementation written in Python using Pyglet. This project includes classic gameplay mechanics enhanced with a unique ability system and LAN multiplayer support.

## Features

*   **Classic Tetris Gameplay**: Standard block-stacking action with increasing difficulty.
*   **Ability System**: Use special abilities like "Bomb", "Slow Time", and "Speed Up" to gain an advantage.
*   **LAN Multiplayer**: Connect with friends over a local network (Client-Server architecture).
*   **Audio**: Integrated sound effects for game events.
*   **Configuration**: somewhat customizable visual settings via `config.json`.

## Prerequisites

*   **Python 3.10+**
*   **Pyglet**: A cross-platform windowing and multimedia library for Python.

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd Jelinkry
    ```

2.  (Optional) Create and activate a virtual environment:
    ```bash
    python -m venv venv
    # Linux/Mac:
    source venv/bin/activate
    # Windows:
    .\venv\Scripts\activate
    ```

3.  Install the required dependencies:
    ```bash
    pip install pyglet
    ```

## Usage

To start the game, run the `main.py` script from the project root:

```bash
python main.py
```

#### Windows Standalone Version
If you are on Windows and prefer to run the game without installing Python or any dependencies, you can download the pre-compiled standalone executable here:

[Download .exe file](https://drive.google.com/file/d/1cmamcII9EuKU86f3oFSCVhNXQnwwAKa9/view)

## Controls

| Key                     | Action                |
|:------------------------|:----------------------|
| **Left Arrow**          | Move Piece Left       |
| **Right Arrow**         | Move Piece Right      |
| **Down Arrow**          | Soft Drop (Move Down) |
| **Up Arrow**            | Rotate Piece          |
| **C**                   | Hold/Swap Piece       |
| **Enter**               | Select Menu Option    |
| **R (after game ends)** | Reset Game            |
| **Q**                   | Use Ability 1         |
| **E**                   | Use Ability 2         |

## Running Tests

This project uses `pytest` for unit testing. To run the full test suite, execute the following command in the root directory:

```bash
pytest
```

## Quality Control & Pylint Decisions

The project maintains a **10.00/10** score, but the Pylint configuration has been customized to filter out warnings that are counterproductive (in my opinion) for this specific game architecture. Below are the justifications for these changes:

* **Cyclic Imports (`cyclic-import`)**: The State Machine pattern used here requires a circular relationship between the `GameManager` and individual `GameState` objects. This is a conscious architectural trade-off to ensure a clean separation between menu logic and gameplay.
* **Code Duplication (`duplicate-code`)**: Disabled primarily for the **Renderers**. Visual consistency across different UI elements and game objects often requires repetitive rendering logic that is necessary for the game to look uniform, and forcing abstraction here would only overcomplicate the drawing code.
* **Increased Class Attributes (`max-attributes=12`)**: The limit was raised to 12 to accommodate complex game entities (like the Tetris board or PlayState) that naturally track multiple game components, coordinates, and ability-specific data in one place.
* **Reduced Public Methods (`min-public-methods=1`)**: Lowered the threshold from 2 to 1. This adjustment supports the **Command pattern** and specific **Ability handlers** used in the game engine. Many of these classes are designed to be small and focused, performing only a single action (e.g., executing a command or triggering a specific effect). Forcing a second public method would result in unnecessary boilerplate code just to satisfy a default linter setting.

To verify the code quality, run:
```bash
pylint .