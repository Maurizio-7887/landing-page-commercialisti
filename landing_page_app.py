import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from PIL import Image

# --- Configurazione Pagina ---
st.set_page_config(
    page_title="Consorzio IDS | Python per Commercialisti",
    page_icon="🐍",
    layout="centered"
)

# --- Autenticazione con Google Sheets ---
# Quando sarai pronto, rimuovi i '#' da questo blocco per attivare la connessione
try:
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = {
        "type": st.secrets["gcp_service_account"]["type"],
        "project_id": st.secrets["gcp_service_account"]["project_id"],
        "private_key_id": st.secrets["gcp_service_account"]["private_key_id"],
        "private_key": st.secrets["gcp_service_account"]["private_key"].replace('\\n', '\n'),
        "client_email": st.secrets["gcp_service_account"]["client_email"],
        "client_id": st.secrets["gcp_service_account"]["client_id"],
        "auth_uri": st.secrets["gcp_service_account"]["auth_uri"],
        "token_uri": st.secrets["gcp_service_account"]["token_uri"],
        "auth_provider_x509_cert_url": st.secrets["gcp_service_account"]["auth_provider_x509_cert_url"],
        "client_x509_cert_url": st.secrets["gcp_service_account"]["client_x509_cert_url"]
    }
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    # RICORDATI DI CAMBIARE IL NOME DEL FOGLIO QUI SOTTO
    sheet = client.open("Leads Landing Page Commercialisti").sheet1 
except Exception as e:
    # Questo messaggio apparirà solo se la connessione fallisce
    st.error("⚠️ Errore di connessione al database. Controlla le credenziali e il nome del foglio.")
    # st.stop() # Commentato per permettere la visualizzazione anche senza connessione


# --- LAYOUT DELLA LANDING PAGE ---

# Immagine Banner Principale
try:
    image = Image.open('consorzio_ids_banner.jpg')
    st.image(image, use_container_width=True)
except FileNotFoundError:
    st.warning("Immagine 'consorzio_ids_banner.jpg' non trovata. Assicurati che sia nella stessa cartella dello script.")

st.title("Commercialista: Automatizza la tua Business Intelligence")
st.header("Basta ore perse su Power BI. Ottieni script Python su misura.")

st.markdown("""
**Il tuo tempo è prezioso.** Invece di passarlo a creare dashboard complesse e a ricordare comandi, puoi ottenere report automatici e analisi precise con soluzioni create per te.

**Consorzio IDS** sviluppa script Python personalizzati che:
- **Si collegano** ai tuoi dati (gestionali, file Excel, etc.).
- **Elaborano** le informazioni in pochi secondi.
- **Producono** report chiari e pronti da condividere con i tuoi clienti.

Dedica più tempo alla consulenza strategica, non alla programmazione.
""")

st.markdown("---")

# --- FORM DI RICHIESTA INFORMAZIONI ---
with st.form(key="contact_form", clear_on_submit=True):
    st.subheader("Scopri di più con una consulenza gratuita")
    
    nome_cognome = st.text_input(
        "Nome e Cognome",
        placeholder="Es. Mario Rossi"
    )
    
    email_studio = st.text_input(
        "Email dello Studio",
        placeholder="Es. info@studiorossi.it"
    )
    
    esigenza = st.text_area(
        "Quale attività vorresti automatizzare?",
        placeholder="Es. Analisi mensile del fatturato per cliente, controllo scadenze F24, report di bilancio automatico..."
    )
    
    # CAMPO AGGIUNTO
    numero_cellulare = st.text_input(
        "Numero di Cellulare (per WhatsApp)",
        placeholder="Es. 3331234567"
    )
    
    consenso_whatsapp = st.checkbox(
        "Autorizzo a essere contattato via WhatsApp per una consulenza rapida."
    )
    
    submit_button = st.form_submit_button(
        label="Richiedi Consulenza Gratuita"
    )

# --- LOGICA DI INVIO DEL FORM ---
if submit_button:
    # LOGICA DI VALIDAZIONE MIGLIORATA
    form_valido = True
    if not (nome_cognome and "@" in email_studio and esigenza):
        st.warning("Per favore, compila i campi Nome, Email ed Esigenza.")
        form_valido = False

    if consenso_whatsapp and not numero_cellulare:
        st.warning("Per favore, inserisci il numero di cellulare se autorizzi il contatto via WhatsApp.")
        form_valido = False
        
    if form_valido:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        consenso_ws_text = "Sì" if consenso_whatsapp else "No"
        
        # LOGICA DI SALVATAGGIO AGGIORNATA
        nuova_riga = [timestamp, nome_cognome, email_studio, numero_cellulare, esigenza, consenso_ws_text]
        
        try:
            sheet.append_row(nuova_riga)
            st.success(f"Grazie, {nome_cognome.split(' ')[0]}! Un nostro specialista ti contatterà al più presto.")
            st.balloons()
        except NameError:
             st.warning("MODALITÀ ANTEPRIMA: I dati non sono stati salvati. Attiva la connessione a Google Sheets.")
        except Exception as e:
            st.error(f"Qualcosa è andato storto durante il salvataggio: {e}")

st.markdown("---")

st.markdown("<p style='text-align: center; color: grey;'>La tua privacy è la nostra priorità. I tuoi dati saranno usati solo per ricontattarti.</p>", unsafe_allow_html=True)
