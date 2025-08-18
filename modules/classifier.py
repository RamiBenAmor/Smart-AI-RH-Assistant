from transformers import BertTokenizer, BertForSequenceClassification
import torch

# Charger modèle + tokenizer
model_path = "{Your path}\\Smart-AI-RH-Assistant\\models\\bert_base_uncased_Fine_Tuned"
tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path)
model.eval()
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder() #label encoder entrainé.
# Exemple à classer
texte = "Ahmed Ali is an agricultural specialist focused on sustainable farming techniques and crop management. Over 8 years of experience advising farmers on soil health, irrigation systems, and pest control. Skilled in data-driven agriculture and environmental impact assessments."

# Tokenisation
inputs = tokenizer(texte, return_tensors="pt", padding=True, truncation=True, max_length=512)

# Prédiction
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_id = torch.argmax(logits, dim=1).item()

# Traduire en label texte (avec LabelEncoder)
predicted_label =le.inverse_transform([predicted_class_id])[0]

print(f"Le texte est classé dans la catégorie : {predicted_label}")
