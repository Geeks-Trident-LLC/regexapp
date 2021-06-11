"""Module containing the logic for the Regex application."""

import tkinter as tk
# from tkinter import ttk
# from tkinter import filedialog
# from tkinter import messagebox
# from os import path
# from pprint import pformat
# import webbrowser
# from textwrap import dedent


__version__ = '0.0.1'
version = __version__

__edition__ = 'Community Edition'
edition = __edition__


class Application:
    def __init__(self):
        self._base_title = 'Regex GUI'
        self.root = tk.Tk()
        self.root.geometry('800x600+100+100')
        self.root.minsize(200, 200)
        self.root.option_add('*tearOff', False)

    def run(self):
        """Launch Regex GUI."""
        self.root.mainloop()


def execute():
    """Launch Regex GUI."""
    app = Application()
    app.run()
