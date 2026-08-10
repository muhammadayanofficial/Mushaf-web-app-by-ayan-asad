import streamlit as st
import requests


# PAGE SETTINGS
st.set_page_config(
    page_title="Mushaf",
    page_icon="📖",
    layout="centered"
)


# TITLE
st.title("📖 Mushaf")
st.write("Read • Listen • Understand")


# SURAH API
mera_surahs_data = requests.get(
    "https://api.alquran.cloud/v1/surah"
)

surahs = mera_surahs_data.json()["data"]


# SURAH OPTIONS
options = []

for s in surahs:
    options.append(
        f'{s["number"]} | {s["name"]}'
    )


# RECITERS
reciters = {
    "Abdur Rahmaan As-Sudais": "ar.abdurrahmaansudais",
    "Mishary Rashid Alafasy": "ar.alafasy",
    "Abdullah Basfar": "ar.abdullahbasfar"
}


# TRANSLATIONS
translations = {
    "English": "en.sahih",
    "Urdu": "ur.jalandhry",
    "French": "fr.hamidullah"
}


# THREE COLUMN LAYOUT
col1, col2, col3 = st.columns(3)


with col1:
    selected_surah = st.selectbox(
        "📖 Choose Surah",
        options
    )


with col2:
    selected_reciter = st.selectbox(
        "🎙️ Choose Reciter",
        list(reciters.keys())
    )


with col3:
    selected_language = st.selectbox(
        "🌍 Choose Translation",
        list(translations.keys())
    )


# IDS
surah_number = selected_surah.split(" | ")[0]

reciter_id = reciters[selected_reciter]

translation_id = translations[selected_language]


# ARABIC + AUDIO
ayahs = requests.get(
    f"https://api.alquran.cloud/v1/surah/{surah_number}/{reciter_id}"
)

ayahs_data = ayahs.json()["data"]["ayahs"]


# TRANSLATION
translation = requests.get(
    f"https://api.alquran.cloud/v1/surah/{surah_number}/{translation_id}"
)

translation_data = translation.json()["data"]["ayahs"]


# SURAH HEADING
st.divider()

st.header(selected_surah)


# AYAH DISPLAY
for a, t in zip(ayahs_data, translation_data):

    with st.container():

        st.subheader(
            f"Ayah {a['numberInSurah']}"
        )

        st.write(a["text"])

        st.write(t["text"])

        st.audio(a["audio"])

    st.divider()