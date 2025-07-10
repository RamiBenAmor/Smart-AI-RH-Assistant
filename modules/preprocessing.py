import PyPDF2  
import nltk
import re
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('stopwords') 
def load_text(filepath):
    text = ""

    # Ouvre le fichier PDF en lecture binaire
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)  # ✅ PdfReader, pas .load

        # Itère sur chaque page et ajoute son texte
        for page in reader.pages:
            text += page.extract_text()

    return text
ALLOWED_INSIDE_TOKENS = r'+#\.\-/'
stop_words = set(stopwords.words('english'))

def clean_text(text: str) -> str:
    """
    Nettoyage léger :
    - Minuscule
    - Garde les chiffres
    - Garde les caractères utiles (+ # . - /)
    - Supprime le reste de la ponctuation
    - Supprime les stopwords
    """
    # 1. Minuscule
    text = text.lower()

    # 2. Sauts de ligne/tab → espace
    text = re.sub(r'[\r\n\t]', ' ', text)

    # 3. Supprimer les caractères non autorisés
    text = re.sub(fr'[^\w{ALLOWED_INSIDE_TOKENS}\s]', ' ', text)

    # 4. Tokenisation
    tokens = nltk.word_tokenize(text)

    # 5. Enlève les mots trop courts (< 2) OU dans stopwords
    tokens = [tok for tok in tokens if tok not in stop_words]

    return ' '.join(tokens)

def preprocess_pdf(filepath):
    text=load_text(filepath)
    return clean_text(text)
