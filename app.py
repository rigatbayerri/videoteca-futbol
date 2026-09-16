import streamlit as st
from supabase import create_client

# --- CONFIGURACIÓ DE LA PÀGINA ---
st.set_page_config(
    page_title="Videoteca - Futbol Base",
    page_icon="⚽",
    layout="centered"
)

# --- CONFIGURACIÓ DE SUPABASE ---
SUPABASE_URL = "https://bufdixztdxrzyrdmueuk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ1ZmRpeHp0ZHhyenlyZG11ZXVrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODk1NTk5ODcsImV4cCI6MjEwNTEzNTk4N30.R_yj76u6ed3K0wr9_407Ti1vq2EvgoFJvs2veaRbBKg"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# --- SISTEMA DE CLAU D'ACCÉS (PRIVACITAT FAMILIARS) ---
CONTRASENYA_FAMILIARS = "manresa2026"

def comprovar_acces():
    if "autoritzat" not in st.session_state:
        st.session_state["autoritzat"] = False

    if not st.session_state["autoritzat"]:
        st.title("🔒 Accés Restringit - Videoteca de l'Equip")
        st.write("Aquest espai és privat per a les famílies. Introdueix la contrasenya per veure els partits.")
        
        password_input = st.text_input("Contrasenya:", type="password")
        if st.button("Entrar"):
            if password_input == CONTRASENYA_FAMILIARS:
                st.session_state["autoritzat"] = True
                st.rerun()
            else:
                st.error("Contrasenya incorrecta. Torna-ho a provar.")
        return False
    return True

# --- APLICACIÓ PRINCIPAL ---
def main():
    st.title("⚽ Videoteca Oficial - Partits")
    st.write("Espai privat per consultar i reproduir tots els partits de la temporada.")

    # Obtenir dades de Supabase
    try:
        response = supabase.table("partits").select("*").order("data", desc=True).execute()
        partits = response.data
    except Exception as e:
        st.error(f"Error al connectar amb la base de dades: {e}")
        partits = []

    if not partits:
        st.info("Encara no hi ha partits pujats a la base de dades o no s'ha trobat cap fila.")
        return

    # Crear una llista de títols per al menú desplegable
    opcions_partits = {f"{p.get('data', '')} - {p.get('titol', 'Sense títol')} ({p.get('jornada', '')})": p for p in partits}
    
    partit_seleccionat_str = st.selectbox("Selecciona un partit:", list(opcions_partits.keys()))
    partit_actual = opcions_partits[partit_seleccionat_str]

    st.divider()

    # Informació del partit
    st.subheader(partit_actual.get('titol'))
    st.markdown(f"**Data:** {partit_actual.get('data')} | **Jornada:** {partit_actual.get('jornada')}")

    # Reproductor de vídeo
    video_url = partit_actual.get('enllaç_video')
    if video_url:
        st.video(video_url)
    else:
        st.warning("El vídeo d'aquest partit encara no està disponible.")

# Executar control d'accés i app
if comprovar_acces():
    main()
