import pandas as pd

# Essayer avec l'encodage ISO-8859-1 (latin1)
df = pd.read_csv('reponse.csv', encoding='ISO-8859-1')

# Afficher le DataFrame
print(df)