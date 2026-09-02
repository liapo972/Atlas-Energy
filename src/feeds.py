# -*- coding: utf-8 -*-
"""Sources d'actualite. / News sources.

IMPORTANT - les URL de flux ci-dessous n'ont pas pu etre validees depuis
l'environnement de developpement. Lancer une fois :

    python3 fetch_news.py --check

pour tester chaque flux et retirer ou corriger ceux qui ne repondent pas.
Le champ "verified" documente ce qui a ete confirme.

Champs :
  name     libelle affiche
  url      URL du flux RSS ou Atom
  theme    "grid" (GRT/regulateur) | "policy" (politique monetaire) | "press"
  country  code pays si le flux est mono-pays, sinon None
  verified True une fois le flux confirme par --check
"""

FEEDS = [

  # --- Institutions et regulateurs europeens (URL confirmees en production) ---
  {"name": "ACER", "urls": ["https://www.acer.europa.eu/rss.xml"],
   "theme": "grid", "country": None},
  {"name": "ENTSOG", "urls": ["https://www.entsog.eu/rss.xml"],
   "theme": "grid", "country": None},
  {"name": "ENTSO-E", "urls": ["https://www.entsoe.eu/rss.xml"],
   "theme": "grid", "country": None},
  {"name": "Commission européenne", "urls": [
      "https://ec.europa.eu/commission/presscorner/api/rss?language=en"],
   "theme": "grid", "country": None},

  # --- Politique monetaire ---------------------------------------------------
  {"name": "BCE", "urls": ["https://www.ecb.europa.eu/rss/press.html"],
   "theme": "policy", "country": None},
  {"name": "Fed — politique monétaire", "urls": [
      "https://www.federalreserve.gov/feeds/press_monetary.xml"],
   "theme": "policy", "country": None},
  {"name": "Bank of England", "urls": ["https://www.bankofengland.co.uk/rss/news"],
   "theme": "policy", "country": "GB"},

  # --- Gestionnaires de reseau et regulateurs nationaux ----------------------
  {"name": "GRTgaz", "urls": ["https://www.grtgaz.com/rss.xml"],
   "theme": "grid", "country": "FR"},
  {"name": "National Gas", "urls": ["https://www.nationalgas.com/rss.xml"],
   "theme": "grid", "country": "GB"},
  {"name": "Statnett", "urls": ["https://www.statnett.no/en/rss/"],
   "theme": "grid", "country": "NO"},
  {"name": "Bundesnetzagentur", "urls": ["https://www.bundesnetzagentur.de/rss.xml"],
   "theme": "grid", "country": "DE"},

  # Retires apres test : RTE, Elia, TenneT, Snam, Enagas, Fingrid, Energinet et
  # PSE ne publient pas de flux RSS accessible. Leurs pays restent couverts par
  # GDELT et par les liens directs du panneau. A retenter si l'un d'eux en
  # ouvre un.
]
# Requetes GDELT. Sans cle, gratuit, JSON. Sert de socle : la page n'est
# jamais vide meme si des flux RSS ci-dessus sont morts.
GDELT_WORLD = (
  '("natural gas" OR "power market" OR "electricity price" OR LNG OR '
  '"energy crisis" OR "gas storage" OR "central bank" OR "interest rate") '
  'sourcelang:english'
)

# Termes ajoutes a la requete GDELT pour chaque pays.
GDELT_COUNTRY_TERMS = '(gas OR electricity OR energy OR power)'

# Noms utilises pour taguer un article a un pays, en plus du flux d'origine.
KEYWORDS = {
  "FR": ["France", "French", "RTE", "GRTgaz", "PEG", "EDF"],
  "DE": ["Germany", "German", "Allemagne", "THE", "Uniper", "Bundesnetzagentur"],
  "NL": ["Netherlands", "Dutch", "TTF", "Gasunie", "Groningen"],
  "BE": ["Belgium", "Belgian", "Zeebrugge", "Fluxys", "Elia"],
  "GB": ["United Kingdom", "Britain", "British", "NBP", "Ofgem", "National Grid"],
  "IE": ["Ireland", "Irish", "EirGrid"],
  "CH": ["Switzerland", "Swiss", "Swissgrid"],
  "AT": ["Austria", "Austrian", "Baumgarten", "CEGH"],
  "ES": ["Spain", "Spanish", "MIBGAS", "Enagas", "Enagás"],
  "PT": ["Portugal", "Portuguese", "Sines"],
  "IT": ["Italy", "Italian", "Snam", "PSV", "Terna"],
  "PL": ["Poland", "Polish", "Baltic Pipe", "Swinoujscie", "GAZ-SYSTEM"],
  "CZ": ["Czech", "Czechia", "NET4GAS"],
  "SK": ["Slovakia", "Slovak", "Eustream"],
  "HU": ["Hungary", "Hungarian", "FGSZ"],
  "RO": ["Romania", "Romanian", "Transgaz"],
  "GR": ["Greece", "Greek", "Revithoussa", "DESFA", "Alexandroupolis"],
  "BG": ["Bulgaria", "Bulgarian", "Bulgartransgaz", "Chiren"],
  "NO": ["Norway", "Norwegian", "Gassco", "Equinor", "Statnett"],
  "SE": ["Sweden", "Swedish", "Svenska kraftnat"],
  "DK": ["Denmark", "Danish", "Energinet"],
  "FI": ["Finland", "Finnish", "Fingrid", "Olkiluoto", "Inkoo"],
  "EE": ["Estonia", "Estonian", "Elering"],
  "LV": ["Latvia", "Latvian", "Incukalns"],
  "LT": ["Lithuania", "Lithuanian", "Klaipeda"],
  "SI": ["Slovenia", "Slovenian", "Krsko"],
  "HR": ["Croatia", "Croatian", "Krk"],
  "RS": ["Serbia", "Serbian"],
}
