# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox

from .config import (
    BOTTOM_OFFSET,
    CONFIG_PATH,
    DEFAULT_ALPHA,
    DEFAULT_HEIGHT,
    DEFAULT_LOCKED,
    DEFAULT_SHOW_TIP,
    DEFAULT_WIDTH,
    MIN_HEIGHT,
    MIN_WIDTH,
    config_bool,
    config_float,
    config_int,
    config_position,
    is_geometry_on_screen,
    load_config,
    save_config,
)
from .version import APP_NAME, APP_VERSION


class SubtitleMasker:
    DEFAULT_WIDTH = DEFAULT_WIDTH
    DEFAULT_HEIGHT = DEFAULT_HEIGHT
    DEFAULT_ALPHA = DEFAULT_ALPHA
    DEFAULT_SHOW_TIP = DEFAULT_SHOW_TIP
    DEFAULT_LOCKED = DEFAULT_LOCKED
    MIN_WIDTH = MIN_WIDTH
    MIN_HEIGHT = MIN_HEIGHT
    BOTTOM_OFFSET = BOTTOM_OFFSET
    GRIP_SIZE = 24
    HOVER_LEAVE_DELAY = 80
    CONFIG_PATH = CONFIG_PATH

    def __init__(self):
        self.config = load_config()

        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.configure(bg="black")

        self.width = config_int(self.config, "width", self.DEFAULT_WIDTH, self.MIN_WIDTH)
        self.height = config_int(self.config, "height", self.DEFAULT_HEIGHT, self.MIN_HEIGHT)
        self.alpha = config_float(self.config, "alpha", self.DEFAULT_ALPHA, 0.2, 1.0)
        self.show_tip = config_bool(self.config, "show_tip", self.DEFAULT_SHOW_TIP)
        self.locked = config_bool(self.config, "locked", self.DEFAULT_LOCKED)
        self.hovering = False
        self._leave_after_id = None

        self._drag_offset_x = 0
        self._drag_offset_y = 0
        self._resize_start_x = 0
        self._resize_start_y = 0
        self._resize_start_width = self.width
        self._resize_start_height = self.height

        self.tip_label = tk.Label(
            self.root,
            text="拖动移动｜右下角缩放｜右键退出｜Esc退出",
            fg="#eeeeee",
            bg="black",
            font=("Microsoft YaHei UI", 12),
        )

        self.resize_grip = tk.Canvas(
            self.root,
            width=self.GRIP_SIZE,
            height=self.GRIP_SIZE,
            bg="black",
            highlightthickness=0,
            cursor="sizing",
        )
        self._draw_resize_grip()

        self.menu = tk.Menu(self.root, tearoff=False)

        self._bind_events()
        self._apply_alpha(self.alpha)
        self._apply_hover_visibility()
        self._restore_or_center_window()

        self.root.after(100, self._activate_window)

    def _save_config(self):
        """Persist the current window state on normal exit."""
        self.root.update_idletasks()
        save_config(
            {
                "x": self.root.winfo_x(),
                "y": self.root.winfo_y(),
                "width": max(self.MIN_WIDTH, self.root.winfo_width()),
                "height": max(self.MIN_HEIGHT, self.root.winfo_height()),
                "alpha": self.alpha,
                "show_tip": self.show_tip,
                "locked": self.locked,
            }
        )

    def _build_context_menu(self):
        self.menu.delete(0, "end")
        opacity_options = (
            ("透明度 100%", 1.0),
            ("透明度 90%", 0.9),
            ("透明度 75%", 0.75),
            ("透明度 60%", 0.6),
            ("透明度 45%", 0.45),
        )
        for label, alpha in opacity_options:
            self.menu.add_command(label=label, command=lambda value=alpha: self._apply_alpha(value))

        self.menu.add_separator()
        self.menu.add_command(label="解锁" if self.locked else "锁定", command=self.toggle_lock)
        self.menu.add_command(label="重置到底部居中", command=self.reset_to_bottom_center)
        self.menu.add_command(label="恢复默认设置", command=self.restore_defaults)
        self.menu.add_separator()
        self.menu.add_command(label="使用说明", command=self.show_help)
        self.menu.add_command(label="关于软件", command=self.show_about)
        self.menu.add_separator()
        self.menu.add_command(label="退出", command=self.exit_app)

    def _bind_events(self):
        """Bind mouse actions, hover reactions, and the local shortcuts."""
        for widget in (self.root, self.tip_label, self.resize_grip):
            widget.bind("<Enter>", self._on_hover_enter)
            widget.bind("<Leave>", self._on_hover_leave)
            widget.bind("<Button-3>", self._show_context_menu)

        for widget in (self.root, self.tip_label):
            widget.bind("<ButtonPress-1>", self._start_move)
            widget.bind("<B1-Motion>", self._move_window)

        self.resize_grip.bind("<ButtonPress-1>", self._start_resize)
        self.resize_grip.bind("<B1-Motion>", self._resize_window)

        self.root.bind_all("<Escape>", lambda _event: self.exit_app())
        self.root.bind_all("<Control-h>", lambda _event: self.toggle_tip())
        self.root.bind_all("<Control-H>", lambda _event: self.toggle_tip())
        self.root.bind_all("<Control-r>", lambda _event: self.reset_to_bottom_center())
        self.root.bind_all("<Control-R>", lambda _event: self.reset_to_bottom_center())
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def _restore_or_center_window(self):
        position = config_position(self.config)
        if position:
            x, y = position
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            if is_geometry_on_screen(x, y, self.width, self.height, screen_width, screen_height):
                self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
                return

        self.reset_to_bottom_center()

    def _apply_alpha(self, alpha):
        self.alpha = max(0.2, min(1.0, float(alpha)))
        self.root.attributes("-alpha", self.alpha)

    def _apply_hover_visibility(self):
        """Hover state controls the temporary tip and resize handle display."""
        if self.hovering:
            self.tip_label.pack(fill="both", expand=True)
        else:
            self.tip_label.pack_forget()

        if self.hovering and not self.locked:
            self.resize_grip.place(relx=1.0, rely=1.0, anchor="se")
            # Canvas overrides lift/tkraise, so call Tk directly for widget stacking.
            self.root.tk.call("raise", self.resize_grip._w)
        else:
            self.resize_grip.place_forget()

    def _activate_window(self):
        self.root.lift()
        self.root.focus_force()

    def _draw_resize_grip(self):
        self.resize_grip.delete("all")
        for offset in (7, 12, 17):
            self.resize_grip.create_line(
                self.GRIP_SIZE - offset,
                self.GRIP_SIZE - 2,
                self.GRIP_SIZE - 2,
                self.GRIP_SIZE - offset,
                fill="#777777",
            )

    def _on_hover_enter(self, _event=None):
        if self._leave_after_id is not None:
            self.root.after_cancel(self._leave_after_id)
            self._leave_after_id = None
        self.hovering = True
        self._apply_hover_visibility()

    def _on_hover_leave(self, _event=None):
        if self._leave_after_id is not None:
            self.root.after_cancel(self._leave_after_id)
        self._leave_after_id = self.root.after(self.HOVER_LEAVE_DELAY, self._finish_hover_leave)

    def _finish_hover_leave(self):
        self._leave_after_id = None
        if self._is_pointer_inside_window():
            return
        self.hovering = False
        self._apply_hover_visibility()

    def _is_pointer_inside_window(self):
        self.root.update_idletasks()
        pointer_x = self.root.winfo_pointerx()
        pointer_y = self.root.winfo_pointery()
        window_x = self.root.winfo_rootx()
        window_y = self.root.winfo_rooty()
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        return (
            window_x <= pointer_x < window_x + window_width
            and window_y <= pointer_y < window_y + window_height
        )

    def _start_move(self, event):
        if self.locked:
            return
        self._drag_offset_x = event.x_root - self.root.winfo_x()
        self._drag_offset_y = event.y_root - self.root.winfo_y()

    def _move_window(self, event):
        if self.locked:
            return
        x = event.x_root - self._drag_offset_x
        y = event.y_root - self._drag_offset_y
        self.root.geometry(f"+{x}+{y}")

    def _start_resize(self, event):
        if self.locked:
            return
        self._resize_start_x = event.x_root
        self._resize_start_y = event.y_root
        self._resize_start_width = self.root.winfo_width()
        self._resize_start_height = self.root.winfo_height()

    def _resize_window(self, event):
        if self.locked:
            return
        delta_x = event.x_root - self._resize_start_x
        delta_y = event.y_root - self._resize_start_y
        self.width = max(self.MIN_WIDTH, self._resize_start_width + delta_x)
        self.height = max(self.MIN_HEIGHT, self._resize_start_height + delta_y)
        self.root.geometry(f"{self.width}x{self.height}")

    def _show_context_menu(self, event):
        self._build_context_menu()
        try:
            self.menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.menu.grab_release()

    def toggle_tip(self):
        self.show_tip = not self.show_tip
        self._apply_hover_visibility()

    def toggle_lock(self):
        self.locked = not self.locked
        self._apply_hover_visibility()

    def reset_to_bottom_center(self):
        """Restore the default size and place the mask near the screen bottom."""
        self.width = self.DEFAULT_WIDTH
        self.height = self.DEFAULT_HEIGHT
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = screen_height - self.height - self.BOTTOM_OFFSET
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")

    def restore_defaults(self):
        """Apply the built-in defaults without deleting the config file immediately."""
        self.alpha = self.DEFAULT_ALPHA
        self.show_tip = self.DEFAULT_SHOW_TIP
        self.locked = self.DEFAULT_LOCKED
        self.hovering = self._is_pointer_inside_window()
        self._apply_alpha(self.alpha)
        self._apply_hover_visibility()
        self.reset_to_bottom_center()

    def show_help(self):
        message = (
            "使用说明\n\n"
            "1. 将遮挡条放在字幕区域上方。\n"
            "2. 鼠标移入遮挡条时会显示提示文字和缩放手柄。\n"
            "3. 未锁定时，左键拖动可移动窗口，右下角可拖动缩放。\n"
            "4. 右键菜单可调整透明度、锁定/解锁、重置位置或恢复默认设置。\n\n"
            "快捷键：\n"
            "Esc：退出\n"
            "Ctrl+R：重置到底部居中\n"
            "Ctrl+H：切换提示文字偏好"
        )
        messagebox.showinfo("使用说明", message, parent=self.root)

    def show_about(self):
        message = (
            f"{APP_NAME} v{APP_VERSION}\n\n"
            "一个用于遮挡电影中文字幕的本地小工具。\n\n"
            "隐私说明：本软件不联网、不采集数据，仅保存本地配置。\n"
            f"配置文件：{self.CONFIG_PATH}"
        )
        messagebox.showinfo("关于软件", message, parent=self.root)

    def exit_app(self):
        self._save_config()
        self.root.destroy()

    def run(self):
        self.root.mainloop()
