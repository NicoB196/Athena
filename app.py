from datetime import date
import streamlit as st

from ai import analyze_fitbit_screenshot
from database import create_database, save_run, get_last_three_runs, get_all_runs
from analysis import average_runs, compare_current_run, generate_summary

st.set_page_config(
    page_title="Athena",
    page_icon="🏃",
)

create_database()

st.sidebar.title("🏃 Athena")
page = st.sidebar.radio(
    "Navigation",
    ["🏠 Home", "📚 Läufe"]
)

if "show_form" not in st.session_state:
    st.session_state.show_form = False


if page == "🏠 Home":
    st.title("🏃 Athena")
    st.write("Willkommen 👋")
    st.write("## Dein persönlicher Laufcoach")
    st.info("Version 1.0.0: AI Laufcoach")

    st.divider()

    st.subheader("📸 Lauf per Screenshot")

    uploaded_file = st.file_uploader(
        "Fitbit-Screenshot auswählen",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        st.image(uploaded_file, use_container_width=True)

        if st.button("🤖 Screenshot auslesen"):
            with st.spinner("Athena liest deinen Screenshot..."):
                try:
                    data = analyze_fitbit_screenshot(uploaded_file)

                    st.session_state.ocr_kilometer = data["kilometer"] or 0.0
                    st.session_state.ocr_dauer = data["dauer"] or 0.0
                    st.session_state.ocr_pace = data["pace"] or ""
                    st.session_state.ocr_puls = int(data["puls"] or 0)
                    st.session_state.ocr_hoehenmeter = int(data["hoehenmeter"] or 0)
                    st.session_state.ocr_kalorien = int(data["kalorien"] or 0)
                    st.session_state.show_form = True

                    st.success("Screenshot erfolgreich ausgelesen ✅")
                    st.rerun()

                except Exception as error:
                    st.error(f"Fehler beim Auslesen: {error}")

    if st.button("➕ Neuen Lauf hinzufügen"):
        st.session_state.show_form = not st.session_state.show_form

    if st.session_state.show_form:
        with st.container(border=True):
            st.write("### Neuen Lauf eintragen")

            lauf_datum = st.date_input("Datum", value=date.today())

            strecke_km = st.number_input(
                "Strecke in km",
                min_value=0.0,
                step=0.1,
                value=float(st.session_state.get("ocr_kilometer", 0.0))
            )

            dauer_min = st.number_input(
                "Dauer in Minuten",
                min_value=0.0,
                step=1.0,
                value=float(st.session_state.get("ocr_dauer", 0.0))
            )

            pace = st.text_input(
                "Pace",
                value=st.session_state.get("ocr_pace", ""),
                placeholder="z.B. 7:02"
            )

            durchschnittspuls = st.number_input(
                "Durchschnittlicher Puls",
                min_value=0,
                step=1,
                value=int(st.session_state.get("ocr_puls", 0))
            )

            hoehenmeter = st.number_input(
                "Höhenmeter",
                min_value=0,
                step=1,
                value=int(st.session_state.get("ocr_hoehenmeter", 0))
            )

            kalorien = st.number_input(
                "Kalorien",
                min_value=0,
                step=1,
                value=int(st.session_state.get("ocr_kalorien", 0))
            )

            notiz = st.text_area(
                "Notiz",
                placeholder="z.B. gestern Tennis, 2 Bier, schlecht geschlafen..."
            )

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

                    for key in [
                        "ocr_kilometer",
                        "ocr_dauer",
                        "ocr_pace",
                        "ocr_puls",
                        "ocr_hoehenmeter",
                        "ocr_kalorien"
                    ]:
                        if key in st.session_state:
                            del st.session_state[key]

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

            st.write(f"📏 Strecke: {comparison['kilometer_diff']:+.2f} km")
            st.write(f"⏱ Dauer: {comparison['dauer_diff']:+.1f} Minuten")
            st.write(f"⛰ Höhenmeter: {comparison['hoehenmeter_diff']:+.0f} m")

        with st.container(border=True):
            st.write("### 🧠 Kurzfazit")
            st.write(summary)

    else:
        st.info("Für die Coach-Analyse brauchst du mindestens 3 gespeicherte Läufe.")


if page == "📚 Läufe":
    st.title("📚 Alle Läufe")

    runs = get_all_runs()

    if runs:
        for run in runs:
            datum, kilometer, dauer, pace, puls, hoehenmeter, kalorien, notiz = run

            with st.container(border=True):
                st.subheader(f"🏃 Lauf vom {datum}")

                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"📏 Strecke: {kilometer} km")
                    st.write(f"⏱ Dauer: {dauer} Minuten")
                    st.write(f"⚡ Pace: {pace} min/km")

                with col2:
                    st.write(f"❤️ Ø Puls: {puls} bpm")
                    st.write(f"⛰ Höhenmeter: {hoehenmeter} m")
                    st.write(f"🔥 Kalorien: {kalorien} kcal")

                if notiz:
                    st.write(f"📝 {notiz}")
    else:
        st.info("Noch keine Läufe gespeichert.")