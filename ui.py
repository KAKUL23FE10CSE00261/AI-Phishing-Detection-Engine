import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
from model import PhishingModel
from database import PredictionHistory

class PhishingUI:
    def __init__(self, master):
        self.master = master
        master.title("AI Phishing Detection Engine")
        master.geometry("800x650")

        self.model = PhishingModel()
        self.db = PredictionHistory()

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = ttk.Frame(master, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Security Analysis Dashboard", font=("Helvetica", 16, "bold")).pack(pady=10)
        
        ttk.Label(main_frame, text="Enter Email Content:").pack(anchor='w')
        self.text_area = scrolledtext.ScrolledText(main_frame, height=8, font=("Consolas", 11))
        self.text_area.pack(fill=tk.X, pady=10)

        self.analyze_btn = ttk.Button(main_frame, text="Run AI Analysis", command=self.analyze_text)
        self.analyze_btn.pack(pady=10)

        self.result_label = ttk.Label(main_frame, text="Status: Ready", font=("Helvetica", 14, "italic"))
        self.result_label.pack(pady=15)

        ttk.Label(main_frame, text="Analysis History:", font=("Helvetica", 10, "bold")).pack(anchor='w')
        self.tree = ttk.Treeview(main_frame, columns=("Time", "Text", "Result"), show="headings")
        self.tree.heading("Time", text="Timestamp")
        self.tree.heading("Text", text="Snippet")
        self.tree.heading("Result", text="Classification")
        self.tree.column("Time", width=150)
        self.tree.column("Text", width=450)
        self.tree.column("Result", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.load_history()

    def analyze_text(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Input Error", "Please provide text to analyze.")
            return
            
        self.result_label.config(text="Analyzing...", foreground="blue")
        self.master.update_idletasks()

        res, conf = self.model.predict(text)
        self.db.add_prediction(text, res, conf)
        
        color = "red" if res == "Phishing" else "green"
        self.result_label.config(text=f"{res} Detection (Confidence: {conf:.2f})", foreground=color)
        self.load_history()

    def load_history(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        for row in self.db.get_all_predictions():
            self.tree.insert("", tk.END, values=(row[4], row[1][:60] + "...", row[2]))