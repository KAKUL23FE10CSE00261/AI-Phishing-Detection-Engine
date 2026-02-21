import tkinter as tk
from tkinter import messagebox, ttk, TOP, BOTH, Toplevel
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PhishingUI:
    def __init__(self, root, model_engine, db):
        self.root = root
        self.model = model_engine
        self.db = db
        self.root.title("AI Phishing Detector")
        self.root.geometry("700x600")
        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Email Content:", font=("Arial", 12, "bold")).pack(pady=10)
        self.text_input = tk.Text(self.root, height=10, width=70)
        self.text_input.pack(pady=5)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Scan Email", command=self.scan_email, bg="#4CAF50", fg="white", width=15).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="View Analytics", command=self.show_dashboard, bg="#2196F3", fg="white", width=15).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Clear History", command=self.clear_ui_history, width=15).grid(row=0, column=2, padx=5)

        self.history_tree = ttk.Treeview(self.root, columns=("ID", "Prediction", "Score", "Time"), show='headings')
        self.history_tree.heading("ID", text="ID")
        self.history_tree.heading("Prediction", text="Prediction")
        self.history_tree.heading("Score", text="Score")
        self.history_tree.heading("Time", text="Time")
        self.history_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        self.load_history()

    def scan_email(self):
        email_content = self.text_input.get("1.0", tk.END).strip()
        if not email_content:
            messagebox.showwarning("Warning", "Please enter email text.")
            return

        result = self.model.predict(email_content)
        prediction = result['label']
        score = result['score']

        self.db.add_prediction(email_content, prediction, score)
        self.load_history()
        messagebox.showinfo("Result", f"This email is: {prediction}\nConfidence: {score:.2f}")

    def load_history(self):
        for i in self.history_tree.get_children():
            self.history_tree.delete(i)
        for row in self.db.get_all_predictions():
            self.history_tree.insert("", tk.END, values=(row[0], row[2], f"{row[3]:.2f}", row[4]))

    def clear_ui_history(self):
        # Implementation for clearing database can go here
        pass

    def show_dashboard(self):
        stats = self.db.get_stats()
        trends = self.db.get_daily_trends()

        dashboard_window = Toplevel(self.root)
        dashboard_window.title("Security Analytics Dashboard")
        dashboard_window.geometry("900x500")

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

        labels = list(stats.keys())
        values = list(stats.values())
        
        if any(values):
            ax1.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#F44336', '#4CAF50'])
        ax1.set_title("Total Detection Distribution")

        if trends:
            dates = [t[0] for t in trends]
            counts = [t[1] for t in trends]
            ax2.bar(dates, counts, color='#2196F3')
            ax2.set_title("Phishing Threats Caught Per Day")
            plt.setp(ax2.get_xticklabels(), rotation=45)
        else:
            ax2.text(0.5, 0.5, 'No Phishing Data Recorded', horizontalalignment='center', verticalalignment='center')

        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=dashboard_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)
