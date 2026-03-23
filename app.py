import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Edytor Excel", layout="wide")

# --- 1. INICJALIZACJA STANU ---
if 'df_editor' not in st.session_state:
    st.session_state.df_editor = None
if 'file_id' not in st.session_state:
    st.session_state.file_id = None

st.title("📂 Edytor z automatycznym odświeżaniem")

# --- 2. WCZYTYWANIE ---
uploaded_file = st.file_uploader("Wgraj plik Excel", type=["xlsx"])

if uploaded_file:
    # SPRAWDZAMY CZY TO NOWY PLIK (porównujemy nazwę i rozmiar jako unikalne ID)
    current_file_id = f"{uploaded_file.name}_{uploaded_file.size}"
    
    if st.session_state.file_id != current_file_id:
        # Jeśli ID jest inne -> ładujemy nowe dane i aktualizujemy ID
        st.session_state.df_editor = pd.read_excel(uploaded_file)
        st.session_state.file_id = current_file_id
        st.session_state.original_filename = uploaded_file.name
        # Wymuszamy odświeżenie interfejsu
        st.rerun()

# --- 3. WYŚWIETLANIE EDYTORA ---
if st.session_state.df_editor is not None:
    # Używamy file_id jako części klucza widgetu, aby wymusić jego reset przy nowym pliku
    edited_df = st.data_editor(
        st.session_state.df_editor,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key=f"editor_{st.session_state.file_id}" 
    )

    # --- 4. EKSPORT ---
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    processed_data = to_excel(edited_df)

    st.divider()
    
    st.download_button(
        label=f"💾 Zapisz jako: {st.session_state.original_filename}",
        data=processed_data,
        file_name=st.session_state.original_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    if st.button("Usuń i wyczyść wszystko"):
        st.session_state.df_editor = None
        st.session_state.file_id = None
        st.rerun()
else:
    st.info("Wgraj plik Excel (.xlsx), aby rozpocząć pracę.")
