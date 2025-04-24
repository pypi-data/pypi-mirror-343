import threading
import tkinter as tk
from io import BytesIO
import os
from ctypes import windll
import pyqrcode
from tkinter import messagebox, ttk
from functools import wraps
import queue





class TkinterThread(threading.Thread):
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            super().__init__()
            self._stop_event = threading.Event()
            self.daemon = True
            self.window = None
            self.tasks = queue.Queue()
            self.active_windows = {}  # 存储活动窗口 {window_id: window}
            self.result_queue = queue.Queue()  # 用于返回结果
            self._initialized = True

    def stop(self):
        self._stop_event.set()
        self.tasks.put(None)  # 唤醒线程

    def should_stop(self):
        return self._stop_event.is_set()

    def add_task(self, task, *args, **kwargs):
        """添加任务到队列，返回一个future用于获取结果"""
        future = FutureResult()
        self.tasks.put((future, task, args, kwargs))
        return future

    def run(self):
        try:
            if os.name == 'nt':
                windll.shcore.SetProcessDpiAwareness(1)

            self.window = tk.Tk()
            self.window.withdraw()

            while not self.should_stop():
                try:
                    item = self.tasks.get(timeout=0.1)
                    if item is None:
                        continue

                    future, task, args, kwargs = item
                    try:
                        result = task(*args, **kwargs)
                        future.set_result(result)
                    except Exception as e:
                        future.set_exception(e)
                except queue.Empty:
                    pass

                # 清理已关闭的窗口
                closed_windows = [
                    wid for wid, win in self.active_windows.items()
                    if not self._safe_winfo_exists(win)
                ]
                for wid in closed_windows:
                    self.active_windows.pop(wid)

                self.window.update()

        finally:
            if self.window:
                self.window.quit()
                self.window.destroy()

    def _safe_winfo_exists(self, win):
        """安全地检查窗口是否存在"""
        try:
            return win.winfo_exists()
        except RuntimeError:
            return False

    def is_window_alive(self, window_id):
        """检查指定窗口是否存活"""

        def _check():
            win = self.active_windows.get(window_id)
            return win is not None and self._safe_winfo_exists(win)

        future = self.add_task(_check)
        return future.get_result()

    def close_window(self, window_id):
        """强制关闭指定窗口"""

        def _close():
            win = self.active_windows.get(window_id)
            if win and self._safe_winfo_exists(win):
                win.destroy()
                self.active_windows.pop(window_id, None)

        self.add_task(_close)


class FutureResult:
    """用于异步获取结果"""

    def __init__(self):
        self._result = None
        self._exception = None
        self._condition = threading.Condition()
        self._ready = False

    def set_result(self, result):
        with self._condition:
            self._result = result
            self._ready = True
            self._condition.notify_all()

    def set_exception(self, exception):
        with self._condition:
            self._exception = exception
            self._ready = True
            self._condition.notify_all()

    def get_result(self, timeout=None):
        with self._condition:
            if not self._ready:
                self._condition.wait(timeout)
            if self._exception is not None:
                raise self._exception
            return self._result


def ensure_tkinter_thread_running(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        tk_thread = TkinterThread()
        if not tk_thread.is_alive():
            tk_thread.start()
        return func(*args, **kwargs)

    return wrapper




@ensure_tkinter_thread_running
def generate_qr_and_show(content):
    """显示二维码窗口"""
    window_id = f"qr_{threading.get_ident()}_{id(content)}"

    def show_qr_window():


        qr = pyqrcode.create(content)
        buffer = BytesIO()
        qr.png(buffer, scale=10, module_color=(0, 0, 0, 255), background=(255, 255, 255, 255))
        png_data = buffer.getvalue()


        window = tk.Toplevel()
        window.title("登录")
        window.resizable(False, False)

        # 方法2：使用tkinter内置的缩放因子检测
        scaling_factor = float(window.tk.call('tk', 'scaling')) / (72.0 / 96.0)  # 转换为标准DPI比例
        print(scaling_factor)
        def scale(value):
            """缩放函数"""
            return int(value * scaling_factor)


        # 设置最小尺寸（已缩放）
        # min_width = scale(200)
        # min_height = scale(200)
        # window.minsize(min_width, min_height)

        # 使用ttk框架和控件
        main_frame = ttk.Frame(window)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # 使用PIL处理图像以便缩放
        from PIL import Image, ImageTk
        img = Image.open(BytesIO(png_data))


        # 设置目标尺寸
        target_width = scale(160)
        target_height = scale(160)

        # 高质量缩放
        resized_image = img.resize((target_width, target_height))

        # 显示QR码
        img = ImageTk.PhotoImage(resized_image)
        label = ttk.Label(main_frame, image=img, justify='center')
        label.image = img
        label.pack(pady=scale(0))

        # 显示文本（使用缩放后的字体大小）
        font_size = scale(7)


        text_label = ttk.Label(
            main_frame,
            text="打开微信扫一扫登录",
            font=('Microsoft YaHei', font_size),

        )
        text_label.pack(pady=scale(4))

        # 窗口居中（使用缩放后的尺寸计算）
        # window.update_idletasks()  # 强制更新布局计算

        nScreenWid, nScreenHei = window.maxsize()
        nCurWid = scale(window.winfo_reqwidth() )
        nCurHeight = scale(window.winfo_reqheight())

        window.geometry(
            "+{}+{}".format(
                int(nScreenWid / 2 - nCurWid / 2),
                int(nScreenHei / 2 - nCurHeight / 2)
            )
        )

        # 设置窗口关闭行为
        window.protocol("WM_DELETE_WINDOW", window.destroy)
        return window

    tk_thread = TkinterThread()
    future = tk_thread.add_task(show_qr_window)
    window = future.get_result()
    tk_thread.active_windows[window_id] = window

    def is_alive():
        return tk_thread.is_window_alive(window_id)

    def close():
        tk_thread.close_window(window_id)

    return is_alive, close


@ensure_tkinter_thread_running
def show_message(content="弹窗内容", title="标题"):
    """显示消息框"""
    closed_msg = True
    def show_message_box():
        root = tk.Toplevel()
        root.withdraw()
        messagebox.showinfo(title, content)
        nonlocal closed_msg
        closed_msg = False

        root.destroy()
        return None  # 消息框无法被控制

    tk_thread = TkinterThread()
    tk_thread.add_task(show_message_box)

    def is_alive():
        return closed_msg  # 消息框无法被检测

    def close():
        pass  # 消息框无法被关闭

    return is_alive, close


if __name__ == "__main__":
    # 启动线程
    tk_thread = TkinterThread()
    if not tk_thread.is_alive():
        tk_thread.start()

    # 显示二维码窗口
    is_qr_alive, close_qr = generate_qr_and_show("https://example.com")
    print("二维码窗口是否存活:", is_qr_alive())  # True

    # 显示消息框
    is_msg_alive, close_msg = show_message("这是一个测试消息", "测试标题")
    print("消息框是否存活:", is_msg_alive())  # False
    while is_qr_alive():
        pass

    # 关闭二维码窗口
    # close_qr()