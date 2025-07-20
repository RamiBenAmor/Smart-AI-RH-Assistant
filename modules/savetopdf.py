
import os

def savetopdf(text, filename):
    output_path = "C:\\Users\\ramib\\OneDrive\\Bureau\\CV_RH\\results"
    os.makedirs(output_path, exist_ok=True)

    full_path = os.path.join(output_path, filename)

    # Écriture en UTF-8 pour bien gérer les caractères spéciaux
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(text)
