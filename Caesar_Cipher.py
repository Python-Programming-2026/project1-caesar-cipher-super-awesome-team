import tkinter as tk
from tkinter import ttk, messagebox, filedialog

def caesar_cipher(text: str, key: int, mode: str = 'encrypt') -> str:
    """凯撒密码核心加密/解密算法"""
    if mode == 'decrypt':
        key = -key

    result = []
    for ch in text:
        if ch.isalpha():
            base = ord('A') if ch.isupper() else ord('a')
            shifted = (ord(ch) - base + key) % 26
            result.append(chr(shifted + base))
        else:
            result.append(ch)
    return "".join(result)

class CaesarCipherGUI:
    def __init__(self, master):
        self.master = master
        master.title("🛡️ 凯撒密码工具箱 Pro")
        master.geometry("520x560")
        master.resizable(False, False) # 固定窗口大小，保持布局美观

        # --- 顶部：密钥输入与文件操作 ---
        frame_top = ttk.Frame(master, padding=10)
        frame_top.pack(fill=tk.X)

        ttk.Label(frame_top, text="密钥 (整数):").pack(side=tk.LEFT)
        self.key_entry = ttk.Entry(frame_top, width=10)
        self.key_entry.pack(side=tk.LEFT, padx=5)
        self.key_entry.insert(0, "3") # 默认密钥为3

        ttk.Button(frame_top, text="📂 导入文件", command=self.load_file).pack(side=tk.RIGHT, padx=5)
        ttk.Button(frame_top, text="💾 保存结果", command=self.save_file).pack(side=tk.RIGHT)

        # --- 中间：输入文本区 ---
        ttk.Label(master, text="输入区 (明文/密文):").pack(anchor=tk.W, padx=10)
        self.text_in = tk.Text(master, height=8, width=65, font=("Microsoft YaHei", 10))
        self.text_in.pack(padx=10, pady=5)

        # --- 核心：操作按钮区 ---
        frame_btn = ttk.Frame(master, padding=10)
        frame_btn.pack(fill=tk.X)
        
        ttk.Button(frame_btn, text="🔒 加密", command=lambda: self.process('encrypt')).pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(frame_btn, text="🔓 解密", command=lambda: self.process('decrypt')).pack(side=tk.LEFT, expand=True, padx=5)
        ttk.Button(frame_btn, text="🔨 暴力破解", command=self.brute_force).pack(side=tk.LEFT, expand=True, padx=5)

        # --- 底部：输出结果区 ---
        ttk.Label(master, text="输出区 (处理结果):").pack(anchor=tk.W, padx=10)
        self.text_out = tk.Text(master, height=12, width=65, font=("Microsoft YaHei", 10))
        self.text_out.pack(padx=10, pady=5)

    def get_key(self) -> int:
        """安全获取密钥"""
        try:
            return int(self.key_entry.get()) % 26
        except ValueError:
            messagebox.showerror("输入错误", "密钥必须是整数！")
            return None

    def process(self, mode: str) -> None:
        """处理加密或解密"""
        key = self.get_key()
        if key is None: return
        
        text = self.text_in.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("提示", "请输入需要处理的文本！")
            return
            
        result = caesar_cipher(text, key, mode)
        self.text_out.delete("1.0", tk.END)
        self.text_out.insert("1.0", result)

    def brute_force(self) -> None:
        """执行暴力破解"""
        text = self.text_in.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("提示", "请输入需要破解的密文！")
            return

        self.text_out.delete("1.0", tk.END)
        self.text_out.insert(tk.END, "====== 暴力破解结果 (1-25) ======\n\n")
        
        for key in range(1, 26):
            plaintext = caesar_cipher(text, key, 'decrypt')
            # 截取前80个字符显示，避免长文本卡顿界面
            display_text = plaintext[:80] + ("..." if len(plaintext) > 80 else "")
            self.text_out.insert(tk.END, f"🔑 尝试密钥 {key:02d} |  {display_text}\n")

    def load_file(self) -> None:
        """通过弹窗选择并读取文件"""
        filepath = filedialog.askopenfilename(filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")])
        if filepath:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.text_in.delete("1.0", tk.END)
                self.text_in.insert("1.0", f.read())

    def save_file(self) -> None:
        """通过弹窗保存结果到文件"""
        result = self.text_out.get("1.0", tk.END).strip()
        if not result:
            messagebox.showwarning("提示", "当前没有可以保存的结果！")
            return
            
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("文本文件", "*.txt")])
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(result)
            messagebox.showinfo("成功", "文件已成功保存！")

# 启动程序
if __name__ == "__main__":
    root = tk.Tk()
    app = CaesarCipherGUI(root)
    root.mainloop()