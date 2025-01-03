import pandas as pd

# Bestandspad
file_path = "totaledata.ods"

# Functie om seizoen te bepalen
def determine_season(date):
    if pd.isna(date):
        return None
    maand = date.month
    dag = date.day
    if (maand == 12 and dag >= 21) or maand in [1, 2] or (maand == 3 and dag < 20):
        return "Winter"
    elif (maand == 3 and dag >= 20) or maand in [4, 5] or (maand == 6 and dag < 21):
        return "Lente"
    elif (maand == 6 and dag >= 21) or maand in [7, 8] or (maand == 9 and dag < 23):
        return "Zomer"
    elif (maand == 9 and dag >= 23) or maand in [10, 11] or (maand == 12 and dag < 21):
        return "Herfst"
    else:
        return None

try:
    # Probeer het bestand te lezen
    print("Probeer het bestand te lezen...")
    data = pd.read_excel(file_path, engine="odf")
    print("Bestand succesvol gelezen.")
except Exception as e:
    print("Fout bij lezen van bestand:", e)
    exit()

# Debug: Bekijk de kolommen in het bestand
print("Beschikbare kolommen:", data.columns)

# Controleer of de datumkolom aanwezig is
if "validfrom (UTC)" not in data.columns:
    raise ValueError("De kolom 'validfrom (UTC)' ontbreekt in het bestand. Controleer de naam of inhoud.")

# Zorg ervoor dat de datumkolom als datetime wordt gelezen
data['validfrom (UTC)'] = pd.to_datetime(data['validfrom (UTC)'], errors='coerce')

# Voeg een kolom toe met de Nederlandse maandnaam
data['Month'] = data['validfrom (UTC)'].dt.strftime('%B')

# Voeg een kolom toe met het jaar
data['Year'] = data['validfrom (UTC)'].dt.year

# Voeg een kolom toe met het seizoen
data['Season'] = data['validfrom (UTC)'].apply(determine_season)

# Selecteer de relevante kolommen om op te slaan (inclusief 'validto' als deze aanwezig is)
output_columns = data.columns  # Ensure all columns, including 'validto', are preserved
output_path = "output_with_month_year_and_season.ods"

try:
    print("Probeer het bewerkte bestand op te slaan...")
    # Opslaan naar het nieuwe bestand
    data.to_excel(output_path, engine="odf", index=False, columns=output_columns)
    print(f"Het bewerkte bestand is succesvol opgeslagen als: {output_path}")
except Exception as e:
    print("Fout bij opslaan van bestand:", e)
