import tkinter as tk
from tkinter import ttk
from datetime import timedelta

class PomodoroWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('番茄工作钟')
        self.work_duration = 25 * 60  # 25分钟
        self.break_duration = 5 * 60  # 5分钟
        
        # 计时显示
        self.time_label = ttk.Label(self, text='25:00', font=('Arial', 48))
        self.time_label.pack(pady=10)
        
        # 控制按钮
        self.control_frame = ttk.Frame(self)
        self.start_btn = ttk.Button(self.control_frame, text='开始', command=self.start_timer)
        self.pause_btn = ttk.Button(self.control_frame, text='暂停', state='disabled', command=self.pause_timer)
        self.reset_btn = ttk.Button(self.control_frame, text='重置', command=self.reset_timer)
        
        self.control_frame.pack(pady=5)
        self.start_btn.pack(side='left', padx=5)
        self.pause_btn.pack(side='left', padx=5)
        self.reset_btn.pack(side='left', padx=5)
        
        self.timer_running = False
        self.remaining_time = self.work_duration

    def start_timer(self):
        self.timer_running = True
        self.start_btn.config(state='disabled')
        self.pause_btn.config(state='normal')
        self.update_timer()

    def pause_timer(self):
        self.timer_running = False
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled')

    def reset_timer(self):
        self.timer_running = False
        self.remaining_time = self.work_duration
        self.update_display()
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled')

    def update_timer(self):
        if self.timer_running and self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_display()
            self.after(1000, self.update_timer)
        elif self.remaining_time == 0:
            self.complete_session()

    def update_display(self):
        minutes, seconds = divmod(self.remaining_time, 60)
        self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")

    def complete_session(self):
        self.timer_running = False
        self.time_label.config(text="完成!")
        # TODO: 添加完成记录到数据库的逻辑