# -*- coding: utf-8 -*-
"""Bloc B : peninsule iberique, Italie, Europe centrale et du Sud-Est.
Block B: Iberia, Italy, Central and South-Eastern Europe."""

B = {

"ES": {
  "name": {"fr": "Espagne", "en": "Spain"},
  "zone": "ES", "eic": "10YES-REE------0",
  "spot": "OMIE", "hub": "PVB / MIBGAS", "agsi": "ES",
  "tso": [
    ["REE — e·sios", "https://www.esios.ree.es/en",
     {"fr": "portail marché très complet", "en": "very complete market portal"}],
    ["OMIE — market results", "https://www.omie.es/en/market-results",
     {"fr": "prix day-ahead MIBEL", "en": "MIBEL day-ahead prices"}],
    ["MIBGAS — market results", "https://www.mibgas.es/en/market-results",
     {"fr": "enchères et indices gaz", "en": "gas auctions and indices"}],
    ["Enagás — GTS", "https://www.enagas.es/en/technical-management-system/",
     {"fr": "réseau gaz et GNL", "en": "gas grid and LNG"}]
  ],
  "notes": {
    "fr": [
      "<b>MIBGAS publie ses indices quotidiens en accès libre</b> — l'une des rares bourses gazières européennes aussi ouverte.",
      "Gaz en régime <b>daily balanced</b>, cotation en €/MWh PCS.",
      "Plus grande capacité de regazéification d'Europe, mais le pays reste une « île gazière » : les interconnexions avec la France limitent la réexportation.",
      "Électricité : marché ibérique MIBEL commun avec le Portugal, avec market splitting quand l'interconnexion sature.",
      "e·sios est le meilleur portail public espagnol, gratuit et doté d'une API."
    ],
    "en": [
      "<b>MIBGAS publishes its daily indices openly</b> — one of the few European gas exchanges that transparent.",
      "Gas is <b>daily balanced</b>, quoted in €/MWh on a gross calorific value basis.",
      "The largest regasification capacity in Europe, yet the country remains a \"gas island\": interconnection with France limits re-export.",
      "Power: the MIBEL Iberian market shared with Portugal, with market splitting whenever the interconnector saturates.",
      "e·sios is the best Spanish public portal, free and with an API."
    ]
  }
},

"PT": {
  "name": {"fr": "Portugal", "en": "Portugal"},
  "zone": "PT", "eic": "10YPT-REN------W",
  "spot": "OMIE", "hub": None, "agsi": "PT",
  "tso": [
    ["REN — Data Hub", "https://datahub.ren.pt/en/",
     {"fr": "électricité et gaz", "en": "power and gas"}],
    ["OMIE — market results", "https://www.omie.es/en/market-results",
     {"fr": "prix MIBEL", "en": "MIBEL prices"}]
  ],
  "notes": {
    "fr": [
      "Même marché day-ahead que l'Espagne (MIBEL) : prix identiques sauf congestion de l'interconnexion, qui déclenche le market splitting.",
      "Terminal GNL de Sines, principal point d'entrée gazier.",
      "Très forte part hydraulique et éolienne — la variabilité hydrologique pèse lourd sur les prix annuels."
    ],
    "en": [
      "Same day-ahead market as Spain (MIBEL): identical prices except when the interconnector congests and market splitting kicks in.",
      "The Sines LNG terminal is the main gas entry point.",
      "Very high hydro and wind share — hydrological variability weighs heavily on yearly price levels."
    ]
  }
},

"IT": {
  "name": {"fr": "Italie", "en": "Italy"},
  "zone": "IT-Nord", "eic": "10Y1001A1001A73I",
  "spot": "GME / IPEX", "hub": "PSV", "agsi": "IT",
  "tso": [
    ["Terna — Transparency", "https://www.terna.it/en/electric-system/transparency-report",
     {"fr": "réseau électrique", "en": "power grid"}],
    ["GME — market results", "https://www.mercatoelettrico.org/En/Default.aspx",
     {"fr": "prix zonaux et PUN", "en": "zonal prices and PUN"}],
    ["Snam — Transparency", "https://www.snam.it/en/transportation/",
     {"fr": "réseau gaz, PSV, stockages", "en": "gas grid, PSV, storage"}]
  ],
  "notes": {
    "fr": [
      "<b>Marché zonal</b> : plusieurs zones de prix (nord, centre-nord, centre-sud, sud, Calabre, Sicile, Sardaigne) avec des écarts parfois très larges.",
      "Le <b>PUN</b> est la moyenne nationale pondérée par la consommation — prix de référence des clients finals, mais pas un prix négociable.",
      "La carte affiche la zone nord, la plus liquide et la plus corrélée au continent.",
      "Gaz : PSV, coté en €/MWh. Point d'arrivée majeur des flux algériens, azéris et du GNL.",
      "Capacités de stockage importantes, opérées par Stogit (groupe Snam)."
    ],
    "en": [
      "<b>Zonal market</b>: several price zones (north, centre-north, centre-south, south, Calabria, Sicily, Sardinia) with sometimes very wide spreads.",
      "The <b>PUN</b> is the demand-weighted national average — the reference price for end customers, but not a tradable price.",
      "The map shows the northern zone, the most liquid and the most correlated with the continent.",
      "Gas: PSV, quoted in €/MWh. A major landing point for Algerian, Azeri and LNG flows.",
      "Substantial storage capacity, operated by Stogit (Snam group)."
    ]
  }
},

"PL": {
  "name": {"fr": "Pologne", "en": "Poland"},
  "zone": "PL", "eic": "10YPL-AREA-----S",
  "spot": "TGE", "hub": "RIM / TGE", "agsi": "PL",
  "tso": [
    ["PSE", "https://www.pse.pl/home",
     {"fr": "opérateur système", "en": "system operator"}],
    ["TGE — Polish Power Exchange", "https://tge.pl/en",
     {"fr": "électricité et gaz", "en": "power and gas"}],
    ["GAZ-SYSTEM", "https://www.gaz-system.pl/en/",
     {"fr": "réseau gaz, terminal GNL", "en": "gas grid, LNG terminal"}]
  ],
  "notes": {
    "fr": [
      "Mix encore très charbonnier : les prix polonais décrochent souvent du reste de la plaque continentale.",
      "Le Baltic Pipe a rebattu les cartes de l'approvisionnement gazier depuis la Norvège.",
      "Terminal GNL de Świnoujście, en extension continue.",
      "TGE cote à la fois l'électricité et le gaz, avec une obligation historique de vente en bourse."
    ],
    "en": [
      "Still a coal-heavy mix: Polish prices often decouple from the rest of the continental plate.",
      "Baltic Pipe reshaped gas supply, bringing Norwegian volumes directly.",
      "The Świnoujście LNG terminal is under continuous expansion.",
      "TGE lists both power and gas, with a historic obligation to sell through the exchange."
    ]
  }
},

"CZ": {
  "name": {"fr": "Tchéquie", "en": "Czechia"},
  "zone": "CZ", "eic": "10YCZ-CEPS-----N",
  "spot": "OTE", "hub": "VTP CZ", "agsi": "CZ",
  "tso": [
    ["ČEPS", "https://www.ceps.cz/en/",
     {"fr": "réseau électrique", "en": "power grid"}],
    ["OTE — market data", "https://www.ote-cr.cz/en",
     {"fr": "opérateur de marché élec et gaz", "en": "power and gas market operator"}],
    ["NET4GAS", "https://www.net4gas.cz/en/",
     {"fr": "transit gazier", "en": "gas transit"}]
  ],
  "notes": {
    "fr": [
      "Pays de transit gazier majeur entre l'Allemagne, la Slovaquie et l'Autriche.",
      "OTE joue le double rôle d'opérateur de marché électricité et gaz, ce qui rend ses données particulièrement pratiques.",
      "Forte corrélation des prix électriques avec la zone DE-LU via le couplage."
    ],
    "en": [
      "A major gas transit country between Germany, Slovakia and Austria.",
      "OTE acts as both power and gas market operator, which makes its data unusually convenient.",
      "Power prices are strongly correlated with the DE-LU zone through market coupling."
    ]
  }
},

"SK": {
  "name": {"fr": "Slovaquie", "en": "Slovakia"},
  "zone": "SK", "eic": "10YSK-SEPS-----K",
  "spot": "OKTE", "hub": "VTP SK", "agsi": "SK",
  "tso": [
    ["SEPS", "https://www.sepsas.sk/en/",
     {"fr": "réseau électrique", "en": "power grid"}],
    ["OKTE", "https://www.okte.sk/en/",
     {"fr": "opérateur de marché", "en": "market operator"}],
    ["Eustream", "https://www.eustream.sk/en/",
     {"fr": "transit gazier", "en": "gas transit"}]
  ],
  "notes": {
    "fr": [
      "Corridor de transit historique du gaz vers l'ouest — les évolutions de flux y sont un indicateur géopolitique suivi de près.",
      "Forte composante nucléaire dans le mix électrique.",
      "Marché couplé avec la Tchéquie, la Hongrie et la Roumanie."
    ],
    "en": [
      "A historic westward gas transit corridor — flow changes here are a closely watched geopolitical indicator.",
      "Strong nuclear component in the power mix.",
      "Market coupled with Czechia, Hungary and Romania."
    ]
  }
},

"HU": {
  "name": {"fr": "Hongrie", "en": "Hungary"},
  "zone": "HU", "eic": "10YHU-MAVIR----U",
  "spot": "HUPX", "hub": "MGP / CEEGEX", "agsi": "HU",
  "tso": [
    ["MAVIR", "https://www.mavir.hu/web/mavir-en",
     {"fr": "réseau électrique", "en": "power grid"}],
    ["HUPX", "https://hupx.hu/en",
     {"fr": "bourse électricité", "en": "power exchange"}],
    ["FGSZ", "https://fgsz.hu/en",
     {"fr": "réseau gaz", "en": "gas grid"}]
  ],
  "notes": {
    "fr": [
      "Plaque tournante gazière régionale, avec des capacités de stockage importantes pour la taille du pays.",
      "CEEGEX est la plateforme gazière organisée, adossée à HUPX.",
      "Prix électriques souvent parmi les plus élevés du couplage continental, faute de capacité d'interconnexion suffisante."
    ],
    "en": [
      "A regional gas hub, with storage capacity that is large for the size of the country.",
      "CEEGEX is the organised gas platform, operated alongside HUPX.",
      "Power prices are often among the highest in continental coupling, for lack of interconnection capacity."
    ]
  }
},

"RO": {
  "name": {"fr": "Roumanie", "en": "Romania"},
  "zone": "RO", "eic": "10YRO-TEL------P",
  "spot": "OPCOM", "hub": "BRM / VTP", "agsi": "RO",
  "tso": [
    ["Transelectrica", "https://www.transelectrica.ro/en/web/tel/home",
     {"fr": "réseau électrique", "en": "power grid"}],
    ["OPCOM", "https://www.opcom.ro/",
     {"fr": "bourse électricité", "en": "power exchange"}],
    ["Transgaz", "https://www.transgaz.ro/en",
     {"fr": "réseau gaz", "en": "gas grid"}]
  ],
  "notes": {
    "fr": [
      "Production gazière domestique significative, avec les projets offshore de mer Noire en développement.",
      "Mix électrique diversifié : nucléaire, hydraulique, charbon, éolien en Dobroudja.",
      "Marché couplé au reste de l'Europe centrale depuis l'extension du couplage journalier."
    ],
    "en": [
      "Significant domestic gas production, with Black Sea offshore projects under development.",
      "Diversified power mix: nuclear, hydro, coal and wind in Dobruja.",
      "Coupled with the rest of Central Europe since day-ahead coupling was extended."
    ]
  }
},

"GR": {
  "name": {"fr": "Grèce", "en": "Greece"},
  "zone": "GR", "eic": "10YGR-HTSO-----Y",
  "spot": "HEnEx", "hub": None, "agsi": "GR",
  "tso": [
    ["IPTO / ADMIE", "https://www.admie.gr/en",
     {"fr": "réseau électrique", "en": "power grid"}],
    ["HEnEx", "https://www.enexgroup.gr/",
     {"fr": "bourse électricité et gaz", "en": "power and gas exchange"}],
    ["DESFA", "https://www.desfa.gr/en",
     {"fr": "réseau gaz, GNL Revithoussa", "en": "gas grid, Revithoussa LNG"}]
  ],
  "notes": {
    "fr": [
      "Porte d'entrée du gaz vers les Balkans : terminal de Revithoussa, unité flottante d'Alexandroupolis, gazoduc TAP depuis l'Azerbaïdjan.",
      "Prix électriques parmi les plus élevés d'Europe, en raison de l'isolement relatif du système.",
      "Rôle régional croissant depuis la réorientation des flux européens."
    ],
    "en": [
      "A gateway for gas into the Balkans: the Revithoussa terminal, the Alexandroupolis floating unit, and the TAP pipeline from Azerbaijan.",
      "Power prices are among the highest in Europe, given the relative isolation of the system.",
      "A growing regional role since European flows were redirected."
    ]
  }
},

"BG": {
  "name": {"fr": "Bulgarie", "en": "Bulgaria"},
  "zone": "BG", "eic": "10YCA-BULGARIA-R",
  "spot": "IBEX", "hub": None, "agsi": "BG",
  "tso": [
    ["ESO", "https://www.eso.bg/?lang=en",
     {"fr": "réseau électrique", "en": "power grid"}],
    ["IBEX", "https://ibex.bg/en/",
     {"fr": "bourse électricité", "en": "power exchange"}],
    ["Bulgartransgaz", "https://www.bulgartransgaz.bg/en/",
     {"fr": "réseau gaz, transit", "en": "gas grid, transit"}]
  ],
  "notes": {
    "fr": [
      "Nœud de transit vers la Serbie, la Hongrie et au-delà — les flux via la Bulgarie sont un indicateur régional suivi.",
      "L'interconnexion avec la Grèce a diversifié l'approvisionnement.",
      "Stockage de Chiren, unique site du pays."
    ],
    "en": [
      "A transit node towards Serbia, Hungary and beyond — Bulgarian flows are a watched regional indicator.",
      "The interconnection with Greece diversified supply.",
      "Chiren is the country's only storage site."
    ]
  }
},

}
