import streamlit as st
from database import get_all_runs

st.set_page_config(
    page_title="Alle Läufe",
    page_icon="📚"
)

st.title("📚 Alle Läufe")

runs = get_all_runs()

if runs:
    for run in runs:
        datum, kilometer, dauer, pace, puls, hoehenmeter, kalorien, notiz = run

        with st.container(border=True):
            st.subheader(f"🏃 {datum}")

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"📏 {kilometer} km")
                st.write(f"⏱ {dauer} Minuten")
                st.write(f"⚡ {pace}")

            with col2:
                st.write(f"❤️ {puls} bpm")
                st.write(f"⛰ {hoehenmeter} m")
                st.write(f"🔥 {kalorien} kcal")

            if notiz:
                st.write(f"📝 {notiz}")
else:
    st.info("Noch keine Läufe vorhanden.")