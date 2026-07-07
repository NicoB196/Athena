from datetime import date
import streamlit as st

from ocr import extract_run_data

from database import create_database, save_run, get_last_three_runs
from analysis import average_runs, compare_current_run, generate_summary

st.set_page_config(
    page_title="Athena",
    page_icon="🏃",
)

create_database()

st.title("🏃 Athena")
st.write("Willkommen Nico 👋")
st.write("## Dein persönlicher Laufcoach")
st.info("Version 0.4.0: Läufe manuell erfassen")

st.divider()

if "show_form" not in st.session_state:
    st.session_state.show_form = False

st.subheader("📸 Lauf per Screenshot")

uploaded_file = st.file_uploader(
    "Fitbit-Screenshot auswählen",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    st.image(uploaded_file, use_container_width=True)

    data = extract_run_data(uploaded_file)

    st.success("Screenshot erfolgreich gelesen ✅")

    st.write("### Erkannte Werte")
    st.write(f"📏 Strecke: {data['kilometer']} km")
    st.write(f"⏱ Dauer: {data['dauer']} Minuten")
    st.write(f"⚡ Pace: {data['pace']} min/km")
    st.write(f"❤️ Puls: {data['puls']} bpm")
    st.write(f"🔥 Kalorien: {data['kalorien']} kcal")

    with st.expander("OCR-Rohtext anzeigen"):
        st.code(data["raw_text"])

    st.success("Screenshot erfolgreich geladen ✅")

if st.button("➕ Neuen Lauf hinzufügen"):
    st.session_state.show_form = not st.session_state.show_form

if st.session_state.show_form:
    with st.container(border=True):
        st.write("### Neuen Lauf eintragen")

        lauf_datum = st.date_input("Datum", value=date.today())
        strecke_km = st.number_input("Strecke in km", min_value=0.0, step=0.1)
        dauer_min = st.number_input("Dauer in Minuten", min_value=0.0, step=1.0)
        pace = st.text_input("Pace", placeholder="z.B. 7:02")
        durchschnittspuls = st.number_input("Durchschnittlicher Puls", min_value=0, step=1)
        hoehenmeter = st.number_input("Höhenmeter", min_value=0, step=1)
        kalorien = st.number_input("Kalorien", min_value=0, step=1)
        notiz = st.text_area("Notiz", placeholder="z.B. gestern Tennis, 2 Bier, schlecht geschlafen...")

if st.button("Lauf speichern"):
    if ":" not in pace:
        st.error("Bitte Pace im Format 7:02 eingeben.")
    else:
        save_run(
            lauf_datum.strftime("%d.%m.%Y"),
            strecke_km,
            dauer_min,
            pace,
            durchschnittspuls,
            hoehenmeter,
            kalorien,
            notiz
        )

        st.success("Lauf wurde gespeichert ✅")
        st.session_state.show_form = False
        st.rerun()


st.divider()

st.subheader("🤖 Coach")

last_three_runs = get_last_three_runs()

if len(last_three_runs) >= 3:
    averages = average_runs(last_three_runs)
    current_run = last_three_runs[0]
    comparison = compare_current_run(current_run, averages)
    summary = generate_summary(comparison)

    with st.container(border=True):
        st.write("### 📊 Vergleich zum Durchschnitt der letzten 3 Läufe")

        pace_diff = comparison["pace_diff"]

        if pace_diff is not None:
            if pace_diff < -3:
                st.success(f"⚡ Pace: {abs(pace_diff):.0f} Sek./km schneller")
            elif pace_diff > 3:
                st.error(f"⚡ Pace: {pace_diff:.0f} Sek./km langsamer")
            else:
                st.info("⚡ Pace: nahezu unverändert")
        else:
            st.warning("⚡ Pace: Keine gültige Pace")

        puls_diff = comparison["puls_diff"]
        if puls_diff < -2:
            st.success(f"❤️ Puls: {abs(puls_diff):.0f} bpm niedriger")
        elif puls_diff > 2:
            st.warning(f"❤️ Puls: {puls_diff:.0f} bpm höher")
        else:
            st.info("❤️ Puls: nahezu unverändert")

        km_diff = comparison["kilometer_diff"]
        st.write(f"📏 Strecke: {km_diff:+.2f} km")

        dauer_diff = comparison["dauer_diff"]
        st.write(f"⏱ Dauer: {dauer_diff:+.1f} Minuten")

        hm_diff = comparison["hoehenmeter_diff"]
        st.write(f"⛰ Höhenmeter: {hm_diff:+.0f} m")

    with st.container(border=True):
        st.write("### 🧠 Kurzfazit")
        st.write(summary)

else:
    st.info("Für die Coach-Analyse brauchst du mindestens 3 gespeicherte Läufe.")