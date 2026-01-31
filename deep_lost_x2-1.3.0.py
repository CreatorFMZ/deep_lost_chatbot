import tkinter as tk
from tkinter import scrolledtext, messagebox
import random
import time

VERSION = "1.3.0"
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

class DeepLostX2:
    def __init__(self, root):
        self.root = root
        root.title("DeepLost X2 - 先进语言模型")
        root.geometry("900x700")
        root.minsize(800, 600)

        font = ("Microsoft YaHei", 12)
        title_font = ("Microsoft YaHei", 16, "bold")

        self.output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=font, bg="#f8f9fa", fg="#212529")
        self.output.pack(padx=10, pady=(10, 5), fill=tk.BOTH, expand=True)

        self.status = tk.Label(root, text="启动中...", font=font, fg="#0066cc")
        self.status.pack(pady=5)

        input_frame = tk.Frame(root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        self.input_entry = tk.Entry(input_frame, font=font, width=60)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.input_entry.bind("<Return>", self.on_send)

        # 模型选择（thinking: 默认，fast: 快速模式）
        self.model_var = tk.StringVar(value="thinking")
        model_menu = tk.OptionMenu(input_frame, self.model_var, "thinking", "fast")
        model_menu.config(font=font, width=10)
        model_menu.pack(side=tk.RIGHT, padx=(0, 10))
        # 当模型切换为 fast 时，禁用长度选择
        self.model_var.trace_add('write', self.on_model_change)


        self.send_btn = tk.Button(input_frame, text="发送", font=font, bg="#0066cc", fg="white", width=10, command=self.on_send)
        self.send_btn.pack(side=tk.RIGHT) 

        bottom_frame = tk.Frame(root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=8)

        about_btn = tk.Button(bottom_frame, text="关于", font=font, bg="#6c757d", fg="white", width=10, command=self.on_about)
        about_btn.pack(side=tk.LEFT)

        # thinking 模式可用的长度选择
        length_label = tk.Label(bottom_frame, text="长度:", font=font)
        length_label.pack(side=tk.LEFT, padx=(8,0))
        self.length_var = tk.StringVar(value="中")
        self.length_menu = tk.OptionMenu(bottom_frame, self.length_var, "短", "中", "长")
        self.length_menu.config(font=font, width=6)
        self.length_menu.pack(side=tk.LEFT, padx=(4, 10))

        self.end_btn = tk.Button(bottom_frame, text="结束对话", font=font, bg="#dc3545", fg="white", width=10, command=self.on_end_conversation)
        self.end_btn.pack(side=tk.RIGHT)

        self.first_response = True
        self.startup_step = 0
        # 缩短启动序列总时长到约 1000ms（1s）
        self.startup_messages = [
            ("初始化智能系统...", 250),
            ("加载语言模型..........", 300),
            ("连接语义网络..........", 200),
            ("系统就绪！", 0)
        ]

        # 初始等待改为 50ms，整个启动过程约为 1s
        self.root.after(50, self.next_startup)

    def next_startup(self):
        if self.startup_step >= len(self.startup_messages):
            return
        msg, delay = self.startup_messages[self.startup_step]
        self.status.config(text=msg)
        self.startup_step += 1
        if self.startup_step < len(self.startup_messages):
            self.root.after(delay, self.next_startup)
        else:
            # 在最后一步后稍微等待以显示就绪状态，然后展示问候，总体控制在 1 秒左右
            self.root.after(200, self.show_greeting)

    def show_greeting(self):
        self.append_output("【AI助手】您好！我是DeepLost-X2，一个先进的语言模型。\n")
        self.append_output("【AI助手】我可以帮助您创作诗歌、文章、故事或任何文本内容。\n")
        self.append_output("【AI助手】请在下方输入您的请求或主题：\n\n")
        self.status.config(text="就绪")

    def append_output(self, text):
        self.output.insert(tk.END, text)
        self.output.see(tk.END)
        self.root.update_idletasks()

    def on_send(self, event=None):
        query = self.input_entry.get().strip()
        if not query:
            return
        self.append_output(f"\n【用户】: {query}\n")
        self.input_entry.delete(0, tk.END)
        self.status.config(text="正在分析您的请求...")
        self.root.after(300, lambda: self.simulate_processing(query))

    def simulate_processing(self, query):
        mode = self.model_var.get() if hasattr(self, 'model_var') else 'thinking'
        self.processing_base = f"【系统】正在分析您的请求: \"{query}\"（模式: {mode}） 深度神经网络处理中"
        self.status.config(text=self.processing_base)
        self.dot_count = 0
        # 根据模型调整加载节奏：fast 总时长约 1s（包含前置的 300ms 延迟），没有标点与换行；
        # thinking 使用默认较慢节奏和标点/换行
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
        if self.dot_count < getattr(self, 'dot_limit', 10):
            self.status.config(text=self.status.cget("text") + ".")
            self.dot_count += 1
            self.root.after(getattr(self, 'dot_interval', 280), self.add_dots)
        else:
            self.root.after(getattr(self, 'final_delay', 600), self.generate_response) 

    def generate_text(self):
        mode = self.model_var.get() if hasattr(self, 'model_var') else 'thinking'

        # fast 模式生成更短的连续文本（无标点与换行）
        if mode == 'fast':
            length = random.randint(10, 150)  # fast 模式固定更短范围
            text = ''.join(random.choices(common_chars, k=length))
            return text

        # thinking 模式保持原有较长、有标点与换行的文本，长度根据底部选择器决定
        choice = self.length_var.get() if hasattr(self, 'length_var') else '中'
        low, high = LENGTH_RANGES.get(choice, (150, 800))
        length = random.randint(low, high)
        text = ''.join(random.choices(common_chars, k=length))

        punct = ['，', '。', '！', '？', '；', '：', '、']
        positions = sorted(random.sample(range(5, length - 5), min(length // 12, 40)))
        offset = 0
        for pos in positions:
            p = random.choice(punct)
            text = text[:pos + offset] + p + text[pos + offset:]
            offset += 1

        para_positions = sorted(random.sample(range(50, len(text) - 50), max(1, len(text) // 120)))
        offset = 0
        for pos in para_positions:
            text = text[:pos + offset] + "\n\n" + text[pos + offset:]
            offset += 2

        return text

    def generate_response(self):
        text = self.generate_text()

        if self.first_response:
            prefix = "基于您的主题，我创作了以下内容：\n"
            self.first_response = False
        else:
            prefix = "根据您的反馈，我优化了内容：\n"

        self.append_output(f"【AI助手】{prefix}")
        self.append_output("════════════════════════════════════════\n")
        self.append_output(text + "\n")
        self.append_output("════════════════════════════════════════\n\n")
        self.append_output("【AI助手】您对结果满意吗？请输入反馈或新请求（点击“结束对话”结束会话）。\n")
        self.status.config(text="就绪")

    def on_about(self):
        info = f"DeepLost X2\n版本: {VERSION}\n© Fanatic Star 2026\n保留所有权利。"
        messagebox.showinfo("关于 DeepLost X2", info)

    def on_model_change(self, *args):
        mode = self.model_var.get()
        # fast 模式时禁用长度选择并将长度设为短（但实际生成使用 10-150）
        if mode == 'fast':
            try:
                self.length_menu.config(state='disabled')
                self.length_var.set('短')
            except Exception:
                pass
        else:
            try:
                self.length_menu.config(state='normal')
            except Exception:
                pass

    def on_end_conversation(self):
        self.append_output("\n【系统】本次会话已结束。感谢使用DeepLost-X2！期待下次为您服务。©Fanatic Star 2026.\n")
        self.status.config(text="会话已结束")
        self.input_entry.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        self.end_btn.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = DeepLostX2(root)
    root.mainloop()