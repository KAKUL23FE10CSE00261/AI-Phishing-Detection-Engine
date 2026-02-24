import tkinter as tk
from ui import PhishingUI
from model import PhishingModel
from database import PredictionHistory
from analyst import PhishingAnalyst

def main():

    API_KEY = "FOR SECURITY PURPOSES I CANNOT LIST API KEY HERE"
    
    root = tk.Tk()
    
    model_engine = PhishingModel()
    db = PredictionHistory()
    analyst = PhishingAnalyst(api_key=API_KEY)
    
    app = PhishingUI(root, model_engine, db, analyst=analyst)
    
    root.mainloop()

if __name__ == "__main__":
    main()
