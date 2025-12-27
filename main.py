"""
This module is the entry point for the Tetris game application.
It initializes the game window, managers, and starts the pyglet event loop.
"""
import pyglet

from src.IOHandlers.InputHandlers.keyboard_input_handler import KeyboardInputHandler
from src.IOHandlers.OutputHandlers.audio_handler import audio_handler
from src.Utils.offset_provider import offsetProvider
from src.GameEngine.game_manager import GameManager


def main():
    """
    Main function to initialize and run the Tetris application.
    Sets up the window, game manager, input handling, and clock intervals.
    """
    # 1. Create window

    window = pyglet.window.Window(fullscreen=False, caption="Tetris", resizable=True)
    offsetProvider.inicialize(window)

    game_manager = GameManager()
    audio_handler.set_event_bus(game_manager.get_event_bus())
    input_handler = KeyboardInputHandler(game_manager)

    def update(dt):
        game_manager.update(dt)

    pyglet.clock.schedule_interval(update, 1/60)  # 60 updates/sec
    pyglet.clock.schedule_interval(input_handler.poll, 1 / 60)

    # 6. Hook the on_draw event
    @window.event
    def on_draw():
        window.clear()
        game_manager.draw()

    # 7. Hook the input events
    @window.event
    def on_key_press(symbol, modifiers):
        input_handler.on_key_press(symbol, modifiers)

    @window.event
    def on_key_release(symbol, modifiers):
        input_handler.on_key_release(symbol, modifiers)

    @window.event
    def on_text(text):
        input_handler.on_text(text)

    @window.event
    def on_text_motion(motion):
        input_handler.on_text_motion(motion)

        # 8. Run the app
    pyglet.app.run()


if __name__ == "__main__":
    main()
