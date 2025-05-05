import tkinter as tk
from tkinter import ttk
from database import DBManager
from pomodoro import PomodoroWindow

class MainApp:
    def open_pomodoro(self):
        PomodoroWindow(self.root)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            if self.db.add_task(task):
                self.load_tasks()
                self.task_entry.delete(0, 'end')

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('智能清单管理')
        
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.schedule_frame = ScheduleCountdownFrame(paned)
        self.todo_frame = TodoListFrame(paned)
        
        paned.add(self.schedule_frame, weight=1)
        paned.add(self.todo_frame, weight=2)
        paned.pack(fill=tk.BOTH, expand=True)
        self.db = DBManager()
        
        # 待办清单框架
        self.list_frame = ttk.LabelFrame(self.root, text='待办事项')
        self.list_tree = ttk.Treeview(self.list_frame, columns=('状态', '截止时间'), show='headings')
        self.list_tree.heading('#0', text='任务')
        self.list_tree.heading('状态', text='状态')
        self.list_tree.heading('截止时间', text='截止时间')
        
        # 番茄钟按钮
        self.pomo_btn = ttk.Button(self.root, text='启动番茄钟', command=self.open_pomodoro)
        
        # 布局组件
        self.list_frame.pack(padx=10, pady=10, fill='both', expand=True)
        self.list_tree.pack(fill='both', expand=True)
        self.pomo_btn.pack(pady=5)
        
        self.load_tasks()
        
        # 新增任务输入控件
        self.task_entry = ttk.Entry(self.list_frame)
        self.add_btn = ttk.Button(self.list_frame, text='添加任务', command=self.add_task)
        
        # 布局新增组件
        self.task_entry.pack(side='bottom', fill='x', padx=5, pady=5)
        self.add_btn.pack(side='bottom', pady=5)
        
    def load_tasks(self):
        self.list_tree.delete(*self.list_tree.get_children())
        for task in self.db.get_all_tasks():
            self.list_tree.insert('', 'end', iid=task[0], text=task[1], values=(task[2], task[3]))

class ScheduleCountdownFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = DBManager()
        
        ttk.Label(self, text='目标日期:').pack(pady=5)
        self.date_entry = DateEntry(self, date_pattern='yyyy-mm-dd')
        self.date_entry.pack(pady=5)
        
        self.countdown_label = ttk.Label(self, text='剩余时间：')
        self.countdown_label.pack(pady=10)
        
        ttk.Button(self, text='保存事件', command=self.save_schedule).pack()
        
    def save_schedule(self):
        target_date = self.date_entry.get_date()
        if self.db.add_schedule(target_date):
            self.update_countdown()

class TodoListFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.db = DBManager()
        
        self.tree = ttk.Treeview(self, columns=('状态', '描述'), show='headings')
        self.tree.heading('#0', text='任务')
        self.tree.heading('状态', text='状态')
        self.tree.heading('描述', text='描述')
        
        self.desc_entry = ttk.Entry(self)
        ttk.Button(self, text='添加任务', command=self.add_task).pack()

    def add_task(self):
        task = self.task_entry.get()
        if task:
            if self.db.add_task(task):
                self.load_tasks()
                self.task_entry.delete(0, 'end')

    def load_tasks(self):
        self.list_tree.delete(*self.list_tree.get_children())
        for task in self.db.get_all_tasks():
            self.list_tree.insert('', 'end', iid=task[0], text=task[1], values=(task[2], task[3]))



if __name__ == '__main__':
    app = MainApp()
    app.root.mainloop()