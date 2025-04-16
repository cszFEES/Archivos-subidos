import pandas as pd
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# nltk.download('vader_lexicon')
def analizar_sentimiento(texto):
    sia = SentimentIntensityAnalyzer()
    puntuaciones_sentimiento = sia.polarity_scores(texto)
    if puntuaciones_sentimiento['compound'] >= 0.05:
        sentimiento_general = 'Positivo'
    elif puntuaciones_sentimiento['compound'] <= -0.05:
        sentimiento_general = 'Negativo'
    else:
        sentimiento_general = 'Neutral'
    return puntuaciones_sentimiento, sentimiento_general

def analizar_multiples_textos(textos):
    resultados = []
    for texto in textos:
        puntuaciones, sentimiento = analizar_sentimiento(texto)
        resultados.append({
            'Texto': texto,
            'Positivo': puntuaciones['pos'],
            'Neutral': puntuaciones['neu'],
            'Negativo': puntuaciones['neg'],
            'Compuesto': puntuaciones['compound'],
            'Sentimiento General': sentimiento
        })
    return pd.DataFrame(resultados)

textos = [
    "¡Me encanta este producto! ¡Es increíble!",
    "Esto es terrible. Lo odio.",
    "El clima está bien hoy.",
    "¡Me siento genial sobre el próximo evento!",
    "Esta película fue una completa pérdida de tiempo."
]

resultados_df = analizar_multiples_textos(textos)
print(resultados_df)
#resultados_df.to_csv('resultados_analisis_sentimiento.csv', index=False)