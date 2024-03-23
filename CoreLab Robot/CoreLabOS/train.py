from transformers import pipeline
import pandas as pd

# Initialisieren der Sentiment-Analyse-Pipeline mit einem vortrainierten Modell
# Hier als Beispiel ein allgemeines Sentiment-Modell; für Emotionserkennung ein spezifisches Modell wählen
classifier = pipeline('sentiment-analysis', model='distilbert-base-uncased-finetuned-sst-2-english')

# Lesen der Chat-Daten
with open('data/chat.txt', 'r', encoding='utf-8') as file:
    chat_lines = file.readlines()

# Vorverarbeitung (optional, basierend auf Ihrem Datensatz)
# Beispiel: Entfernen von Zeitstempeln, wenn vorhanden

# Analyse der Emotionen/Sentiments in den Nachrichten
results = []
for line in chat_lines:
    # Analyse der einzelnen Zeilen
    result = classifier(line)
    results.append(result)

# Speichern der Ergebnisse für spätere Verwendung
df = pd.DataFrame(results)
df.to_csv('data/analyzed_chat.csv', index=False)

# Der DataFrame df enthält jetzt die ursprünglichen Nachrichten und deren analysierte Sentiments oder Emotionen
