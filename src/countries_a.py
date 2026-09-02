# -*- coding: utf-8 -*-
"""Metadonnees pays - bloc A : Europe de l'Ouest. / Country metadata - block A: Western Europe.

Champs / fields :
  name  : {"fr":..., "en":...}
  zone  : zone de depot electrique representee / bidding zone shown on the map
  eic   : code EIC de cette zone (API ENTSO-E)
  spot  : bourse spot electricite / power spot exchange
  hub   : hub gaz / gas hub (ou None)
  agsi  : code pays AGSI+ / AGSI+ country code (ou None)
  ccy   : devise des prix elec / power price currency (defaut EUR)
  tso   : [libelle, url, {"fr":note, "en":note}]
  notes : {"fr":[...], "en":[...]}  specificites de marche / market specifics
"""

A = {

"FR": {
  "name": {"fr": "France", "en": "France"},
  "zone": "FR", "eic": "10YFR-RTE------C",
  "spot": "EPEX SPOT", "hub": "PEG (TRF)", "agsi": "FR",
  "tso": [
    ["RTE — éCO2mix", "https://www.rte-france.com/eco2mix",
     {"fr": "conso, mix, prix", "en": "demand, mix, prices"}],
    ["GRTgaz — Smart", "https://www.smart.grtgaz.com/en",
     {"fr": "flux, équilibrage, prix TRF", "en": "flows, balancing, TRF price"}],
    ["Teréga — Data", "https://www.terega.fr/en/data",
     {"fr": "sud-ouest, stockages", "en": "south-west, storage"}]
  ],
  "notes": {
    "fr": [
      "Gaz : zone unique TRF depuis 2018 — la fusion des zones nord et sud a supprimé le spread PEG Nord/TRS.",
      "Gaz en régime <b>daily balanced</b> : l'expéditeur équilibre sur la journée gazière, pas heure par heure.",
      "Journée gazière 06:00 → 06:00 CET, cotation en €/MWh PCS.",
      "Électricité : zone de dépôt unique malgré la taille du pays — pas de découpage zonal comme en Italie ou en Norvège."
    ],
    "en": [
      "Gas: single TRF zone since 2018 — merging the northern and southern zones removed the PEG Nord/TRS spread.",
      "Gas is <b>daily balanced</b>: shippers balance over the gas day, not hour by hour.",
      "Gas day runs 06:00 → 06:00 CET, quoted in €/MWh on a gross calorific value basis.",
      "Power: a single bidding zone despite the size of the country — no zonal split as in Italy or Norway."
    ]
  }
},

"DE": {
  "name": {"fr": "Allemagne", "en": "Germany"},
  "zone": "DE-LU", "eic": "10Y1001A1001A82H",
  "spot": "EPEX SPOT", "hub": "THE", "agsi": "DE",
  "tso": [
    ["SMARD — Bundesnetzagentur", "https://www.smard.de/en",
     {"fr": "le meilleur portail public européen", "en": "the best public portal in Europe"}],
    ["Trading Hub Europe", "https://www.tradinghub.eu/en-gb/",
     {"fr": "hub gaz THE", "en": "THE gas hub"}],
    ["netztransparenz.de", "https://www.netztransparenz.de/en",
     {"fr": "transparence des 4 GRT", "en": "transparency of the 4 TSOs"}]
  ],
  "notes": {
    "fr": [
      "Zone de dépôt commune avec le Luxembourg (DE-LU) depuis la séparation d'avec l'Autriche en 2018.",
      "Gaz : THE est né en 2021 de la fusion de NCG et GASPOOL — un seul hub allemand là où il y en avait deux.",
      "Quatre GRT électricité se partagent le territoire, mais une seule zone de prix.",
      "SMARD est le point d'entrée à recommander à quelqu'un qui découvre : tout y est gratuit et lisible."
    ],
    "en": [
      "Bidding zone shared with Luxembourg (DE-LU) since the split from Austria in 2018.",
      "Gas: THE was created in 2021 by merging NCG and GASPOOL — one German hub where there used to be two.",
      "Four power TSOs share the territory, but there is a single price zone.",
      "SMARD is the entry point to recommend to a newcomer: everything is free and readable."
    ]
  }
},

"NL": {
  "name": {"fr": "Pays-Bas", "en": "Netherlands"},
  "zone": "NL", "eic": "10YNL----------L",
  "spot": "EPEX SPOT", "hub": "TTF", "agsi": "NL",
  "tso": [
    ["TenneT NL", "https://www.tennet.eu/nl/elektriciteitsmarkt-inzichten",
     {"fr": "marché électrique", "en": "power market insights"}],
    ["Gasunie Transport Services", "https://www.gasunietransportservices.nl/en",
     {"fr": "réseau gaz, TTF", "en": "gas grid, TTF"}]
  ],
  "notes": {
    "fr": [
      "<b>TTF est la référence gazière européenne</b> : la majorité des contrats du continent y sont indexés, y compris hors Pays-Bas.",
      "C'est le hub le plus liquide d'Europe — c'est lui qu'on cite quand on dit « le prix du gaz en Europe ».",
      "Cotation en €/MWh, journée gazière 06:00 → 06:00 CET.",
      "Le champ de Groningue étant fermé, le pays est importateur net : le TTF reste un hub financier plus qu'un point de production."
    ],
    "en": [
      "<b>TTF is the European gas benchmark</b>: most continental contracts are indexed to it, including outside the Netherlands.",
      "It is the most liquid hub in Europe — it is what people mean by \"the European gas price\".",
      "Quoted in €/MWh, gas day 06:00 → 06:00 CET.",
      "With the Groningen field shut, the country is a net importer: TTF is now a financial hub rather than a production point."
    ]
  }
},

"BE": {
  "name": {"fr": "Belgique", "en": "Belgium"},
  "zone": "BE", "eic": "10YBE----------2",
  "spot": "EPEX SPOT", "hub": "ZTP", "agsi": "BE",
  "tso": [
    ["Elia — Open Data", "https://opendata.elia.be/",
     {"fr": "excellent portail open data", "en": "excellent open data portal"}],
    ["Fluxys — Transparency", "https://www.fluxys.com/en/energy-transition/transparency",
     {"fr": "gaz, GNL Zeebrugge", "en": "gas, Zeebrugge LNG"}]
  ],
  "notes": {
    "fr": [
      "Zeebrugge est un point d'entrée GNL majeur et une porte vers le Royaume-Uni via l'Interconnector.",
      "Gaz coté en €/MWh sur ZTP, mais la proximité du NBP en fait un point d'arbitrage entre les deux conventions.",
      "Le portail open data d'Elia est l'un des plus généreux d'Europe — bon exemple à citer."
    ],
    "en": [
      "Zeebrugge is a major LNG entry point and a gateway to the UK through the Interconnector.",
      "Gas is quoted in €/MWh at ZTP, but proximity to NBP makes it an arbitrage point between the two conventions.",
      "Elia's open data portal is one of the most generous in Europe — a good example to cite."
    ]
  }
},

"GB": {
  "name": {"fr": "Royaume-Uni", "en": "United Kingdom"},
  "zone": "GB", "eic": "10YGB----------A",
  "spot": "EPEX SPOT / N2EX", "hub": "NBP", "agsi": "GB", "ccy": "GBP",
  "tso": [
    ["NESO — Data Portal", "https://www.neso.energy/data-portal",
     {"fr": "opérateur système", "en": "system operator"}],
    ["Elexon — BMRS", "https://bmrs.elexon.co.uk/",
     {"fr": "prix d'équilibrage, settlement", "en": "imbalance prices, settlement"}],
    ["National Gas — Data", "https://www.nationalgas.com/data-and-operations",
     {"fr": "réseau gaz, NBP", "en": "gas grid, NBP"}]
  ],
  "notes": {
    "fr": [
      "<b>Le gaz se cote en pence par therm (p/th), pas en €/MWh</b> — c'est le piège numéro un quand on compare NBP et TTF.",
      "Conversion approximative : 1 therm ≈ 29,3071 kWh. Il faut convertir <i>et</i> passer de GBP à EUR pour comparer.",
      "Électricité cotée en £/MWh.",
      "Journée gazière 05:00 → 05:00 heure locale, décalée par rapport au continent.",
      "Depuis le Brexit, le GB est sorti du couplage de marché — les échanges passent par des enchères explicites sur interconnexions."
    ],
    "en": [
      "<b>Gas is quoted in pence per therm (p/th), not €/MWh</b> — the number one trap when comparing NBP and TTF.",
      "Rough conversion: 1 therm ≈ 29.3071 kWh. You have to convert the unit <i>and</i> the currency to compare.",
      "Power is quoted in £/MWh.",
      "Gas day runs 05:00 → 05:00 local time, offset from the continent.",
      "Since Brexit, GB has left market coupling — cross-border trade goes through explicit interconnector auctions."
    ]
  }
},

"IE": {
  "name": {"fr": "Irlande", "en": "Ireland"},
  "zone": "IE (SEM)", "eic": "10Y1001A1001A59C",
  "spot": "SEMOpx", "hub": None, "agsi": None,
  "tso": [
    ["EirGrid — Smart Grid Dashboard", "https://www.smartgriddashboard.com/",
     {"fr": "temps réel île entière", "en": "all-island real time"}],
    ["SEMO", "https://www.sem-o.com/",
     {"fr": "marché unique tout-île", "en": "single all-island market"}]
  ],
  "notes": {
    "fr": [
      "Marché unique de l'électricité couvrant la République et l'Irlande du Nord (SEM) — une seule zone pour deux juridictions.",
      "Forte pénétration éolienne : les épisodes de prix négatifs et de curtailment y sont fréquents.",
      "Pas de hub gaz coté : approvisionnement via l'interconnexion britannique, indexé NBP."
    ],
    "en": [
      "A single electricity market covering the Republic and Northern Ireland (SEM) — one zone across two jurisdictions.",
      "High wind penetration: negative prices and curtailment episodes are frequent.",
      "No quoted gas hub: supply comes through the UK interconnection and is indexed to NBP."
    ]
  }
},

"CH": {
  "name": {"fr": "Suisse", "en": "Switzerland"},
  "zone": "CH", "eic": "10YCH-SWISSGRIDZ",
  "spot": "EPEX SPOT", "hub": None, "agsi": None,
  "tso": [
    ["Swissgrid — Grid Data", "https://www.swissgrid.ch/en/home/operation/grid-data.html",
     {"fr": "réseau et marché", "en": "grid and market"}]
  ],
  "notes": {
    "fr": [
      "Hors couplage de marché faute d'accord-cadre : les flux passent par des enchères explicites, avec des inefficacités visibles sur les spreads.",
      "Très forte composante hydraulique avec pompage-turbinage : le pays joue le rôle de batterie de l'arc alpin.",
      "Pas de marché gazier organisé : approvisionnement contractuel via l'Allemagne, la France et l'Italie."
    ],
    "en": [
      "Outside market coupling for lack of a framework agreement: flows go through explicit auctions, with inefficiencies visible in the spreads.",
      "Heavily hydro, with large pumped storage: the country acts as the battery of the Alpine arc.",
      "No organised gas market: supply is contractual, through Germany, France and Italy."
    ]
  }
},

"AT": {
  "name": {"fr": "Autriche", "en": "Austria"},
  "zone": "AT", "eic": "10YAT-APG------L",
  "spot": "EXAA / EPEX SPOT", "hub": "CEGH VTP", "agsi": "AT",
  "tso": [
    ["APG — Market Transparency", "https://markttransparenz.apg.at/en",
     {"fr": "transparence marché", "en": "market transparency"}],
    ["CEGH", "https://www.cegh.at/en/",
     {"fr": "hub gaz autrichien", "en": "Austrian gas hub"}],
    ["Gas Connect Austria", "https://www.gasconnect.at/en",
     {"fr": "réseau gaz", "en": "gas grid"}]
  ],
  "notes": {
    "fr": [
      "Baumgarten est un nœud gazier majeur — point d'entrée des flux venus de l'est et carrefour vers l'Italie.",
      "Zone de dépôt séparée de l'Allemagne depuis 2018 ; les deux pays formaient auparavant une seule zone.",
      "Capacité de stockage très importante rapportée à la consommation nationale, d'où un rôle régional."
    ],
    "en": [
      "Baumgarten is a major gas node — entry point for eastern flows and a crossroads towards Italy.",
      "Bidding zone separated from Germany in 2018; the two countries previously formed a single zone.",
      "Storage capacity is very large relative to national demand, which gives the country a regional role."
    ]
  }
},

}
