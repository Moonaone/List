import tkinter as tk
from tkinter import ttk
from database import DBManager
from pomodoro import PomodoroWindow

class MainApp:
    def open_pomodoro(self):
        PomodoroWindow(self.root)

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('智能清单管理')
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
        
    def load_tasks(self):
        self.list_tree.delete(*self.list_tree.get_children())
        for task in self.db.get_all_tasks():
            self.list_tree.insert('', 'end', iid=task[0], text=task[1], values=(task[2], task[3]))



if __name__ == '__main__':
    app = MainApp()
    app.root.mainloop()