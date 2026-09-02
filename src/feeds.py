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

  # --- Institutions et regulateurs europeens -------------------------------
  {"name": "ACER", "url": "https://www.acer.europa.eu/rss.xml",
   "theme": "grid", "country": None, "verified": False},
  {"name": "ENTSOG", "url": "https://www.entsog.eu/rss.xml",
   "theme": "grid", "country": None, "verified": False},
  {"name": "ENTSO-E", "url": "https://www.entsoe.eu/rss/news/",
   "theme": "grid", "country": None, "verified": False},
  {"name": "Commission européenne", "url": "https://ec.europa.eu/commission/presscorner/api/rss?language=en",
   "theme": "grid", "country": None, "verified": False},

  # --- Politique monetaire -------------------------------------------------
  {"name": "BCE — communiqués", "url": "https://www.ecb.europa.eu/rss/press.html",
   "theme": "policy", "country": None, "verified": False},
  {"name": "BCE — politique monétaire", "url": "https://www.ecb.europa.eu/rss/pressmopo.html",
   "theme": "policy", "country": None, "verified": False},
  {"name": "Fed — politique monétaire", "url": "https://www.federalreserve.gov/feeds/press_monetary.xml",
   "theme": "policy", "country": None, "verified": False},
  {"name": "Bank of England", "url": "https://www.bankofengland.co.uk/news/news-rss",
   "theme": "policy", "country": "GB", "verified": False},

  # --- Gestionnaires de reseau, par pays -----------------------------------
  {"name": "RTE", "url": "https://www.rte-france.com/rss.xml",
   "theme": "grid", "country": "FR", "verified": False},
  {"name": "GRTgaz", "url": "https://www.grtgaz.com/rss.xml",
   "theme": "grid", "country": "FR", "verified": False},
  {"name": "Elia", "url": "https://www.elia.be/en/news/rss",
   "theme": "grid", "country": "BE", "verified": False},
  {"name": "TenneT", "url": "https://www.tennet.eu/rss/news",
   "theme": "grid", "country": "NL", "verified": False},
  {"name": "Snam", "url": "https://www.snam.it/en/rss/press-releases.xml",
   "theme": "grid", "country": "IT", "verified": False},
  {"name": "Enagás", "url": "https://www.enagas.es/en/rss/news/",
   "theme": "grid", "country": "ES", "verified": False},
  {"name": "National Gas", "url": "https://www.nationalgas.com/rss.xml",
   "theme": "grid", "country": "GB", "verified": False},
  {"name": "Fingrid", "url": "https://www.fingrid.fi/en/rss/",
   "theme": "grid", "country": "FI", "verified": False},
  {"name": "Energinet", "url": "https://en.energinet.dk/rss/",
   "theme": "grid", "country": "DK", "verified": False},
  {"name": "Bundesnetzagentur", "url": "https://www.bundesnetzagentur.de/SiteGlobals/Functions/RSSFeed/DE/RSSNewsfeed/RSSNewsfeed.xml",
   "theme": "grid", "country": "DE", "verified": False},
  {"name": "Statnett", "url": "https://www.statnett.no/en/rss/",
   "theme": "grid", "country": "NO", "verified": False},
  {"name": "PSE", "url": "https://www.pse.pl/rss",
   "theme": "grid", "country": "PL", "verified": False},
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
