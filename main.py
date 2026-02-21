import tkinter as tk
from ui import PhishingUI
from model import PhishingModel
from database import PredictionHistory

def main():
    root = tk.Tk()
    
    # stttart logic and database first
    model_engine = PhishingModel()
    db = PredictionHistory()
    
    # Pass them into the UI
    app = PhishingUI(root, model_engine, db)
    
    root.mainloop()

if __name__ == "__main__":
    main()
