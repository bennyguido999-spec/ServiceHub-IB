import sqlite3
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker("it_IT")

conn = sqlite3.connect("servicehub.db")
cursor = conn.cursor()

cursor.executescript("""
DROP TABLE IF EXISTS richieste;
DROP TABLE IF EXISTS clienti;
DROP TABLE IF EXISTS fornitori;
DROP TABLE IF EXISTS servizi;
DROP TABLE IF EXISTS tempo;
""")

cursor.execute("""
CREATE TABLE clienti (
    id_cliente INTEGER PRIMARY KEY,
    nome TEXT,
    zona TEXT,
    data_iscrizione TEXT,
    tipo_cliente TEXT,
    fascia_eta TEXT,
    comune TEXT,
    fidelizzato TEXT
)
""")

cursor.execute("""
CREATE TABLE fornitori (
    id_fornitore INTEGER PRIMARY KEY,
    nome TEXT,
    servizio TEXT,
    zona TEXT,
    valutazione_media REAL
)
""")

cursor.execute("""
CREATE TABLE servizi (
   id_servizio INTEGER PRIMARY KEY,
    nome TEXT,
    categoria TEXT
)
""")

cursor.execute("""
CREATE TABLE tempo (
    id_tempo INTEGER PRIMARY KEY,
    data TEXT,
    mese TEXT,
    anno INTEGER,
    giorno_settimana TEXT
)
""")

cursor.execute("""
CREATE TABLE richieste (
    id_richiesta INTEGER PRIMARY KEY,
    id_cliente INTEGER,
    id_fornitore INTEGER,
    id_servizio INTEGER,
    id_tempo INTEGER,
    zona TEXT,
    importo REAL,
    valutazione REAL,
    stato TEXT,
    tempo_erogazione_min INTEGER,
    FOREIGN KEY(id_cliente) REFERENCES clienti(id_cliente),
    FOREIGN KEY(id_fornitore) REFERENCES fornitori(id_fornitore),
    FOREIGN KEY(id_servizio) REFERENCES servizi(id_servizio),
    FOREIGN KEY(id_tempo) REFERENCES tempo(id_tempo)
)
""")

servizi = [
    (1, "Pulizie", "Casa"),
    (2, "Idraulico", "Manutenzione"),
    (3, "Giardiniere", "Esterno"),
    (4, "Elettricista", "Manutenzione"),
    (5, "Baby sitter", "Famiglia")
]

zone = ["Centro", "Nord", "Sud", "Est", "Ovest"]
tipi_cliente = ["Privato", "Attività locale"]

fasce_eta = ["18-30", "31-45", "46-60", "Over 60"]

comuni = [
    "Mandatoriccio",
    "Rossano",
    "Corigliano",
    "Cariati",
    "Pietrapaola",
    "Altri comuni limitrofi"
]

fidelizzazione = ["Sì", "No"]

for servizio in servizi:
    cursor.execute("INSERT INTO servizi VALUES (?, ?, ?)", servizio)

for i in range(1, 151):
    cursor.execute("""
    INSERT INTO clienti VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        i,
        fake.name(),
        random.choice(zone),
        str(fake.date_between(start_date="-3y", end_date="today")),
        random.choices(tipi_cliente, weights=[72, 28])[0],
        random.choices(fasce_eta, weights=[18, 40, 30, 12])[0],
        random.choices(comuni, weights=[35, 20, 18, 15, 7, 5])[0],
        random.choices(fidelizzazione, weights=[61, 39])[0]
    ))

for i in range(1, 31):
    servizio_scelto = random.choice(servizi)[1]
    cursor.execute("""
    INSERT INTO fornitori VALUES (?, ?, ?, ?, ?)
    """, (
    i,
    fake.company(),
    servizio_scelto,
   random.choice(zone),
    round(random.uniform(4.0, 5.0), 1)
))

data_inizio = datetime(2025, 1, 1)

for i in range(1, 366):
   data = data_inizio + timedelta(days=i - 1)
   cursor.execute("""
   INSERT INTO tempo VALUES (?, ?, ?, ?, ?)
   """, (
       i,
       data.strftime("%Y-%m-%d"),
        data.strftime("%B"),
        data.year,
        data.strftime("%A")
    ))

for i in range(1, 501):
    id_cliente = random.randint(1, 150)
    id_servizio = random.randint(1, 5)

    servizio_nome = servizi[id_servizio - 1][1]

    cursor.execute("""
    SELECT id_fornitore
    FROM fornitori
    WHERE servizio = ?
    ORDER BY RANDOM()
    LIMIT 1
    """, (servizio_nome,))

    risultato = cursor.fetchone()

    if risultato:
        id_fornitore = risultato[0]
    else:
        id_fornitore = random.randint(1, 30)

    cursor.execute("""
    INSERT INTO richieste VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        i,
        id_cliente,
        id_fornitore,
        id_servizio,
        random.randint(1, 365),
        random.choice(zone),
        random.randint(40, 350),
        round(random.uniform(4.0, 5.0), 1),
        random.choice(["Completata", "Completata", "Completata", "Annullata"]),
        random.randint(30, 240)
    ))

conn.commit()
conn.close()

print("Database ServiceHub creato correttamente con struttura a stella.")
