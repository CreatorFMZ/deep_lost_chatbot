# deep_lost_x2-1.4.0.2.py

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import random
import time
import datetime
import pyperclip
import os
import json

VERSION = "1.4.0.2"

LENGTH_RANGES = {
    "短": (100, 500),
    "中": (500, 1000),
    "长": (1000, 2000)
}

common_chars = [
    "的", "一", "是", "在", "不", "了", "有", "和", "人", "这", "中", "大", "为", "上", "个", "国", "我", "以", "要", "他",
    "时", "来", "用", "们", "生", "到", "作", "地", "于", "出", "就", "分", "对", "成", "会", "可", "主", "发", "年", "动",
    "同", "工", "也", "能", "下", "过", "子", "说", "产", "种", "面", "而", "方", "后", "多", "定", "行", "学", "法", "所",
    "民", "得", "经", "十", "三", "之", "进", "着", "等", "部", "度", "家", "电", "力", "里", "如", "水", "化", "高", "自",
    "二", "理", "起", "小", "物", "现", "实", "加", "量", "都", "两", "体", "制", "机", "当", "使", "点", "从", "业", "本",
    "去", "把", "性", "好", "应", "开", "它", "合", "还", "因", "由", "其", "些", "然", "前", "外", "天", "政", "四", "日",
    "那", "社", "义", "事", "平", "形", "相", "全", "表", "间", "样", "与", "关", "各", "重", "新", "线", "内", "数", "正",
    "心", "反", "你", "明", "看", "原", "又", "么", "利", "比", "或", "但", "质", "气", "第", "向", "道", "命", "此", "变",
    "条", "只", "没", "结", "解", "问", "意", "建", "月", "公", "无", "系", "军", "很", "情", "者", "最", "立", "代", "想",
    "已", "通", "并", "提", "直", "题", "党", "程", "展", "五", "果", "料", "象", "员", "次", "位", "常", "文", "总", "次",
    "品", "式", "活", "设", "及", "管", "特", "件", "长", "求", "老", "头", "基", "资", "边", "流", "路", "级", "少", "图",
    "山", "统", "接", "知", "较", "将", "组", "见", "计", "别", "她", "手", "角", "期", "根", "论", "运", "农", "指", "几",
    "九", "区", "强", "放", "决", "西", "被", "干", "做", "必", "战", "先", "回", "则", "任", "取", "据", "处", "队", "南",
    "给", "色", "光", "门", "即", "保", "治", "北", "造", "百", "规", "热", "领", "七", "海", "口", "东", "导", "器", "压",
    "志", "世", "金", "增", "争", "济", "阶", "油", "思", "术", "极", "交", "受", "联", "什", "认", "六", "共", "权", "收",
    "证", "改", "清", "美", "再", "采", "转", "更", "单", "风", "切", "打", "白", "教", "速", "花", "带", "安", "场", "身",
    "车", "例", "真", "务", "具", "万", "每", "目", "至", "达", "走", "积", "示", "议", "声", "报", "斗", "完", "类", "八",
    "离", "华", "名", "确", "才", "科", "张", "信", "马", "节", "话", "米", "整", "空", "元", "况", "今", "集", "温", "传",
    "土", "许", "步", "群", "广", "石", "记", "需", "段", "研", "界", "拉", "林", "律", "叫", "且", "究", "观", "越", "织",
    "装", "影", "算", "低", "持", "音", "众", "书", "布", "复", "容", "儿", "须", "际", "商", "非", "验", "连", "断", "深",
    "难", "近", "矿", "千", "周", "委", "素", "技", "备", "半", "办", "青", "省", "列", "习", "响", "约", "支", "般", "史",
    "感", "劳", "便", "团", "往", "酸", "历", "市", "克", "何", "除", "消", "构", "府", "称", "太", "准", "精", "值", "号",
    "率", "族", "维", "划", "选", "标", "写", "存", "候", "毛", "亲", "快", "效", "斯", "院", "查", "江", "型", "眼", "王"
]

THEMES = {
    "light": {
        "bg": "#f0f2f5",
        "card": "#ffffff",
        "text": "#1a1a1a",
        "muted_text": "#666666",
        "primary": "#0066cc",
        "muted": "#6c757d",
        "danger": "#dc3545",
        "entry_bg": "#ffffff",
        "insert_bg": "#0066cc",
        "status_fg": "#0066cc"
    },
    "dark": {
        "bg": "#0d1117",
        "card": "#161b22",
        "text": "#e6edf3",
        "muted_text": "#8b949e",
        "primary": "#58a6ff",
        "muted": "#6e7681",
        "danger": "#f85149",
        "entry_bg": "#0d1117",
        "insert_bg": "#58a6ff",
        "status_fg": "#58a6ff"
    }
}

class DeepLostX2:
    def __init__(self, root):
        self.root = root
        root.title(f"DeepLost X2 v{VERSION}")
        root.geometry("940x760")
        root.minsize(840, 660)

        # 主题相关
        self.theme_mode = "light"
        self.theme_file = "dl_theme.json"
        self.load_theme()
        self.current_theme = THEMES[self.theme_mode]

        self.font = ("Microsoft YaHei", 12)

        # ───────────── 所有控件创建区 ─────────────

        # 输出区
        self.output = scrolledtext.ScrolledText(
            root, wrap=tk.WORD, font=self.font,
            bg=self.current_theme["card"], fg=self.current_theme["text"],
            insertbackground=self.current_theme["insert_bg"]
        )
        self.output.pack(padx=14, pady=(14, 6), fill=tk.BOTH, expand=True)

        # 状态栏
        self.status = tk.Label(
            root, text="启动中...", font=self.font,
            fg=self.current_theme["status_fg"], bg=self.current_theme["bg"],
            anchor="w"
        )
        self.status.pack(fill=tk.X, padx=14, pady=(0, 4))

        # 输入区域
        input_frame = tk.Frame(root, bg=self.current_theme["bg"])
        input_frame.pack(fill=tk.X, padx=14, pady=6)

        self.input_entry = tk.Entry(
            input_frame, font=self.font, relief="flat",
            bg=self.current_theme["entry_bg"], fg=self.current_theme["text"],
            insertbackground=self.current_theme["insert_bg"]
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10), ipady=6)
        self.input_entry.bind("<Return>", self.on_send)

        self.model_var = tk.StringVar(value="thinking")
        self.model_menu = tk.OptionMenu(input_frame, self.model_var, "thinking", "fast")
        self.model_menu.config(font=self.font, width=9,
                               bg=self.current_theme["card"], fg=self.current_theme["text"])
        self.model_menu["menu"].config(bg=self.current_theme["card"], fg=self.current_theme["text"])
        self.model_menu.pack(side=tk.LEFT, padx=(0, 10))
        self.model_var.trace_add('write', self.on_model_change)

        send_btn = tk.Button(
            input_frame, text="发送", font=self.font,
            bg=self.current_theme["primary"], fg="white", relief="flat",
            command=self.on_send
        )
        send_btn.pack(side=tk.LEFT, ipadx=16, ipady=5)

        # 底部控制栏
        bottom_frame = tk.Frame(root, bg=self.current_theme["bg"])
        bottom_frame.pack(fill=tk.X, padx=14, pady=8)

        left = tk.Frame(bottom_frame, bg=self.current_theme["bg"])
        left.pack(side=tk.LEFT)

        about_btn = tk.Button(left, text="关于", font=self.font,
                              bg=self.current_theme["muted"], fg="white", relief="flat",
                              command=self.on_about)
        about_btn.pack(side=tk.LEFT, padx=(0, 10), ipadx=12, ipady=4)

        tk.Label(left, text="长度:", font=self.font,
                 bg=self.current_theme["bg"], fg=self.current_theme["text"]).pack(side=tk.LEFT, padx=(16, 4))

        self.length_var = tk.StringVar(value="中")
        self.length_menu = tk.OptionMenu(left, self.length_var, "短", "中", "长")
        self.length_menu.config(font=self.font, width=6,
                                bg=self.current_theme["card"], fg=self.current_theme["text"])
        self.length_menu["menu"].config(bg=self.current_theme["card"], fg=self.current_theme["text"])
        self.length_menu.pack(side=tk.LEFT)

        right = tk.Frame(bottom_frame, bg=self.current_theme["bg"])
        right.pack(side=tk.RIGHT)

        tk.Button(right, text="复制", font=self.font,
                  bg=self.current_theme["muted"], fg="white", relief="flat",
                  command=self.copy_output).pack(side=tk.LEFT, padx=(0, 8), ipadx=12, ipady=4)

        tk.Button(right, text="保存文本", font=self.font,
                  bg=self.current_theme["muted"], fg="white", relief="flat",
                  command=self.save_output).pack(side=tk.LEFT, padx=(0, 8), ipadx=12, ipady=4)

        self.theme_btn = tk.Button(right,
                                   text="浅色主题" if self.theme_mode == "dark" else "深色主题",
                                   font=self.font,
                                   bg=self.current_theme["muted"], fg="white", relief="flat",
                                   command=self.toggle_theme)
        self.theme_btn.pack(side=tk.LEFT, padx=(0, 8), ipadx=12, ipady=4)

        self.end_btn = tk.Button(right, text="结束对话", font=self.font,
                                 bg=self.current_theme["danger"], fg="white", relief="flat",
                                 command=self.on_end_conversation)
        self.end_btn.pack(side=tk.LEFT, ipadx=12, ipady=4)

        # ───────────── 控件创建完毕，现在才统一再刷一次主题（保险） ─────────────
        self.apply_theme()

        # 其他初始化
        self.first_response = True
        self.ended = False

        self.startup_step = 0
        self.startup_messages = [
            ("初始化智能系统...", 250),
            ("加载语言模型..........", 300),
            ("连接语义网络..........", 200),
            ("系统就绪！", 0)
        ]

        self.root.after(50, self.next_startup)

    def apply_theme(self):
        t = self.current_theme
        self.root.configure(bg=t["bg"])
        self.output.configure(bg=t["card"], fg=t["text"], insertbackground=t["insert_bg"])
        self.status.configure(bg=t["bg"], fg=t["status_fg"])
        self.input_entry.configure(bg=t["entry_bg"], fg=t["text"], insertbackground=t["insert_bg"])
        self.theme_btn.configure(text="浅色主题" if self.theme_mode == "dark" else "深色主题")

    def toggle_theme(self):
        self.theme_mode = "dark" if self.theme_mode == "light" else "light"
        self.current_theme = THEMES[self.theme_mode]
        self.apply_theme()
        self.save_theme()

    def save_theme(self):
        try:
            with open(self.theme_file, "w", encoding="utf-8") as f:
                json.dump({"theme": self.theme_mode}, f)
        except:
            pass

    def load_theme(self):
        if os.path.exists(self.theme_file):
            try:
                with open(self.theme_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    mode = data.get("theme")
                    if mode in THEMES:
                        self.theme_mode = mode
            except:
                pass

    def next_startup(self):
        if self.startup_step >= len(self.startup_messages):
            return
        msg, delay = self.startup_messages[self.startup_step]
        self.status.config(text=msg)
        self.startup_step += 1
        if self.startup_step < len(self.startup_messages):
            self.root.after(delay, self.next_startup)
        else:
            self.root.after(200, self.show_greeting)

    def show_greeting(self):
        self.append_output("【AI助手】您好！我是DeepLost-X2，一个先进的语言模型。\n")
        self.append_output("【AI助手】我可以帮助您创作诗歌、文章、故事或任何文本内容。\n")
        self.append_output("【AI助手】请在下方输入您的请求或主题：\n\n")
        self.status.config(text="就绪")

    def append_output(self, text):
        self.output.insert(tk.END, text)
        self.output.see(tk.END)

    def on_send(self, event=None):
        if self.ended: return
        query = self.input_entry.get().strip()
        if not query: return
        self.append_output(f"\n【用户】: {query}\n")
        self.input_entry.delete(0, tk.END)
        self.status.config(text="正在分析您的请求...")
        self.root.after(300, lambda: self.simulate_processing(query))

    def simulate_processing(self, query):
        mode = self.model_var.get()
        self.processing_base = f"【系统】正在分析您的请求: \"{query}\"（模式: {mode}） 深度神经网络处理中"
        self.status.config(text=self.processing_base)
        self.dot_count = 0
        if mode == 'fast':
            self.dot_limit = 5
            self.dot_interval = 100
            self.final_delay = 200
        else:
            self.dot_limit = 10
            self.dot_interval = 280
            self.final_delay = 600
        self.add_dots()

    def add_dots(self):
        if self.dot_count < self.dot_limit:
            self.status.config(text=self.status.cget("text") + ".")
            self.dot_count += 1
            self.root.after(self.dot_interval, self.add_dots)
        else:
            self.root.after(self.final_delay, self.generate_response)

    def generate_text(self):
        mode = self.model_var.get()
        if mode == 'fast':
            length = random.randint(10, 150)
            return ''.join(random.choices(common_chars, k=length))

        choice = self.length_var.get()
        low, high = LENGTH_RANGES.get(choice, (150, 800))
        length = random.randint(low, high)
        text = ''.join(random.choices(common_chars, k=length))

        punct = ['，', '。', '！', '？', '；', '：', '、']
        positions = sorted(random.sample(range(5, length-5), min(length//12, 40)))
        offset = 0
        for pos in positions:
            p = random.choice(punct)
            text = text[:pos+offset] + p + text[pos+offset:]
            offset += 1

        para_positions = sorted(random.sample(range(50, len(text)-50), max(1, len(text)//120)))
        offset = 0
        for pos in para_positions:
            text = text[:pos+offset] + "\n\n" + text[pos+offset:]
            offset += 2

        return text

    def generate_response(self):
        text = self.generate_text()
        prefix = "基于您的主题，我创作了以下内容：" if self.first_response else "根据您的反馈，我优化了内容："
        self.first_response = False

        self.append_output(f"【AI助手】{prefix}\n")
        self.append_output("════════════════════════════════════════\n")
        self.append_output(text + "\n")
        self.append_output("════════════════════════════════════════\n\n")
        self.append_output("【AI助手】您对结果满意吗？请输入反馈或新请求（点击“结束对话”结束会话）。\n")
        self.status.config(text="就绪")

    def copy_output(self):
        try:
            pyperclip.copy(self.output.get("1.0", tk.END).strip())
            self.status.config(text="已复制到剪贴板")
            self.root.after(1800, lambda: self.status.config(text="就绪") if not self.ended else None)
        except:
            self.status.config(text="复制失败")
            self.root.after(1800, lambda: self.status.config(text="就绪") if not self.ended else None)

    def save_output(self):
        content = self.output.get("1.0", tk.END).strip()
        if not content.strip(): return

        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        default_name = f"DeepLost-X2_{now}.txt"

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
            initialfile=default_name,
            title="保存输出"
        )
        if not path: return

        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.status.config(text="已保存")
            self.root.after(1800, lambda: self.status.config(text="就绪") if not self.ended else None)
        except Exception as e:
            messagebox.showerror("保存失败", str(e))

    def on_about(self):
        messagebox.showinfo("关于", f"DeepLost X2\n版本 {VERSION}\n© Fanatic Star 2026")

    def on_model_change(self, *args):
        if self.model_var.get() == "fast":
            self.length_menu.config(state="disabled")
            self.length_var.set("短")
        else:
            self.length_menu.config(state="normal")

    def on_end_conversation(self):
        self.append_output("\n【系统】本次会话已结束。感谢使用！©Fanatic Star 2026\n")
        self.status.config(text="会话已结束")
        self.ended = True
        self.input_entry.config(state="disabled")
        self.model_menu.config(state="disabled")
        self.length_menu.config(state="disabled")
        self.end_btn.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = DeepLostX2(root)
    root.mainloop()