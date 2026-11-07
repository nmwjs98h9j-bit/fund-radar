"""Bundled sample records; these values are not verified live market data."""

SEED_FUNDS = [
    {"id": "seed-1",  "name": "Tekmerion Capital Management", "strategy": "systematic", "aum": 1000, "perf": 18.2,  "date": "2025-02-01", "source": "news",  "founders": "Zachary Squire, Reed Morrissey", "prior": "D.E. Shaw, Bridgewater, HBK → Brevan Howard spin-out"},
    {"id": "seed-2",  "name": "Agave Capital Management",     "strategy": "macro",      "aum": 1000, "perf": None,  "date": "2025-07-01", "source": "news",  "founders": "Gilberto Marcheggiano",         "prior": "Citadel, Goldman Sachs, Bank of England"},
    {"id": "seed-3",  "name": "Deem Global",                  "strategy": "macro",      "aum": 1000, "perf": 14.3,  "date": "2022-06-01", "source": "edgar", "founders": "Asfandyar Nadeem",              "prior": "Brevan Howard"},
    {"id": "seed-4",  "name": "Kate Capital",                 "strategy": "macro",      "aum": None, "perf": None,  "date": "2024-10-01", "source": "news",  "founders": "Paul Podolsky",                 "prior": "Bridgewater Associates (LP/strategist)"},
    {"id": "seed-5",  "name": "Verdad Capital",               "strategy": "macro",      "aum": 1000, "perf": 15.6,  "date": "2019-01-01", "source": "edgar", "founders": "Dan Rasmussen",                 "prior": "Harvard (academic) → Bain Capital"},
    {"id": "seed-6",  "name": "Taula Capital Management",     "strategy": "macro",      "aum": 6000, "perf": None,  "date": "2024-06-01", "source": "edgar", "founders": "Diego Megia",                   "prior": "Millennium Management"},
    {"id": "seed-7",  "name": "Aspect Capital",               "strategy": "systematic", "aum": 1200, "perf": 9.3,   "date": "1997-01-01", "source": "nfa",   "founders": "Anthony Todd",                  "prior": "AHL / Man Group"},
    {"id": "seed-8",  "name": "Fort LP",                      "strategy": "systematic", "aum": 900,  "perf": 11.7,  "date": "1993-01-01", "source": "nfa",   "founders": "Yves Balcer, Sanjiv Kumar",     "prior": "Academic — Johns Hopkins"},
    {"id": "seed-9",  "name": "Chesapeake Capital Corp",      "strategy": "cta",        "aum": 650,  "perf": 12.1,  "date": "1988-01-01", "source": "nfa",   "founders": "Jerry Parker",                  "prior": "Richard Dennis / Turtles program"},
    {"id": "seed-10", "name": "Welton Investment Corp",       "strategy": "cta",        "aum": 520,  "perf": 7.2,   "date": "1988-01-01", "source": "nfa",   "founders": "Patrick Welton",                "prior": "Discretionary trader"},
    # Merger Arb
    {"id": "seed-11", "name": "Pentwater Capital Management",  "strategy": "merger-arb", "aum": 4500, "perf": 8.1,   "date": "2007-01-01", "source": "edgar", "founders": "Matthew Halbower",              "prior": "Stark Investments"},
    {"id": "seed-12", "name": "Sculptor Capital Management",   "strategy": "merger-arb", "aum": 9000, "perf": 6.4,   "date": "1994-01-01", "source": "edgar", "founders": "Daniel Och",                    "prior": "Goldman Sachs"},
    {"id": "seed-13", "name": "Gabelli Funds",                 "strategy": "merger-arb", "aum": 800,  "perf": 5.9,   "date": "1977-01-01", "source": "edgar", "founders": "Mario Gabelli",                 "prior": "Loeb Rhoades"},
    {"id": "seed-14", "name": "Westchester Capital Management","strategy": "merger-arb", "aum": 1100, "perf": 7.2,   "date": "1990-01-01", "source": "edgar", "founders": "Roy Behren, Michael Shannon",    "prior": "Gabelli Funds"},
    {"id": "seed-15", "name": "Water Island Capital",          "strategy": "merger-arb", "aum": 1600, "perf": 6.8,   "date": "2000-01-01", "source": "edgar", "founders": "John Orrico",                   "prior": "Bear Stearns"},
    # Commodity
    {"id": "seed-16", "name": "Andurand Capital Management",   "strategy": "commodity",  "aum": 1800, "perf": 22.4,  "date": "2012-01-01", "source": "news",  "founders": "Pierre Andurand",               "prior": "BlueGold Capital, Goldman Sachs"},
    {"id": "seed-17", "name": "Galena Asset Management",       "strategy": "commodity",  "aum": 700,  "perf": 11.3,  "date": "2004-01-01", "source": "edgar", "founders": "Jaime Bejarano",                "prior": "Trafigura"},
    {"id": "seed-18", "name": "Merchant Commodity Fund",       "strategy": "commodity",  "aum": 600,  "perf": 9.7,   "date": "2004-01-01", "source": "edgar", "founders": "Michael Coleman",               "prior": "Commodities Corp / Goldman Sachs"},
    {"id": "seed-19", "name": "Crosby Resource Capital",       "strategy": "commodity",  "aum": 2000, "perf": None,  "date": "2024-01-01", "source": "news",  "founders": "Robert Crosby",                 "prior": "Citadel (head of agriculture)"},
    {"id": "seed-20", "name": "Quantix Commodities",           "strategy": "commodity",  "aum": 900,  "perf": 13.1,  "date": "2018-01-01", "source": "edgar", "founders": "Don Casturo",                   "prior": "Goldman Sachs commodities desk"},
]

SEED_NEWS = [
    {"id": "sn-1", "headline": "Tekmerion Capital spinning out of Brevan Howard with $1B, actively fundraising", "source": "Business Insider", "time": "Feb 25 2026", "tag": "#spinout #brevan #systematic", "fundRef": "Tekmerion Capital Management"},
    {"id": "sn-2", "headline": "Two new Millennium spin-out commodity funds seeking $1.4B combined",             "source": "Bloomberg",        "time": "Feb 23 2026", "tag": "#spinout #millennium #commodities", "fundRef": None},
    {"id": "sn-3", "headline": "Agave Capital (ex-Citadel) targets $1B launch with quant macro strategy",       "source": "Hedgeweek",        "time": "Jul 2025",    "tag": "#launch #citadel #macro", "fundRef": "Agave Capital Management"},
    {"id": "sn-4", "headline": "Taula Capital grows to $6B+, hires ex-Brevan Howard PM Alfredo Saitta",         "source": "Bloomberg",        "time": "Jan 2025",    "tag": "#growth #millennium #macro", "fundRef": "Taula Capital Management"},
    {"id": "sn-5", "headline": "Deem Global crosses $1B AUM on double-digit returns since 2022 inception",      "source": "Hedgeweek",        "time": "Sep 2024",    "tag": "#emerging #brevan #macro", "fundRef": "Deem Global"},
    {"id": "sn-6", "headline": "Crosby Resource Capital launches with $2B, founder ex-Citadel head of agriculture", "source": "eFinancialCareers","time": "Jan 2024",    "tag": "#launch #citadel #commodity", "fundRef": "Crosby Resource Capital"},
    {"id": "sn-7", "headline": "Andurand Capital bets big on energy transition; energy fund up 22% in 2024",     "source": "Bloomberg",        "time": "Dec 2024",    "tag": "#commodity #energy #performance", "fundRef": "Andurand Capital Management"},
    {"id": "sn-8", "headline": "Merger arbitrage funds see record deal flow as M&A activity surges in 2025",     "source": "Institutional Inv.","time": "Jan 2025",    "tag": "#merger-arb #dealflow #mna", "fundRef": None},
    {"id": "sn-9", "headline": "Water Island Capital raises $400M for new event-driven sleeve",                  "source": "Hedgeweek",        "time": "Mar 2024",    "tag": "#merger-arb #event-driven #raise", "fundRef": "Water Island Capital"},
]

