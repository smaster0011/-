# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

from .single_instance import is_another_instance_running
from .version import APP_NAME
from .window import SubtitleMasker


def show_already_running_message():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(APP_NAME, f"{APP_NAME} 已经在运行。", parent=root)
    root.destroy()


def run_app():
    if is_another_instance_running():
        show_already_running_message()
        return

    app = SubtitleMasker()
    app.run()
