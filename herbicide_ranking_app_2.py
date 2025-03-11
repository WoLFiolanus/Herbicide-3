import pandas as pd
import streamlit as st

# Φόρτωση δεδομένων από Excel
@st.cache_data  # Μπορεί να αφαιρεθεί αν προκαλεί πρόβλημα
def load_data():
    try:
        path_vineyard = "ΦΥΣΙΚΟΧΗΜΙΚΑ_ΖΙΖΑΝΙΟΚΤΟΝΑ_ΑΜΠΕΛΙ.xlsx"
        path_peach = "ΦΥΣΙΚΟΧΗΜΙΚΑ_ΖΙΖΑΝΙΟΚΤΟΝΑ_ΡΟΔΑΚΙΝΑ.xlsx"
        df_vineyard = pd.read_excel(path_vineyard)
        df_peach = pd.read_excel(path_peach)
        return df_vineyard, df_peach
    except Exception as e:
        st.error(f"Σφάλμα κατά τη φόρτωση των δεδομένων: {e}")
        return None, None

df_vineyard, df_peach = load_data()

if df_vineyard is None or df_peach is None:
    st.stop()

# Συνδυασμός δεδομένων
all_herbicides = pd.concat([df_vineyard, df_peach])
if "Δραστική Ουσία1" not in all_herbicides.columns:
    st.error("Η στήλη 'Δραστική Ουσία1' δεν βρέθηκε στα δεδομένα.")
    st.stop()

herbicide_names = all_herbicides["Δραστική Ουσία1"].dropna().unique()

# Streamlit App
st.title("Herbicide Ranking System")
st.write("Επιλέξτε καλλιέργεια και ζιζανιοκτόνο για να δείτε τις λεπτομέρειες.")

# Επιλογή καλλιέργειας
crop = st.selectbox("Επιλέξτε καλλιέργεια:", ["Αμπέλι", "Ροδακινιά"])

# Επιλογή ζιζανιοκτόνου
selected_herbicide = st.selectbox("Επιλέξτε ζιζανιοκτόνο:", herbicide_names)

# Input για φυσική θέση καλλιέργειας (επικινδυνότητα μόλυνσης υδάτων)
water_proximity = st.slider("Εγγύτητα σε όγκους υδάτων (0: Μακριά, 1: Πολύ κοντά)", 0.0, 1.0, 0.5)

# Φιλτράρισμα δεδομένων για το επιλεγμένο ζιζανιοκτόνο
herbicide_data = all_herbicides[all_herbicides["Δραστική Ουσία1"] == selected_herbicide]

if not herbicide_data.empty:
    st.write(f"### Πληροφορίες για το {selected_herbicide}")
    st.dataframe(herbicide_data)
    
    # Έλεγχος αν υπάρχουν οι στήλες πριν τη χρήση τους
    pollution_index = herbicide_data["Pollution Index"].values[0] if "Pollution Index" in herbicide_data.columns else 0
    resistance_index = herbicide_data["Resistance Index"].values[0] if "Resistance Index" in herbicide_data.columns else 0
    
    herbicide_score = pollution_index + resistance_index + water_proximity
    st.write(f"### Herbicide Score: {herbicide_score:.2f}")
else:
    st.write("Δεν βρέθηκαν δεδομένα για το επιλεγμένο ζιζανιοκτόνο.")

st.stop()
