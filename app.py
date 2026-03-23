import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Edytor Excel", layout="wide")

# --- 1. INICJALIZACJA STANU ---
if 'df_editor' not in st.session_state:
    st.session_state.df_editor = None
if 'original_filename' not in st.session_state:
    st.session_state.original_filename = "nowy_arkusz.xlsx"

st.title("📂 Edytor z zachowaniem nazwy")

# --- 2. WCZYTYWANIE ---
uploaded_file = st.file_uploader("Wgraj plik", type=["xlsx"])

if uploaded_file:
    # Zapamiętujemy nazwę tylko raz przy wgraniu
    st.session_state.original_filename = uploaded_file.name
    # Wczytujemy dane tylko jeśli jeszcze ich nie ma w sesji (żeby edycja nie znikała)
    if st.session_state.df_editor is None:
        st.session_state.df_editor = pd.read_excel(uploaded_file)

# --- 3. EDYCJA ---
if st.session_state.df_editor is not None:
    edited_df = st.data_editor(
        st.session_state.df_editor,
        num_rows="dynamic",
        use_container_width=True,
        hide_index=True,
        key="editor"
    )

    # --- 4. EKSPORT ---
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    processed_data = to_excel(edited_df)

    st.divider()
    
    # Przycisk pobierania z oryginalną nazwą
    st.download_button(
        label=f"💾 Zapisz jako: {st.session_state.original_filename}",
        data=processed_data,
        file_name=st.session_state.original_filename, # To wymusza nazwę w okienku zapisu
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    if st.button("Usuń wszystko i zacznij od nowa"):
        st.session_state.df_editor = None
        st.rerun()
else:
    st.info("Wgraj plik Excel, aby rozpocząć edycję.")
