import streamlit as st
import pandas as pd
from io import BytesIO

# 1. Konfiguracja strony
st.set_page_config(page_title="Edytor Excel PRO", layout="wide", page_icon="📊")

st.title("📊 Interaktywny Edytor Arkuszy Excel")
st.markdown("""
Ta aplikacja pozwala na:
1. **Wczytanie** istniejącego pliku Excel.
2. **Edycję** danych (dodawanie wierszy, zmianę wartości).
3. **Pobranie** poprawionego pliku na dysk.
""")

# --- 2. LOGIKA WCZYTYWANIA DANYCH ---

# Inicjalizacja stanu sesji, aby dane nie znikały
if 'df_editor' not in st.session_state:
    # Dane startowe, jeśli nic nie wgrano
    st.session_state.df_editor = pd.DataFrame({
        "Produkt": ["Przykład 1", "Przykład 2"],
        "Cena": [100, 200],
        "Ilość": [10, 5]
    })

# Widget do wgrywania pliku
uploaded_file = st.file_uploader("Wybierz plik Excel (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    try:
        # Wczytujemy plik i zapisujemy go do stanu sesji
        file_df = pd.read_excel(uploaded_file)
        st.session_state.df_editor = file_df
        st.success("Pomyślnie wczytano plik!")
    except Exception as e:
        st.error(f"Błąd podczas wczytywania pliku: {e}")

# --- 3. INTERAKTYWNY EDYTOR ---

st.subheader("📝 Edytuj dane poniżej:")

# Główny edytor danych
# Zmiany są automatycznie zapisywane do zmiennej 'edited_df'
edited_df = st.data_editor(
    st.session_state.df_editor,
    num_rows="dynamic",  # Pozwala dodawać i usuwać wiersze (ikona kosza i '+')
    use_container_width=True,
    hide_index=True,
    key="main_editor"
)

# --- 4. EKSPORT I POBIERANIE ---

def to_excel(df):
    """Konwertuje DataFrame do bajtów pliku Excel."""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Dane_z_Edytora')
    return output.getvalue()

st.divider()
col1, col2 = st.columns([1, 4])

with col1:
    # Przygotowanie danych do pobrania
    excel_data = to_excel(edited_df)
    
    st.download_button(
        label="📥 Pobierz jako Excel",
        data=excel_data,
        file_name="zaktualizowane_dane.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="Kliknij, aby zapisać wprowadzone zmiany do nowego pliku."
    )

with col2:
    if st.button("Wyczyść i zacznij od nowa"):
        del st.session_state.df_editor
        st.rerun()

# --- 5. PODGLĄD (OPCJONALNIE) ---
with st.expander("Zobacz podgląd techniczny (Pandas DataFrame)"):
    st.write(edited_df)
