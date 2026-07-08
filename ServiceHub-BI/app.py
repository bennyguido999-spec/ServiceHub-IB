import streamlit as st
import pandas as pd
import plotly.express as px
import io
from fpdf import FPDF
import os 
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

dati_servizi = {
"Servizio": ["Idraulico", "Giardiniere", "Pulizie", "Elettricista", "Baby sitter"],
"Richieste": [120, 95, 150, 80, 60],
"Valutazione media": [4.7, 4.5, 4.8, 4.6, 4.4],
"Fatturato (€)": [7200, 5200, 8400, 6100, 3000]
}

st.dataframe(dati_servizi, use_container_width=True)
st.markdown("---")
classifica_servizi = pd.DataFrame(dati_servizi)

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
df_servizi = pd.DataFrame(dati_servizi)

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

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Richieste totali", totale_richieste)

with col2:
    st.metric("Fatturato totale", f"€ {fatturato_totale:,.0f}")

with col3:
    st.metric("Valutazione media", f"{valutazione_media:.2f} / 5")

with col4:
    st.metric("Servizi attivi", len(classifica_servizi))

st.subheader("📥 Esportazione dati")

csv = dati_filtrati.to_csv(index=False, sep=";").encode("utf-8-sig")

st.download_button(
label="⬇️ Esporta dati CSV",
data=csv,
file_name="ServiceHub_Report.csv",
mime="text/csv"
)
st.markdown("---")
if st.button("📄 Genera Report PDF"):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, "ServiceHub BI", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Universita Telematica Pegaso", ln=True)
    pdf.cell(0, 10, "Project Work - Business Intelligence", ln=True)
    pdf.ln(10)

    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Riepilogo Dashboard", ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Richieste totali: {totale_richieste}", ln=True)
    pdf.cell(0, 10, f"Fatturato totale: EUR {fatturato_totale:,.0f}", ln=True)
    pdf.cell(0, 10, f"Valutazione media: {valutazione_media:.2f}/5", ln=True)
    pdf.cell(0, 10, f"Servizi attivi: {len(classifica_servizi)}", ln=True)

    pdf.output("ServiceHub_Report.pdf")

    with open("ServiceHub_Report.pdf", "rb") as file:
        st.download_button(
        "⬇️ Scarica Report PDF",
        file,
        file_name="ServiceHub_Report.pdf",
        mime="application/pdf"
)

