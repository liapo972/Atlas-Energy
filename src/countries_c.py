# -*- coding: utf-8 -*-
"""Bloc C : Nordiques, Baltes, Balkans occidentaux.
Block C: Nordics, Baltics, Western Balkans."""

C = {

"NO": {
  "name": {"fr": "Norvège", "en": "Norway"},
  "zone": "NO2", "eic": "10YNO-2--------T",
  "spot": "Nord Pool", "hub": None, "agsi": None,
  "tso": [
    ["Statnett — Power system data", "https://www.statnett.no/en/for-stakeholders-in-the-power-industry/data-from-the-power-system/",
     {"fr": "réseau électrique", "en": "power system"}],
    ["Gassco", "https://www.gassco.no/en/",
     {"fr": "réseau gazier vers le continent", "en": "gas pipelines to the continent"}],
    ["Nord Pool — market data", "https://data.nordpoolgroup.com/",
     {"fr": "prix day-ahead", "en": "day-ahead prices"}]
  ],
  "notes": {
    "fr": [
      "<b>Cinq zones de dépôt (NO1 à NO5)</b> avec des écarts parfois spectaculaires entre le sud, connecté au continent, et le nord excédentaire.",
      "La carte affiche NO2 (sud-ouest), la zone reliée à l'Allemagne et au Royaume-Uni par câbles — celle qui importe la volatilité continentale.",
      "Système quasi entièrement hydraulique : le niveau des réservoirs est le fondamental numéro un, davantage que la demande.",
      "<b>Premier fournisseur de gaz par gazoduc de l'Europe</b> depuis la chute des flux russes — les flux Gassco sont devenus un indicateur central.",
      "Pas de hub gazier domestique : le gaz norvégien se vend aux hubs d'arrivée (TTF, NBP, Zeebrugge)."
    ],
    "en": [
      "<b>Five bidding zones (NO1 to NO5)</b>, with sometimes spectacular spreads between the south, cabled to the continent, and the surplus north.",
      "The map shows NO2 (south-west), the zone connected to Germany and the UK by cable — the one that imports continental volatility.",
      "An almost entirely hydro system: reservoir levels are the number one fundamental, more so than demand.",
      "<b>Europe's largest pipeline gas supplier</b> since Russian flows collapsed — Gassco flows have become a central indicator.",
      "No domestic gas hub: Norwegian gas is sold at the landing hubs (TTF, NBP, Zeebrugge)."
    ]
  }
},

"SE": {
  "name": {"fr": "Suède", "en": "Sweden"},
  "zone": "SE3", "eic": "10Y1001A1001A46L",
  "spot": "Nord Pool", "hub": None, "agsi": None,
  "tso": [
    ["Svenska kraftnät", "https://www.svk.se/en/",
     {"fr": "réseau électrique", "en": "power grid"}],
    ["Nord Pool — market data", "https://data.nordpoolgroup.com/",
     {"fr": "prix day-ahead", "en": "day-ahead prices"}]
  ],
  "notes": {
    "fr": [
      "Quatre zones de dépôt (SE1 à SE4) : hydraulique et éolien au nord, consommation au sud, congestion structurelle entre les deux.",
      "La carte affiche SE3 (Stockholm), la zone la plus peuplée.",
      "Mix hydraulique et nucléaire, avec un éolien en forte croissance.",
      "Pas de marché gazier significatif : le gaz est marginal dans le mix énergétique suédois."
    ],
    "en": [
      "Four bidding zones (SE1 to SE4): hydro and wind in the north, demand in the south, structural congestion in between.",
      "The map shows SE3 (Stockholm), the most populated zone.",
      "A hydro and nuclear mix, with wind growing fast.",
      "No significant gas market: gas is marginal in the Swedish energy mix."
    ]
  }
},

"DK": {
  "name": {"fr": "Danemark", "en": "Denmark"},
  "zone": "DK1", "eic": "10YDK-1--------W",
  "spot": "Nord Pool", "hub": "ETF", "agsi": "DK",
  "tso": [
    ["Energinet — Energi Data Service", "https://www.energidataservice.dk/",
     {"fr": "open data exemplaire, API gratuite", "en": "exemplary open data, free API"}],
    ["Nord Pool — market data", "https://data.nordpoolgroup.com/",
     {"fr": "prix day-ahead", "en": "day-ahead prices"}]
  ],
  "notes": {
    "fr": [
      "Deux zones séparées par le Grand Belt : DK1 à l'ouest (synchronisée au continent) et DK2 à l'est (synchronisée aux nordiques).",
      "La carte affiche DK1, la zone la plus éolienne et la plus volatile.",
      "Taux de pénétration éolienne parmi les plus élevés au monde — épisodes de prix négatifs fréquents.",
      "<b>Energi Data Service est le portail open data à citer en exemple</b> : API gratuite, sans friction, documentation claire."
    ],
    "en": [
      "Two zones split by the Great Belt: DK1 in the west (synchronised with the continent) and DK2 in the east (synchronised with the Nordics).",
      "The map shows DK1, the windiest and most volatile zone.",
      "One of the highest wind penetration rates in the world — negative price episodes are frequent.",
      "<b>Energi Data Service is the open data portal to hold up as an example</b>: free API, no friction, clear documentation."
    ]
  }
},

"FI": {
  "name": {"fr": "Finlande", "en": "Finland"},
  "zone": "FI", "eic": "10YFI-1--------U",
  "spot": "Nord Pool", "hub": None, "agsi": None,
  "tso": [
    ["Fingrid — Open Data", "https://data.fingrid.fi/en",
     {"fr": "API gratuite et complète", "en": "free and complete API"}],
    ["Nord Pool — market data", "https://data.nordpoolgroup.com/",
     {"fr": "prix day-ahead", "en": "day-ahead prices"}]
  ],
  "notes": {
    "fr": [
      "Zone unique, fortement dépendante des importations depuis la Suède et de sa capacité nucléaire.",
      "La mise en service d'Olkiluoto 3 a durablement abaissé le niveau des prix finlandais.",
      "Marché gazier marginal ; le terminal GNL d'Inkoo assure la sécurité d'approvisionnement depuis l'arrêt des importations russes.",
      "Fingrid propose l'une des meilleures API publiques d'Europe, à connaître."
    ],
    "en": [
      "A single zone, heavily dependent on imports from Sweden and on its nuclear capacity.",
      "Commissioning Olkiluoto 3 durably lowered Finnish price levels.",
      "A marginal gas market; the Inkoo LNG terminal secures supply since Russian imports stopped.",
      "Fingrid offers one of the best public APIs in Europe, worth knowing."
    ]
  }
},

"EE": {
  "name": {"fr": "Estonie", "en": "Estonia"},
  "zone": "EE", "eic": "10Y1001A1001A39I",
  "spot": "Nord Pool", "hub": None, "agsi": None,
  "tso": [
    ["Elering — Live", "https://elering.ee/en",
     {"fr": "réseau élec et gaz, données ouvertes", "en": "power and gas grid, open data"}]
  ],
  "notes": {
    "fr": [
      "Les pays baltes se sont désynchronisés du système russe pour rejoindre le réseau continental européen.",
      "Prix très corrélés à la Finlande via les câbles Estlink.",
      "Elering opère à la fois l'électricité et le gaz, avec un portail de données ouvert."
    ],
    "en": [
      "The Baltic states desynchronised from the Russian system to join the European continental grid.",
      "Prices are strongly correlated with Finland through the Estlink cables.",
      "Elering operates both power and gas, with an open data portal."
    ]
  }
},

"LV": {
  "name": {"fr": "Lettonie", "en": "Latvia"},
  "zone": "LV", "eic": "10YLV-1001A00074",
  "spot": "Nord Pool", "hub": None, "agsi": "LV",
  "tso": [
    ["AST", "https://www.ast.lv/en",
     {"fr": "réseau électrique", "en": "power grid"}]
  ],
  "notes": {
    "fr": [
      "Abrite Inčukalns, principal stockage souterrain de gaz de la région balte — actif stratégique régional.",
      "Marché électrique intégré au couplage nordique via Nord Pool.",
      "Forte composante hydraulique sur la Daugava."
    ],
    "en": [
      "Home to Inčukalns, the main underground gas storage in the Baltic region — a strategic regional asset.",
      "The power market is integrated into Nordic coupling through Nord Pool.",
      "A strong hydro component on the Daugava river."
    ]
  }
},

"LT": {
  "name": {"fr": "Lituanie", "en": "Lithuania"},
  "zone": "LT", "eic": "10YLT-1001A0008Q",
  "spot": "Nord Pool", "hub": None, "agsi": None,
  "tso": [
    ["Litgrid", "https://www.litgrid.eu/index.php/?lang=2",
     {"fr": "réseau électrique", "en": "power grid"}]
  ],
  "notes": {
    "fr": [
      "Le terminal GNL flottant de Klaipėda a été le premier levier d'indépendance gazière de la région.",
      "Pays fortement importateur d'électricité depuis la fermeture d'Ignalina.",
      "Interconnexions LitPol et NordBalt avec la Pologne et la Suède."
    ],
    "en": [
      "The Klaipėda floating LNG terminal was the region's first lever of gas independence.",
      "A heavy net importer of electricity since the closure of Ignalina.",
      "LitPol and NordBalt interconnections with Poland and Sweden."
    ]
  }
},

"SI": {
  "name": {"fr": "Slovénie", "en": "Slovenia"},
  "zone": "SI", "eic": "10YSI-ELES-----O",
  "spot": "BSP SouthPool", "hub": None, "agsi": None,
  "tso": [
    ["ELES", "https://www.eles.si/en",
     {"fr": "réseau électrique", "en": "power grid"}]
  ],
  "notes": {
    "fr": [
      "Petit marché fortement couplé à l'Italie et à l'Autriche.",
      "Centrale nucléaire de Krško exploitée conjointement avec la Croatie — cas unique en Europe.",
      "Pas de hub gazier organisé."
    ],
    "en": [
      "A small market, tightly coupled with Italy and Austria.",
      "The Krško nuclear plant is jointly operated with Croatia — a unique arrangement in Europe.",
      "No organised gas hub."
    ]
  }
},

"HR": {
  "name": {"fr": "Croatie", "en": "Croatia"},
  "zone": "HR", "eic": "10YHR-HEP------M",
  "spot": "CROPEX", "hub": None, "agsi": "HR",
  "tso": [
    ["HOPS", "https://www.hops.hr/en",
     {"fr": "réseau électrique", "en": "power grid"}]
  ],
  "notes": {
    "fr": [
      "Le terminal GNL de Krk a fait du pays un point d'entrée régional pour les Balkans et l'Europe centrale.",
      "Copropriétaire de la centrale nucléaire de Krško avec la Slovénie.",
      "Marché électrique de taille modeste, couplé à ses voisins."
    ],
    "en": [
      "The Krk LNG terminal turned the country into a regional entry point for the Balkans and Central Europe.",
      "Co-owner of the Krško nuclear plant with Slovenia.",
      "A modest power market, coupled with its neighbours."
    ]
  }
},

"RS": {
  "name": {"fr": "Serbie", "en": "Serbia"},
  "zone": "RS", "eic": "10YCS-SERBIATSOV",
  "spot": "SEEPEX", "hub": None, "agsi": "RS",
  "tso": [
    ["EMS", "https://www.ems.rs/en/",
     {"fr": "réseau électrique", "en": "power grid"}]
  ],
  "notes": {
    "fr": [
      "Hors Union européenne mais membre de la Communauté de l'énergie, donc aligné progressivement sur les règles du marché intérieur.",
      "Mix électrique dominé par le lignite.",
      "Point de passage des flux gaziers venus de Bulgarie vers la Hongrie."
    ],
    "en": [
      "Outside the European Union but a member of the Energy Community, so progressively aligned with internal market rules.",
      "A power mix dominated by lignite.",
      "A transit point for gas flows from Bulgaria towards Hungary."
    ]
  }
},

}
