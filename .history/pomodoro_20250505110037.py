import tkinter as tk
from tkinter import ttk
from datetime import timedelta

from database import DBManager

class PomodoroWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = DBManager()
        self.title('番茄工作钟')
        
        # 配置面板
        self.config_frame = ttk.Frame(self)
        ttk.Label(self.config_frame, text='工作时间（分）:').grid(row=0, column=0, padx=5)
        self.work_entry = ttk.Entry(self.config_frame, width=5, validate='key')
        self.work_entry.grid(row=0, column=1, padx=5)
        # 加载保存的配置
        saved_work = self.db.get_setting('work_time', '25')
        saved_break = self.db.get_setting('break_time', '5')
        self.work_entry.insert(0, saved_work)
        self.break_entry.insert(0, saved_break)
        
        ttk.Label(self.config_frame, text='休息时间（分）:').grid(row=1, column=0)
        self.break_entry = ttk.Entry(self.config_frame, width=5, validate='key')
        self.break_entry.grid(row=1, column=1)
        self.break_entry.insert(0, '5')
        
        self.save_btn = ttk.Button(self.config_frame, text='保存配置', command=self.save_settings)
        self.save_btn.grid(row=2, columnspan=2, pady=5)
        
        self.config_frame.pack(pady=10)
        
        # 初始化持续时间
        self.work_duration = 25 * 60
        self.break_duration = 5 * 60
        
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
        # 从输入框获取最新配置
        self.work_duration = int(self.work_entry.get()) * 60
        self.break_duration = int(self.break_entry.get()) * 60
        self.remaining_time = self.work_duration
        
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
        self.work_duration = int(self.work_entry.get()) * 60
        self.remaining_time = self.work_duration
        self.update_display()
        self.start_btn.config(state='normal')
        self.pause_btn.config(state='disabled')
    
    def save_settings(self):
        try:
            self.db.save_setting('work_time', self.work_entry.get())
            self.db.save_setting('break_time', self.break_entry.get())
            self.save_btn.config(text='保存成功!')
            self.after(2000, lambda: self.save_btn.config(text='保存配置'))
        except ValueError:
            self.save_btn.config(text='请输入数字')
            self.after(2000, lambda: self.save_btn.config(text='保存配置'))

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