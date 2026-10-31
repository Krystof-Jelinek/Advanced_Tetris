# Tetris with Abilities

A Tetris implementation written in Python using Pyglet. This project includes classic gameplay mechanics enhanced with a unique ability system and LAN multiplayer support.

## Features

*   **Classic Tetris Gameplay**: Standard block-stacking action with increasing difficulty.
*   **Ability System**: Use special abilities like "Bomb", "Slow Time", and "Speed Up" to gain an advantage.
*   **LAN Multiplayer**: Connect with friends over a local network (Client-Server architecture).
*   **Controller Support**: Play with a game controller (e.g. PS5 DualSense) using the D-pad or the left stick, alongside the keyboard.
*   **Audio**: Integrated sound effects for game events.
*   **Configuration**: somewhat customizable visual settings via `config.json`.

## Prerequisites

*   **Python 3.11+**
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

[Download .exe file](https://github.com/Krystof-Jelinek/Advanced_Tetris/releases/latest/download/Tetris.exe)

## Controls

The game can be played with a keyboard or a game controller (tested with a PS5 DualSense). Both can be used at the same time.

| Action                     | Keyboard        | Controller                              |
|:---------------------------|:----------------|:----------------------------------------|
| Move Piece Left            | **Left Arrow**  | **D-pad Left** / **Left Stick Left**    |
| Move Piece Right           | **Right Arrow** | **D-pad Right** / **Left Stick Right**  |
| Soft Drop (Move Down)      | **Down Arrow**  | **D-pad Down** / **Left Stick Down**    |
| Rotate Piece               | **Up Arrow**    | **D-pad Up** / **Left Stick Up** / **Triangle** |
| Hold/Swap Piece            | **C**           | **Circle**                              |
| Select Menu Option         | **Enter**       | **Cross**                               |
| Reset Game (after it ends) | **R**           | **Options**                             |
| Use Ability 1              | **Q**           | **L1**                                  |
| Use Ability 2              | **E**           | **R1**                                  |

Holding a direction repeats the move after a short delay, on the keyboard and on the controller alike.

If the game does not react to the controller, close Steam (Steam Input can take over the controller) and check that Pyglet detects it:

```bash
python -c "import pyglet; print(pyglet.input.get_controllers())"
```

## Running Tests

This project uses `pytest` for unit testing. To run the full test suite, execute the following command in the root directory:

```bash
pytest
```

## Quality Control & Pylint Decisions

The project maintains a **10.00/10** score, but the Pylint configuration (in `pyproject.toml`) has been customized to filter out warnings that are counterproductive (in my opinion) for this specific game architecture. Below are the justifications for these changes:

* **Cyclic Imports (`cyclic-import`)**: The State Machine pattern used here requires a circular relationship between the `GameManager` and individual `GameState` objects. This is a conscious architectural trade-off to ensure a clean separation between menu logic and gameplay.
* **Code Duplication (`duplicate-code`)**: Disabled primarily for the **Renderers**. Visual consistency across different UI elements and game objects often requires repetitive rendering logic that is necessary for the game to look uniform, and forcing abstraction here would only overcomplicate the drawing code.
* **Increased Class Attributes (`max-attributes=12`)**: The limit was raised to 12 to accommodate complex game entities (like the Tetris board or PlayState) that naturally track multiple game components, coordinates, and ability-specific data in one place.
* **Reduced Public Methods (`min-public-methods=1`)**: Lowered the threshold from 2 to 1. This adjustment supports the **Command pattern** and specific **Ability handlers** used in the game engine. Many of these classes are designed to be small and focused, performing only a single action (e.g., executing a command or triggering a specific effect). Forcing a second public method would result in unnecessary boilerplate code just to satisfy a default linter setting.
* **Longer Lines (`max-line-length=160`)**: Raised from the default 100. The deep package structure produces long import paths (e.g. `src.GameEngine.GameStates.PlayStates.AbiliteWrapperStates...`) and descriptive docstrings, and wrapping them would make the code harder to read rather than easier.
* **PascalCase Package Names (`module-rgx`)**: Packages (folders) are named in PascalCase (e.g. `GameEngine`, `TetrisPieces`) so they are easy to tell apart from the snake_case modules inside them. The naming rule was extended to accept both styles instead of renaming the whole package tree.

To verify the code quality, run:
```bash
python -m pylint .
```
