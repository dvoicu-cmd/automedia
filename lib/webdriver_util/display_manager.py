from pyvirtualdisplay.display import Display
import Xlib.display
import atexit
import os


class DisplayManager:
    """
    Xvfb display wrapper class
    """

    def __init__(self, size=(1366, 768)):
        # Set up display.
        self.display = Display(visible=True, size=size, backend="xvfb", use_xauth=True)
        self.display.start()
        self.display_id = self.display.new_display_var

        # Register cleanup to stop display on program exit
        atexit.register(self.stop_display)

    def activate_display(self):
        if self.display.is_alive():  # Apply the display to the machine when the sub process is active.
            # Ight so basically, if this is imported on the top of this file, it breaks everything.
            # So just import it here.
            import pyautogui
            # Set display for object
            print("Setting display for driver.")
            os.environ["DISPLAY"] = self.display_id
            pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ['DISPLAY'])

    def stop_display(self):
        if self.display:
            print(f"Stopping Xvfb display: {self.display_id}")
            self.display.stop()
            self.display = None
