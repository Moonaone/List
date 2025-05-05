import tkinter as tk
from tkinter import ttk
from database import DBManager

class MainApp:
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
        # 从数据库加载任务逻辑
        pass
        
    def open_pomodoro(self):
        # 打开番茄钟窗口
        PomodoroWindow(self.root)

if __name__ == '__main__':
    app = MainApp()
    app.root.mainloop()