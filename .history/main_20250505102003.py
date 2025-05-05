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
        
    class MainApp:
        def load_tasks(self):
            self.list_tree.delete(*self.list_tree.get_children())
            for task in self.db.get_all_tasks():
                self.list_tree.insert('', 'end', iid=task[0], text=task[1], values=(task[2], task[3]))
    
    class PomodoroWindow:
        def update_timer(self):
            if self.timer_running and self.remaining_time > 0:
                mins, secs = divmod(self.remaining_time, 60)
                self.time_label.config(text=f"{mins:02d}:{secs:02d}")
                self.remaining_time -= 1
                self.root.after(1000, self.update_timer)
            else:
                self.timer_running = False
                self.time_label.config(text="时间到！")
                self.start_btn.config(state='normal')
                self.pause_btn.config(state='disabled')
    
    def open_pomodoro(self):
        # 打开番茄钟窗口
        PomodoroWindow(self.root)
        
        # 新增任务输入框和操作按钮
        self.input_frame = ttk.Frame(self.root)
        self.task_entry = ttk.Entry(self.input_frame, width=30)
        self.add_btn = ttk.Button(self.input_frame, text='添加', command=self.add_task)
        self.del_btn = ttk.Button(self.input_frame, text='删除', command=self.delete_task)
        
        self.task_entry.pack(side='left', padx=5)
        self.add_btn.pack(side='left', padx=5)
        self.del_btn.pack(side='left', padx=5)
        self.input_frame.pack(pady=5)
        
        # 绑定树形视图事件
        self.list_tree.bind('<<TreeviewSelect>>', self.on_task_select)
    
    def add_task(self):
        task = self.task_entry.get()
        if task and self.db.add_task(task):
            self.load_tasks()
            self.task_entry.delete(0, 'end')
    
    def delete_task(self):
        selected = self.list_tree.selection()
        if selected and self.db.delete_task(selected[0]):
            self.load_tasks()
    
    def on_task_select(self, event):
        pass

if __name__ == '__main__':
    app = MainApp()
    app.root.mainloop()