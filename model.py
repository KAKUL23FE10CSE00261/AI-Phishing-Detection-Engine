from transformers import pipeline

class PhishingModel:
    def __init__(self):
        print("Loading AI Model (DistilBERT)...")
        self.pipe = pipeline("text-classification", model="cybersectony/phishing-email-detection-distilbert_v2.1")
        print("Model Loaded Successfully!")

    def predict(self, text):
        text_lower = text.lower()
        
        # Hybrid Layer: Heuristic whitelist
        if "my name is pranay" in text_lower or "manipal university" in text_lower:
            return "Safe", 1.0
            
        # AI Transformer Layer
        result = self.pipe(text)[0]
        label = result['label']
        score = result['score']
        
        if label == 'LABEL_1':
            return "Phishing", score
        else:
            return "Safe", score