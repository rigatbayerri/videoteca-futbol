import streamlit as st
from supabase import create_client

# --- CONFIGURACIÓ DE LA PÀGINA ---
st.set_page_config(
    page_title="Videoteca - C.F. Ginesta",
    page_icon="⚽",
    layout="centered"
)

# --- ESTIL I COLORS PERSONALITZATS ---
st.markdown("""
    <style>
    /* Fons general de l'aplicació */
    .stApp {
        background-color: #f7f5fa;
        color: #2b1b3d;
    }
    
    /* Textos generals visibles */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #2b1b3d !important;
    }
    
    /* Botons principals (lila amb lletra blanca) */
    .stButton>button, .stButton>button * {
        color: white !important;
        background-color: #5c2d73;
        border-radius: 8px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #4a2858;
    }
    
    /* --- SELECTOR DE PARTITS (Fons lila i lletres blanques) --- */
    div[data-baseweb="select"] > div {
        background-color: #5c2d73 !important;
        color: white !important;
        border-color: #4a2858 !important;
        border-radius: 8px;
    }
    
    /* Text interior del selectbox i icones */
    div[data-baseweb="select"] span, div[data-baseweb="select"] svg {
        color: white !important;
        fill: white !important;
    }
    
    /* Caixa de text de contrasenya */
    .stTextInput>div>div>input {
        color: #2b1b3d !important;
        border-color: #5c2d73;
    }
    </style>
""", unsafe_allow_html=True)

# --- CONFIGURACIÓ DE SUPABASE ---
SUPABASE_URL = "https://bufdixztdxrzyrdmueuk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJ1ZmRpeHp0ZHhyenlyZG11ZXVrIkwicm9sZSI6ImFub24iLCJpYXQiOjE3ODk1NTk5ODcsImV4cCI6MjEwNTEzNTk4N30.R_yj76u6ed3K0wr9_407Ti1vq2EvgoFJvs2veaRbBKg"

@st.cache_resource
def init_supabase():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

# --- SISTEMA DE CLAU D'ACCÉS (PRIVACITAT FAMILIARS) ---
CONTRASENYA_FAMILIARS = "ginesta2026"

def comprovar_acces():
    if "autoritzat" not in st.session_state:
        st.session_state["autoritzat"] = False

    if not st.session_state["autoritzat"]:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            try:
                st.image("logo.png", width=160)
            except:
                pass
                
        st.title("🔒 Accés Restringit")
        st.write("Espai privat per a les famílies del cadet F11 **C.F. Ginesta**. Introdueix la contrasenya:")
        
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
    # --- CAPÇALERA AMB EL LOGO DEL GINESTA ---
    col1, col2 = st.columns([1, 4])
    with col1:
        try:
            st.image("logo.png", width=100)
        except:
            st.write("⚽")
    with col2:
        st.title("Partits Cadet F11 C.F. Ginesta")
        st.markdown("*Partits de la temporada*")

    st.divider()

    # Obtenir dades de Supabase
    try:
        response = supabase.table("partits").select("*").order("data", desc=True).execute()
        partits = response.data
    except Exception as e:
        st.error(f"Error al connectar amb la base de dades: {e}")
        partits = []

    if not partits:
        st.info("Encara no hi ha partits pujats a la base de dades.")
        return

    # Menú desplegable de partits
    opcions_partits = {f"{p.get('data', '')} - {p.get('titol', 'Sense títol')} ({p.get('jornada', '')})": p for p in partits}
    
    partit_seleccionat_str = st.selectbox("Selecciona un partit per veure:", list(opcions_partits.keys()))
    partit_actual = opcions_partits[partit_seleccionat_str]

    st.divider()

    # Informació i Reproductor
    st.subheader(partit_actual.get('titol'))
    st.markdown(f"📅 **Data:** {partit_actual.get('data')} &nbsp;&nbsp;|&nbsp;&nbsp; 🏆 **Jornada:** {partit_actual.get('jornada')}")

    video_url = partit_actual.get('enllaç_video')
    if video_url:
        st.video(video_url)
    else:
        st.warning("El vídeo d'aquest partit encara no està disponible.")

# Executar control d'accés i app
if comprovar_acces():
    main()
