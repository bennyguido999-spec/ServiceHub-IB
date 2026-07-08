import streamlit as st
import pandas as pd
import plotly.express as px
import io
from fpdf import FPDF
from datetime import datetime
import os 
import matplotlib.pyplot as plt
import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).parent / "servicehub.db"
# Configurazione della pagina
st.set_page_config(
    page_title="ServiceHub BI",
    page_icon="📊",
    layout="wide"
)
st.sidebar.title("📊 ServiceHub BI")
st.sidebar.markdown("---")

st.sidebar.info("""
Dashboard dimostrativa sviluppata come Project Work.

**Tema:** Digitalizzazione dell'impresa
**Ambito:** Startup digitale di servizi on-demand
**Versione:** 1.0 - Giugno 2026
""")

st.sidebar.markdown("---")

st.sidebar.write("🏛 **Università Telematica Pegaso**")
st.sidebar.write("🎓 **Corso di Laurea:** L-31 ")
st.sidebar.write("👤 **Autore:** Benny Benigno Guido")
st.sidebar.write("🆔 **Matricola:** 0312200934")
st.sidebar.markdown("---")

st.sidebar.markdown("---")
# Titolo
st.title("📊 ServiceHub BI")

data_aggiornamento = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
st.caption(f"🕒 Ultimo aggiornamento dati: {data_aggiornamento}")

st.caption ("sistema di business Intelligence per stratup di servizi on-demand")
st.info("""
### 📈 Dashboard di Business Intelligence

Questa dashboard consente di monitorare le prestazioni della startup **ServiceHub**, analizzando:

- 📌 richieste dei servizi
- 💰 fatturato generato
- ⭐ valutazioni degli utenti
- 📊 indicatori strategici (KPI)

Le informazioni sono organizzate in modo da supportare il processo decisionale aziendale attraverso una rappresentazione chiara e immediata dei dati.
""")
st.markdown("---")

st.header("Benvenuto")

st.write("""
Questa piattaforma è stata sviluppata come progetto di Business Intelligence
per una startup digitale di servizi on-demand.

L'obiettivo del sistema è raccogliere, organizzare e analizzare i dati
generati dalla piattaforma ServiceHub, fornendo al gestore strumenti
di supporto alle decisioni aziendali.
""")

st.info("Versione 1.0 - Ambiente di sviluppo configurato correttamente")

st.markdown("---")

st.subheader("Stato del progetto")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Database", "In progettazione")

with col2:
    st.metric("Dataset", "Da creare")

with col3:
    st.metric("Dashboard", "In sviluppo")

st.markdown("---")

st.subheader("Dataset iniziale dei servizi")

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    s.nome AS Servizio,
    COUNT(r.id_richiesta) AS Richieste,
    ROUND(AVG(r.valutazione), 1) AS "Valutazione media",
    SUM(r.importo) AS "Fatturato (€)"   
FROM richieste r
JOIN servizi s ON r.id_servizio = s.id_servizio
WHERE r.stato = 'Completata'
GROUP BY s.nome
ORDER BY Richieste DESC
"""

classifica_servizi = pd.read_sql_query(query, conn)

conn.close()
conn = sqlite3.connect(DB_PATH)

query_dettaglio = """
SELECT
    r.id_richiesta,
    c.nome AS Cliente,
    c.zona AS Zona_cliente,
    c.data_iscrizione,
    c.tipo_cliente,
    c.fascia_eta,
    c.comune,
    c.fidelizzato,
    f.nome AS Fornitore,
    f.zona AS Zona_fornitore,
    s.nome AS Servizio,
    t.data AS Data_richiesta,
    t.mese AS Mese,
    t.anno AS Anno,
    t.giorno_settimana,
    r.importo,
    r.valutazione,
    r.stato,
    r.tempo_erogazione_min
FROM richieste r
JOIN clienti c ON r.id_cliente = c.id_cliente
JOIN fornitori f ON r.id_fornitore = f.id_fornitore
JOIN servizi s ON r.id_servizio = s.id_servizio
JOIN tempo t ON r.id_tempo = t.id_tempo
WHERE r.stato = 'Completata'
"""

dettaglio_richieste = pd.read_sql_query(query_dettaglio, conn)

conn.close()

st.markdown("---")
st.subheader("🗃️ Struttura dati e modello a stella")

st.info("""
Il database del prototipo è organizzato secondo una struttura a stella.

La tabella centrale è **richieste**, che contiene i dati operativi principali.
Attorno ad essa sono collegate le tabelle dimensionali: **clienti**, **fornitori**, **servizi** e **tempo**.
""")

st.markdown("""
**Fact table**
- `richieste`: contiene richieste, importi, valutazioni e stato del servizio.

**Dimension table**
- `clienti`: anagrafica clienti, zona e data di iscrizione.
- `fornitori`: operatori/partner, servizio offerto, zona e valutazione.
- `servizi`: elenco delle categorie di servizio.
- `tempo`: data, mese, anno e giorno della settimana.
""")


st.sidebar.markdown("---")

servizio_selezionato = st.sidebar.selectbox(
"🔎 Seleziona un servizio",
["Tutti"] + list(classifica_servizi["Servizio"])
)

if servizio_selezionato == "Tutti":
    dati_filtrati = classifica_servizi
else:
    dati_filtrati = classifica_servizi[
    classifica_servizi["Servizio"] == servizio_selezionato
]
totale_richieste = dati_filtrati["Richieste"].sum()
fatturato_totale = dati_filtrati["Fatturato (€)"].sum()
valutazione_media = dati_filtrati["Valutazione media"].mean()
st.subheader("📊 Distribuzione delle richieste")

grafico = {
"Idraulico": 120,
"Giardiniere": 95,
"Pulizie": 150,
"Elettricista": 80,
"Baby sitter": 60
}

st.bar_chart(grafico)
st.markdown("---")

st.subheader("📋 Riepilogo servizi")

for servizio, richieste in grafico.items():
    st.write(f"✅ {servizio}: **{richieste} richieste**")


st.markdown("---")

st.subheader("🥧 Ripartizione delle richieste")

df = pd.DataFrame({
"Servizio": list(grafico.keys()),
"Richieste": list(grafico.values())
})

fig = px.pie(
df,
values="Richieste",
names="Servizio",
title="Distribuzione dei servizi richiesti"
)

st.markdown("---")
st.subheader("💰 Indicatori economici")
fatturato_totale = dati_filtrati["Fatturato (€)"].sum()
valutazione_media = dati_filtrati["Valutazione media"].mean()
col1, col2 = st.columns(2)

with col1:
    st.metric("Fatturato totale stimato", f"€ {fatturato_totale:,.0f}")
with col2:
    st.metric("Valutazione media generale", f"{valutazione_media:.2f} / 5")
st.markdown("---")

st.subheader("📊 Classifica dei servizi più richiesti")
df_servizi = classifica_servizi

classifica_servizi = df_servizi.sort_values(
by="Richieste",
ascending=False
)

st.markdown("---")

st.subheader("📈 Richieste per servizio")

fig_barre = px.bar(
classifica_servizi,
x="Servizio",
y="Richieste",
color="Richieste",
text="Richieste",
title="Numero di richieste per servizio"
)
st.dataframe(
classifica_servizi,
use_container_width=True
)
st.markdown("---")

st.subheader("📈 Richieste per servizio")

fig_barre = px.bar(
classifica_servizi,
x="Servizio",
y="Richieste",
color="Richieste",
text="Richieste",
title="Numero di richieste per servizio"
)
fig_barre.update_layout(height=400)

st.plotly_chart(fig_barre, use_container_width=True)
st.markdown("---")

st.subheader("📅 Andamento mensile delle richieste")
dati_mensili = pd.DataFrame({
"Mese": ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno"],
"Richieste": [65, 80, 95, 110, 130, 150]
})

fig_linea = px.line(
dati_mensili,
x="Mese",
y="Richieste",
markers=True,
title="Evoluzione delle richieste nel semestre"
)

st.plotly_chart(fig_linea, use_container_width=True)
st.markdown("---")

st.subheader("💶 Fatturato per servizio")

fig_fatturato = px.bar(
classifica_servizi,
x="Servizio",
y="Fatturato (€)",
color="Fatturato (€)",
text="Fatturato (€)",
title="Fatturato stimato generato da ciascun servizio"
)

fig_fatturato.update_layout(height=400)
st.plotly_chart(fig_fatturato, use_container_width=True)
st.markdown("---")
st.markdown("---")

# ===== PROFILO CLIENTELA =====

st.subheader("👥 Profilo della clientela")

col1, col2 = st.columns(2)

with col1:
    comuni = dettaglio_richieste.groupby("comune").size().reset_index(name="Clienti")

    fig_comuni = px.bar(
    comuni,
        x="comune",
        y="Clienti",
        color="Clienti",
        title="Provenienza della clientela"
    )

    st.plotly_chart(fig_comuni, use_container_width=True)

with col2:
    tipo = dettaglio_richieste.groupby("tipo_cliente").size().reset_index(name="Numero")

    fig_tipo = px.pie(
        tipo,
        names="tipo_cliente",
        values="Numero",
        title="Tipologia clienti"
    )

    st.plotly_chart(fig_tipo, use_container_width=True)

fasce = dettaglio_richieste.groupby("fascia_eta").size().reset_index(name="Clienti")

fig_eta = px.bar(
    fasce,
    x="fascia_eta",
    y="Clienti",
    color="Clienti",
    title="Distribuzione per fascia d'età"
)

st.plotly_chart(fig_eta, use_container_width=True)

st.markdown("---")

# ==========================
# PROFILO CLIENTELA
# ==========================

st.markdown("---")
st.subheader("👥 Profilo della clientela e distribuzione territoriale")

clientela = dettaglio_richieste[
["Cliente", "tipo_cliente", "fascia_eta", "comune", "fidelizzato"]
].drop_duplicates()

col1, col2 = st.columns(2)

with col1:
    provenienza = clientela.groupby("comune").size().reset_index(name="Clienti")

    fig_comuni = px.pie(
    provenienza,
    names="comune",
    values="Clienti",
    title="Provenienza geografica della clientela",
    hole=0.35
    )

    fig_comuni.update_layout(height=360)
    st.plotly_chart(fig_comuni, use_container_width=True)

with col2:
    st.info("""
    **Osservazione BI**

    L'analisi evidenzia che la maggior parte delle richieste proviene dal territorio di **Mandatoriccio** e dai comuni limitrofi.

    Tra le località maggiormente rappresentate figurano **Rossano, Corigliano, Cariati e Pietrapaola**, oltre ai clienti residenti a Mandatoriccio.

    La piattaforma risulta quindi coerente con un modello di servizio on-demand radicato nel territorio locale.
    """)

col3, col4, col5, col6 = st.columns(4)

tipo_clienti = clientela["tipo_cliente"].value_counts(normalize=True) * 100
fascia_prevalente = clientela["fascia_eta"].value_counts().idxmax()
fidelizzati = clientela["fidelizzato"].value_counts(normalize=True).get("Sì", 0) * 100

with col3:
    st.metric("👤 Clienti privati", f"{tipo_clienti.get('Privato', 0):.0f}%")

with col4:
    st.metric("🏢 Attività locali", f"{tipo_clienti.get('Attività locale', 0):.0f}%")

with col5:
    st.metric("🎂 Fascia prevalente", fascia_prevalente)

with col6:
    st.metric("🔁 Clienti fidelizzati", f"{fidelizzati:.0f}%")

st.markdown("""
La clientela della piattaforma è composta prevalentemente da utenti privati, con una presenza significativa di piccole attività locali.
La fascia d'età più rappresentata consente di individuare il pubblico principale a cui rivolgere eventuali campagne promozionali.
Il tasso di fidelizzazione evidenzia la propensione degli utenti a riutilizzare il servizio dopo la prima esperienza.
""")

st.markdown("---")

st.subheader("📊 Analisi automatica")

st.success("""
✔ **Servizio più richiesto:** Pulizie

✔ **Fatturato maggiore:** Pulizie (€ 8.400)

✔ **Valutazione media:** 4.60 / 5

✔ **Crescita richieste semestre:** +130%

✔ **Raccomandazione AI:**
Si consiglia di investire nei servizi **Pulizie** e **Idraulico**, poiché rappresentano oltre il 50% del fatturato complessivo.
""")

st.markdown("---")

st.subheader("🏆 Top 3 servizi")

top3 = classifica_servizi.sort_values(
by="Richieste",
ascending=False
).head(3)

st.dataframe(
top3,
use_container_width=True
)
st.markdown("---")
st.subheader("📌 Riepilogo indicatori principali")

st.markdown(f"""
<div style="display: flex; gap: 18px; margin-top: 15px; margin-bottom: 25px;">
<div style="flex: 1; background-color: #eef6ff; padding: 22px; border-radius: 14px; border-left: 6px solid #2f80ed;">
<h4>📦 Richieste totali</h4>
<h2>{totale_richieste}</h2>
</div>
<div style="flex: 1; background-color: #f0fff4; padding: 22px; border-radius: 14px; border-left: 6px solid #27ae60;">
<h4>💰 Fatturato totale</h4>
<h2>€ {fatturato_totale:,.0f}</h2>
</div>
<div style="flex: 1; background-color: #fff9e6; padding: 22px; border-radius: 14px; border-left: 6px solid #f2c94c;">
<h4>⭐ Valutazione media</h4>
<h2>{valutazione_media:.2f} / 5</h2>
</div>
<div style="flex: 1; background-color: #f7f0ff; padding: 22px; border-radius: 14px; border-left: 6px solid #9b51e0;">
<h4>🛠️ Servizi attivi</h4>
<h2>{len(dettaglio_richieste)}</h2>
</div>
</div>
""", unsafe_allow_html=True)


st.subheader("📥 Esportazione dati")

csv = dettaglio_richieste.to_csv(index=False, sep=";").encode("utf-8-sig")

st.download_button(
label="⬇️ Esporta dati CSV",
data=csv,
file_name="ServiceHub_Report.csv",
mime="text/csv"
)
st.markdown("---")
if st.button("📄 Genera Report PDF"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    # =========================
    # PAGINA 1 - RIEPILOGO + TABELLA
    # =========================

    # Intestazione colorata
    pdf.set_fill_color(235, 243, 255)
    pdf.rect(10, 10, 190, 28, "F")

    pdf.set_font("Arial", "B", 18)
    pdf.set_text_color(20, 60, 110)
    pdf.cell(0, 10, "ServiceHub BI", ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(40, 40, 40)
    pdf.cell(0, 7, "Universita Telematica Pegaso", ln=True)
    pdf.cell(0, 7, "Project Work - Business Intelligence", ln=True)

    pdf.ln(12)

    # Titolo report
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(0, 80, 160)

    if servizio_selezionato == "Tutti":
        pdf.cell(0, 10, "Report completo di tutti i servizi", ln=True)
    else:
        pdf.cell(0, 10, f"Report del servizio: {servizio_selezionato}", ln=True)

    pdf.set_text_color(0, 0, 0)
    data_ora = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 7, f"Report generato il: {data_ora}", ln=True)

    pdf.ln(6)

    # KPI
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Riepilogo indicatori principali", ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", "", 10)

    pdf.set_fill_color(238, 246, 255)
    pdf.cell(95, 12, f"Richieste totali: {totale_richieste}", border=1, fill=True)

    pdf.set_fill_color(240, 255, 244)
    pdf.cell(95, 12, f"Fatturato totale: EUR {fatturato_totale:,.0f}", border=1, fill=True)
    pdf.ln()

    pdf.set_fill_color(255, 249, 230)
    pdf.cell(95, 12, f"Valutazione media: {valutazione_media:.2f}/5", border=1, fill=True)

    pdf.set_fill_color(247, 240, 255)
    pdf.cell(95, 12, f"Servizi analizzati: {len(dettaglio_richieste)}", border=1, fill=True)

    pdf.ln(16)

    # Tabella
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Dettaglio servizi", ln=True)
    pdf.ln(2)

    pdf.set_font("Arial", "B", 9)
    pdf.set_fill_color(220, 230, 241)

    pdf.cell(45, 8, "Servizio", border=1, fill=True)
    pdf.cell(35, 8, "Richieste", border=1, fill=True)
    pdf.cell(45, 8, "Valutazione", border=1, fill=True)
    pdf.cell(45, 8, "Fatturato EUR", border=1, fill=True)
    pdf.ln()

    pdf.set_font("Arial", "", 9)

    for index, row in dettaglio_richieste.iterrows():
        pdf.cell(45, 8, str(row["Servizio"]), border=1)
        pdf.cell(35, 8, str(row["Richieste"]), border=1)
        pdf.cell(45, 8, str(row["Valutazione media"]), border=1)
        pdf.cell(45, 8, str(row["Fatturato (€)"]), border=1)
        pdf.ln()

    pdf.ln(8)

    # Analisi sintetica
    servizio_top = dettaglio_richieste.sort_values(by="Richieste", ascending=False).iloc[0]["Servizio"]
    fatturato_top = dettaglio_richieste.sort_values(by="Fatturato (€)", ascending=False).iloc[0]["Servizio"]
    
    pdf.set_fill_color(245, 245, 245)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Sintesi automatica", ln=True)

    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 7,
    f"Il servizio con più richieste è {servizio_top}. "
    f"Il fatturato maggiore è generato da {fatturato_top}. "
    f"La valutazione media complessiva è pari a {valutazione_media:.2f}/5. "
    "I dati mostrano una base utile per supportare decisioni strategiche e operative."
    )
    
    # =========================
    # PAGINA 2 - GRAFICO
    # =========================

    pdf.add_page()

    pdf.set_font("Arial", "B", 15)
    pdf.set_text_color(0, 80, 160)
    pdf.cell(0, 10, "Analisi grafica richieste", ln=True)
    pdf.set_text_color(0, 0, 0)

    fig, ax = plt.subplots(figsize=(7, 3.2))
    ax.bar(dettaglio_richieste["Servizio"], dettaglio_richieste["Richieste"])
    ax.set_title("Richieste per servizio")
    ax.set_xlabel("Servizio")
    ax.set_ylabel("Richieste")
    plt.xticks(rotation=30)
    plt.tight_layout()

    grafico_path = "grafico_richieste.png"
    plt.savefig(grafico_path)
    plt.close()

    pdf.image(grafico_path, x=20, y=35, w=170, h=95)

    pdf.set_y(145)
    pdf.set_font("Arial", "", 10)
    pdf.multi_cell(0, 7,
        "Il grafico consente di confrontare rapidamente il volume delle richieste "
        "per ciascun servizio selezionato, evidenziando le aree con maggiore domanda."
    )

    pdf.output("ServiceHub_Report.pdf")

    with open("ServiceHub_Report.pdf", "rb") as file:
        st.download_button(
            "⬇️ Scarica Report PDF",
        file,
        file_name="ServiceHub_Report.pdf",
        mime="application/pdf"
        )
st.markdown("---")
st.subheader("🗃️ Struttura dati e modello a stella")
st.info("""
Il database del prototipo è organizzato secondo una struttura a stella.

La tabella centrale è richieste, che contiene i dati operativi principali.
Attorno ad essa sono collegate le tabelle dimensionali: clienti, fornitori, servizi e tempo.
""")

st.markdown("""
**Fact table**
- richieste: contiene richieste, importi, valutazioni, stato del servizio e tempo di erogazione.

**Dimension table**
- clienti: anagrafica clienti, zona e data di iscrizione.
- fornitori: operatori partner, servizio offerto, zona e valutazione.
- servizi: categorie dei servizi disponibili.
- tempo: data, mese, anno e giorno della settimana.
""")

st.markdown("---")
st.subheader("🔄 Procedura ETL")

st.info("""
Il prototipo utilizza una procedura ETL per simulare il processo di gestione dei dati.

**Estrazione:** generazione dei dati simulati relativi a clienti, fornitori, servizi, richieste e tempo.

**Trasformazione:** pulizia, organizzazione e normalizzazione dei dati attraverso identificativi, categorie, zone, date e stati delle richieste.

**Caricamento:** inserimento dei dati nel database SQLite `servicehub.db`, organizzato secondo una struttura a stella.
""")

st.markdown("""
Questa procedura consente di partire da dati simulati ma realistici e di trasformarli in informazioni utilizzabili dalla dashboard di Business Intelligence.
""")



