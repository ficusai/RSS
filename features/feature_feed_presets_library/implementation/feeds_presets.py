"""
Pre-Configured Feed Presets Library (Git Branch: feature/feed-presets-library)

239 curated RSS/Atom feed subscriptions across 22 industry
categories, sourced from market intelligence feed catalogs.
"""

from typing import Any, Dict, List

PRESET_CATEGORIES: List[str] = [
    "Technology",
    "Artificial Intelligence",
    "Science & Space",
    "Central Banks",
    "Economy & Indicators",
    "Finance & Markets",
    "Bonds & Credit",
    "Commodities & Energy",
    "Housing Market",
    "Crypto & Forex",
    "Business & Corporate",
    "World News",
    "Europe",
    "Asia-Pacific",
    "Geopolitics & Security",
    "Crisis Indicators",
    "Health & Medical",
    "Cybersecurity",
    "Maritime & Supply Chain",
    "Agriculture",
    "Legal & Regulatory",
    "Quality of Life",
]

PRESET_FEEDS: List[Dict[str, str]] = [
    # --- Technology ---
    {"name": "ArsTechnica", "url": "http://feeds.arstechnica.com/arstechnica/index", "category": "Technology"},
    {"name": "Bloomberg Tech", "url": "https://feeds.bloomberg.com/technology/news.rss", "category": "Technology"},
    {"name": "Engadget", "url": "https://www.engadget.com/rss.xml", "category": "Technology"},
    {"name": "Reuters Tech", "url": "http://feeds.reuters.com/reuters/technologyNews", "category": "Technology"},
    {"name": "TechCrunch", "url": "https://techcrunch.com/feed/", "category": "Technology"},
    {"name": "TheVerge", "url": "https://www.theverge.com/rss/index.xml", "category": "Technology"},
    {"name": "Wired", "url": "https://www.wired.com/feed/rss", "category": "Technology"},
    # --- Artificial Intelligence ---
    {"name": "AI Research Feed", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_ai_research.xml", "category": "Artificial Intelligence"},
    {"name": "Anthropic News", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_anthropic_news.xml", "category": "Artificial Intelligence"},
    {"name": "Anthropic Red Teaming", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_anthropic_red.xml", "category": "Artificial Intelligence"},
    {"name": "Anthropic Research", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_anthropic_research.xml", "category": "Artificial Intelligence"},
    {"name": "Arena Magazine", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_arenamag.xml", "category": "Artificial Intelligence"},
    {"name": "DeepMind Blog", "url": "https://deepmind.com/blog/feed/basic/", "category": "Artificial Intelligence"},
    {"name": "Digg AI", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_digg_tech.xml", "category": "Artificial Intelligence"},
    {"name": "Google AI Blog", "url": "https://ai.googleblog.com/feeds/posts/default", "category": "Artificial Intelligence"},
    {"name": "Hacker News", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_hackernews.xml", "category": "Artificial Intelligence"},
    {"name": "MIT Technology Review AI", "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed/", "category": "Artificial Intelligence"},
    {"name": "Mistral AI News", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_mistral_news.xml", "category": "Artificial Intelligence"},
    {"name": "OpenAI Alignment", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_openai_alignment.xml", "category": "Artificial Intelligence"},
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss.xml", "category": "Artificial Intelligence"},
    {"name": "OpenAI Research", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_openai_research.xml", "category": "Artificial Intelligence"},
    {"name": "Pirate Wires", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_piratewires.xml", "category": "Artificial Intelligence"},
    {"name": "Steve Jobs Archive", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_steve_jobs_archive_stories.xml", "category": "Artificial Intelligence"},
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "category": "Artificial Intelligence"},
    {"name": "The Verge AI", "url": "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml", "category": "Artificial Intelligence"},
    {"name": "Thinking Machines Blog", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_thinkingmachines.xml", "category": "Artificial Intelligence"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/ai/feed/", "category": "Artificial Intelligence"},
    {"name": "xAI News", "url": "https://raw.githubusercontent.com/0xSMW/rss-feeds/main/feeds/feed_xai_news.xml", "category": "Artificial Intelligence"},
    # --- Science & Space ---
    {"name": "MIT News", "url": "https://news.mit.edu/rss/feed", "category": "Science & Space"},
    {"name": "NASA News", "url": "https://www.nasa.gov/news/nasa-news-feed.rss", "category": "Science & Space"},
    {"name": "NASASpaceflight", "url": "https://www.nasaspaceflight.com/feed/", "category": "Science & Space"},
    {"name": "Nature", "url": "http://www.nature.com/nature/current_issue/rss", "category": "Science & Space"},
    {"name": "PLOS ONE", "url": "http://everyone.plos.org/feed/", "category": "Science & Space"},
    {"name": "ScienceMag", "url": "https://www.science.org/rss/news_current.xml", "category": "Science & Space"},
    {"name": "Scientific American", "url": "http://rss.sciam.com/ScientificAmerican-Global", "category": "Science & Space"},
    {"name": "SpaceNews", "url": "https://spacenews.com/feed/", "category": "Science & Space"},
    # --- Central Banks ---
    {"name": "Atlanta Fed", "url": "https://www.atlantafed.org/rss/news", "category": "Central Banks"},
    {"name": "Bank of Canada", "url": "https://www.bankofcanada.ca/feed/", "category": "Central Banks"},
    {"name": "Bank of Canada", "url": "https://www.bankofcanada.ca/rss-feeds/", "category": "Central Banks"},
    {"name": "Bank of England", "url": "https://www.bankofengland.co.uk/rss/news", "category": "Central Banks"},
    {"name": "Bank of Japan", "url": "https://www.boj.or.jp/en/rss/index.xml", "category": "Central Banks"},
    {"name": "Bundesbank", "url": "https://www.bundesbank.de/en/rss/", "category": "Central Banks"},
    {"name": "CBR Russia News", "url": "http://www.cbr.ru/rss/RssNews", "category": "Central Banks"},
    {"name": "CBR Russia Press", "url": "http://www.cbr.ru/rss/RssPress", "category": "Central Banks"},
    {"name": "ECB Press", "url": "https://www.ecb.europa.eu/rss/press.xml", "category": "Central Banks"},
    {"name": "ECB Speeches", "url": "https://www.ecb.europa.eu/rss/speeches.xml", "category": "Central Banks"},
    {"name": "Fed FOMC", "url": "https://www.federalreserve.gov/feeds/press_monetary.xml", "category": "Central Banks"},
    {"name": "Federal Reserve", "url": "https://www.federalreserve.gov/feeds/press_all.xml", "category": "Central Banks"},
    {"name": "NY Fed", "url": "https://www.newyorkfed.org/feeds/all_feeds.xml", "category": "Central Banks"},
    {"name": "RBA Australia", "url": "https://www.rba.gov.au/rss/rss-cb-bulletin.xml", "category": "Central Banks"},
    {"name": "RBA Speeches", "url": "https://www.rba.gov.au/rss/rss-cb-speeches.xml", "category": "Central Banks"},
    {"name": "RBI India", "url": "https://www.rbi.org.in/pressreleases_rss.xml", "category": "Central Banks"},
    {"name": "Richmond Fed", "url": "https://www.richmondfed.org/rss/news", "category": "Central Banks"},
    {"name": "SNB Swiss", "url": "https://www.snb.ch/en/rss", "category": "Central Banks"},
    # --- Economy & Indicators ---
    {"name": "ADP Employment", "url": "https://mediacenter.adp.com/feed/", "category": "Economy & Indicators"},
    {"name": "BEA GDP", "url": "https://www.bea.gov/feeds/rss.xml", "category": "Economy & Indicators"},
    {"name": "BLS Employment", "url": "https://www.bls.gov/feed/bls_latest.rss", "category": "Economy & Indicators"},
    {"name": "Census Economic", "url": "https://www.census.gov/economic-indicators/indicator.xml", "category": "Economy & Indicators"},
    {"name": "Challenger Layoffs", "url": "https://www.challengergray.com/feed/", "category": "Economy & Indicators"},
    {"name": "Chicago PMI", "url": "https://www.ism-chicago.org/feed/", "category": "Economy & Indicators"},
    {"name": "Conference Board", "url": "https://www.conference-board.org/rss/rssconsumerconfidence.xml", "category": "Economy & Indicators"},
    {"name": "FRED StLouis", "url": "https://fred.stlouisfed.org/tags/series/rss", "category": "Economy & Indicators"},
    {"name": "Glassdoor Research", "url": "https://www.glassdoor.com/research/rss/", "category": "Economy & Indicators"},
    {"name": "ISM Manufacturing", "url": "https://www.ismworld.org/feed/", "category": "Economy & Indicators"},
    {"name": "Indeed Hiring", "url": "https://www.hiringlab.org/feed/", "category": "Economy & Indicators"},
    {"name": "JOLTS Report", "url": "https://www.bls.gov/jlt/rss/jolts.rss", "category": "Economy & Indicators"},
    {"name": "LinkedIn Workforce", "url": "https://economicgraph.linkedin.com/rss", "category": "Economy & Indicators"},
    {"name": "Monster Employment", "url": "https://www.monster.com/rss/", "category": "Economy & Indicators"},
    {"name": "Trading Economics", "url": "https://tradingeconomics.com/rss/news.aspx", "category": "Economy & Indicators"},
    {"name": "We Work Remotely", "url": "https://weworkremotely.com/remote-jobs.rss", "category": "Economy & Indicators"},
    # --- Finance & Markets ---
    {"name": "ARK Invest", "url": "https://ark-invest.com/feed/", "category": "Finance & Markets"},
    {"name": "Bloomberg Markets", "url": "https://feeds.bloomberg.com/markets/news.rss", "category": "Finance & Markets"},
    {"name": "Bloomberg Opinion Levine", "url": "https://www.bloomberg.com/opinion/authors/ARbTQlRLRjE/matthew-s-levine.rss", "category": "Finance & Markets"},
    {"name": "DowJones News", "url": "https://www.dowjones.com/feed/", "category": "Finance & Markets"},
    {"name": "FT Markets", "url": "https://www.ft.com/markets?format=rss", "category": "Finance & Markets"},
    {"name": "FT Tech", "url": "https://www.ft.com/technology?format=rss", "category": "Finance & Markets"},
    {"name": "FTSE Russell", "url": "https://www.ftserussell.com/rss.xml", "category": "Finance & Markets"},
    {"name": "Forbes Investing", "url": "https://www.forbes.com/investing/feed/", "category": "Finance & Markets"},
    {"name": "Investing Indices", "url": "https://www.investing.com/rss/indices_news.rss", "category": "Finance & Markets"},
    {"name": "Investopedia", "url": "https://www.investopedia.com/rss/news", "category": "Finance & Markets"},
    {"name": "MSCI Indices", "url": "https://www.msci.com/rss", "category": "Finance & Markets"},
    {"name": "MarketBeat Alerts", "url": "https://www.marketbeat.com/rss/instant-alerts.xml", "category": "Finance & Markets"},
    {"name": "MarketWatch", "url": "http://feeds.marketwatch.com/marketwatch/topstories", "category": "Finance & Markets"},
    {"name": "NASDAQ Feed", "url": "https://www.nasdaq.com/feed/nasdaq-original/rss.xml", "category": "Finance & Markets"},
    {"name": "NYSE Updates", "url": "https://www.nyse.com/rss/news", "category": "Finance & Markets"},
    {"name": "S&P 500 News", "url": "https://www.spglobal.com/spdji/en/indices/equity/sp-500/rss.xml", "category": "Finance & Markets"},
    {"name": "Seeking Alpha Editors' Picks", "url": "https://seekingalpha.com/tag/editors-picks.xml", "category": "Finance & Markets"},
    {"name": "Stratechery", "url": "https://stratechery.com/feed/", "category": "Finance & Markets"},
    {"name": "The Economist Finance", "url": "https://www.economist.com/finance-and-economics/rss.xml", "category": "Finance & Markets"},
    {"name": "The Information", "url": "https://www.theinformation.com/feed", "category": "Finance & Markets"},
    {"name": "WSJ Markets", "url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml", "category": "Finance & Markets"},
    {"name": "Yahoo Finance", "url": "https://feeds.finance.yahoo.com/rss/2.0/headline", "category": "Finance & Markets"},
    {"name": "Yahoo Finance Index", "url": "https://finance.yahoo.com/news/rssindex", "category": "Finance & Markets"},
    # --- Bonds & Credit ---
    {"name": "Bond Buyer", "url": "https://www.bondbuyer.com/feed", "category": "Bonds & Credit"},
    {"name": "Credit Suisse", "url": "https://www.credit-suisse.com/about-us/en/rss.html", "category": "Bonds & Credit"},
    {"name": "Fitch Ratings", "url": "https://www.fitchratings.com/feed/", "category": "Bonds & Credit"},
    {"name": "Fixed Income", "url": "https://www.fixedincomeinvestor.co.uk/rss", "category": "Bonds & Credit"},
    {"name": "Moodys", "url": "https://www.moodys.com/rss/research", "category": "Bonds & Credit"},
    {"name": "S&P Ratings", "url": "https://www.spglobal.com/ratings/en/rss/", "category": "Bonds & Credit"},
    {"name": "Treasury Direct", "url": "https://www.treasurydirect.gov/rss/RSS_TD_Announcements.xml", "category": "Bonds & Credit"},
    # --- Commodities & Energy ---
    {"name": "Action Forex", "url": "https://www.actionforex.com/feed/", "category": "Commodities & Energy"},
    {"name": "AgWeb", "url": "https://www.agweb.com/rss/news", "category": "Commodities & Energy"},
    {"name": "Bitcoinist", "url": "https://bitcoinist.com/feed/", "category": "Commodities & Energy"},
    {"name": "Bloomberg Energy", "url": "https://feeds.bloomberg.com/energy/news.rss", "category": "Commodities & Energy"},
    {"name": "CommodityTV", "url": "https://www.commodity-tv.com/api/feeds/rss/", "category": "Commodities & Energy"},
    {"name": "Investing Commodities", "url": "https://www.investing.com/rss/commodities_news.rss", "category": "Commodities & Energy"},
    {"name": "Kitco Gold", "url": "https://www.kitco.com/rss/gold.xml", "category": "Commodities & Energy"},
    {"name": "Kitco Market Nuggets", "url": "https://feeds.kitco.com/MarketNuggets", "category": "Commodities & Energy"},
    {"name": "Kitco Silver", "url": "https://www.kitco.com/rss/silver.xml", "category": "Commodities & Energy"},
    {"name": "MarketWatch Oil", "url": "http://feeds.marketwatch.com/marketwatch/marketpulse/", "category": "Commodities & Energy"},
    {"name": "MetalBulletin", "url": "https://www.metalbulletin.com/Article/Feed", "category": "Commodities & Energy"},
    {"name": "National Observer Energy", "url": "https://nationalobserver.com/feed/", "category": "Commodities & Energy"},
    {"name": "Oil & Gas 360", "url": "https://www.oilandgas360.com/feed/", "category": "Commodities & Energy"},
    {"name": "OilPrice", "url": "https://oilprice.com/rss/main", "category": "Commodities & Energy"},
    {"name": "Reuters Commodities", "url": "http://feeds.reuters.com/reuters/commoditiesNews", "category": "Commodities & Energy"},
    {"name": "Rigzone", "url": "https://www.rigzone.com/news/rss/rigzone_latest.aspx", "category": "Commodities & Energy"},
    {"name": "S&P Global Oil", "url": "https://www.spglobal.com/commodityinsights/en/rss-feed/oil", "category": "Commodities & Energy"},
    {"name": "SP Global Commodities", "url": "https://www.spglobal.com/commodityinsights/en/rss/rss.xml", "category": "Commodities & Energy"},
    # --- Housing Market ---
    {"name": "CaseShiller", "url": "https://www.spglobal.com/spdji/en/index-family/indicators/sp-corelogic-case-shiller/rss.xml", "category": "Housing Market"},
    {"name": "CoreLogic", "url": "https://www.corelogic.com/intelligence/feed/", "category": "Housing Market"},
    {"name": "HousingWire", "url": "https://www.housingwire.com/rss/", "category": "Housing Market"},
    {"name": "HousingWire Daily", "url": "https://feeds.buzzsprout.com/989209.rss", "category": "Housing Market"},
    {"name": "MBA Mortgage", "url": "https://www.mba.org/news/rss", "category": "Housing Market"},
    {"name": "Mortgage News Daily", "url": "https://www.mortgagenewsdaily.com/rss/news", "category": "Housing Market"},
    {"name": "NAHB Builders", "url": "https://www.nahb.org/news/rss", "category": "Housing Market"},
    {"name": "NAR Housing", "url": "https://www.nar.realtor/rss/news", "category": "Housing Market"},
    {"name": "Realtor News", "url": "https://www.realtor.com/news/feed/", "category": "Housing Market"},
    {"name": "Redfin", "url": "https://www.redfin.com/blog/feed/", "category": "Housing Market"},
    {"name": "Zillow Research", "url": "https://www.zillow.com/research/feed/", "category": "Housing Market"},
    # --- Crypto & Forex ---
    {"name": "BeInCrypto", "url": "https://beincrypto.com/feed/", "category": "Crypto & Forex"},
    {"name": "Bitcoin Magazine", "url": "https://bitcoinmagazine.com/.rss/full/", "category": "Crypto & Forex"},
    {"name": "CoinDesk", "url": "https://www.coindesk.com/arc/outboundfeeds/rss/", "category": "Crypto & Forex"},
    {"name": "CoinTelegraph", "url": "https://cointelegraph.com/rss", "category": "Crypto & Forex"},
    {"name": "Crunchbase Fintech", "url": "https://news.crunchbase.com/feed/", "category": "Crypto & Forex"},
    {"name": "CryptoNews", "url": "https://cryptonews.com/news/feed/", "category": "Crypto & Forex"},
    {"name": "CryptoSlate", "url": "https://cryptoslate.com/feed/", "category": "Crypto & Forex"},
    {"name": "DailyFX", "url": "https://rss.dailyfx.com/feeds/all", "category": "Crypto & Forex"},
    {"name": "FXStreet", "url": "https://www.fxstreet.com/rss/news", "category": "Crypto & Forex"},
    {"name": "Forex Factory", "url": "https://www.forexfactory.com/rss.php", "category": "Crypto & Forex"},
    {"name": "Reuters Forex", "url": "http://feeds.reuters.com/reuters/currenciesNews", "category": "Crypto & Forex"},
    {"name": "TheBlock", "url": "https://www.theblockcrypto.com/rss.xml", "category": "Crypto & Forex"},
    # --- Business & Corporate ---
    {"name": "Bloomberg Companies", "url": "https://feeds.bloomberg.com/company/news.rss", "category": "Business & Corporate"},
    {"name": "CNBC Earnings", "url": "https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839135", "category": "Business & Corporate"},
    {"name": "Earnings Whispers", "url": "https://www.earningswhispers.com/rss", "category": "Business & Corporate"},
    {"name": "MarketWatch Earnings", "url": "http://feeds.marketwatch.com/marketwatch/earningswatch/", "category": "Business & Corporate"},
    {"name": "Reuters Business", "url": "http://feeds.reuters.com/reuters/businessNews", "category": "Business & Corporate"},
    {"name": "SEC EDGAR", "url": "https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&output=atom", "category": "Business & Corporate"},
    {"name": "Seeking Alpha Earnings", "url": "https://seekingalpha.com/earnings/earnings-call-transcripts.xml", "category": "Business & Corporate"},
    {"name": "WSJ Business", "url": "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml", "category": "Business & Corporate"},
    {"name": "Zacks Earnings", "url": "https://www.zacks.com/rss/earnings-check-rss.xml", "category": "Business & Corporate"},
    # --- World News ---
    {"name": "14ymedio", "url": "https://www.14ymedio.com/rss/", "category": "World News"},
    {"name": "404 Media", "url": "https://404media.co/feed/", "category": "World News"},
    {"name": "BBC Africa", "url": "https://feeds.bbci.co.uk/news/world/africa/rss.xml", "category": "World News"},
    {"name": "BBC Asia", "url": "https://feeds.bbci.co.uk/news/world/asia/rss.xml", "category": "World News"},
    {"name": "BBC Latin America", "url": "https://feeds.bbci.co.uk/news/world/latin_america/rss.xml", "category": "World News"},
    {"name": "CNN Top Stories", "url": "http://rss.cnn.com/rss/cnn_topstories.rss", "category": "World News"},
    {"name": "Democracy Now", "url": "https://www.democracynow.org/democracynow.rdf", "category": "World News"},
    {"name": "FoxNews Politics", "url": "http://feeds.foxnews.com/foxnews/politics", "category": "World News"},
    {"name": "La Silla Vacía", "url": "https://www.lasillavacia.com/rss", "category": "World News"},
    {"name": "NPR News", "url": "https://feeds.npr.org/1001/rss.xml", "category": "World News"},
    {"name": "NYTimes Homepage", "url": "http://feeds.nytimes.com/nyt/rss/HomePage", "category": "World News"},
    {"name": "Rest of World", "url": "https://restofworld.org/feed/", "category": "World News"},
    {"name": "Reuters US", "url": "http://feeds.reuters.com/Reuters/domesticNews", "category": "World News"},
    {"name": "USAToday", "url": "http://rssfeeds.usatoday.com/usatoday-NewsTopStories", "category": "World News"},
    {"name": "Vietnam News", "url": "https://vietnamnews.vn/rss", "category": "World News"},
    {"name": "WashingtonPost", "url": "http://feeds.washingtonpost.com/rss/politics", "category": "World News"},
    # --- Europe ---
    {"name": "BBC UK", "url": "http://feeds.bbci.co.uk/news/uk/rss.xml", "category": "Europe"},
    {"name": "BBC World", "url": "http://feeds.bbci.co.uk/news/world/rss.xml", "category": "Europe"},
    {"name": "CEPS Feed", "url": "https://www.ceps.eu/feed/", "category": "Europe"},
    {"name": "CEPS News", "url": "https://www.ceps.eu/news/", "category": "Europe"},
    {"name": "CEPS Publications", "url": "https://www.ceps.eu/ceps-publications/", "category": "Europe"},
    {"name": "DerSpiegel", "url": "https://www.spiegel.de/international/index.rss", "category": "Europe"},
    {"name": "ECFR", "url": "https://ecfr.eu/feeds/", "category": "Europe"},
    {"name": "Guardian UK", "url": "https://www.theguardian.com/uk/rss", "category": "Europe"},
    {"name": "Guardian World", "url": "https://www.theguardian.com/world/rss", "category": "Europe"},
    {"name": "LeMonde", "url": "https://www.lemonde.fr/rss/une.xml", "category": "Europe"},
    {"name": "New Geopolitics", "url": "https://www.newgeopolitics.org/feed/", "category": "Europe"},
    {"name": "Telegraph UK", "url": "https://www.telegraph.co.uk/rss.xml", "category": "Europe"},
    # --- Asia-Pacific ---
    {"name": "China Daily", "url": "http://www.chinadaily.com.cn/rss/world_rss.xml", "category": "Asia-Pacific"},
    {"name": "Focus Taiwan", "url": "https://focustaiwan.tw/rss/news.xml", "category": "Asia-Pacific"},
    {"name": "Japan Times", "url": "https://www.japantimes.co.jp/feed", "category": "Asia-Pacific"},
    {"name": "Nikkei Asia", "url": "https://asia.nikkei.com/rss/feed/nar", "category": "Asia-Pacific"},
    {"name": "SCMP", "url": "https://www.scmp.com/rss/91/feed", "category": "Asia-Pacific"},
    {"name": "Times India", "url": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "category": "Asia-Pacific"},
    {"name": "University of South Pacific", "url": "https://www.usp.ac.fj/feed/", "category": "Asia-Pacific"},
    # --- Geopolitics & Security ---
    {"name": "Airforce Technology", "url": "https://www.airforce-technology.com/rss/", "category": "Geopolitics & Security"},
    {"name": "Atlantic Council", "url": "https://www.atlanticcouncil.org/feed/", "category": "Geopolitics & Security"},
    {"name": "Brookings", "url": "https://www.brookings.edu/feed/", "category": "Geopolitics & Security"},
    {"name": "CFR Global", "url": "https://www.cfr.org/rss/feeds", "category": "Geopolitics & Security"},
    {"name": "CSIS Analysis", "url": "https://www.csis.org/rss.xml", "category": "Geopolitics & Security"},
    {"name": "Defense News", "url": "https://www.defensenews.com/home/rss.xml", "category": "Geopolitics & Security"},
    {"name": "Foreign Affairs", "url": "https://www.foreignaffairs.com/rss.xml", "category": "Geopolitics & Security"},
    {"name": "Naval Today", "url": "https://navaltoday.com/feed/", "category": "Geopolitics & Security"},
    {"name": "Stratfor", "url": "https://worldview.stratfor.com/rss.xml", "category": "Geopolitics & Security"},
    {"name": "War on Rocks", "url": "https://warontherocks.com/feed/", "category": "Geopolitics & Security"},
    {"name": "Wilson Center", "url": "https://www.wilsoncenter.org/rss-feeds", "category": "Geopolitics & Security"},
    # --- Crisis Indicators ---
    {"name": "BIS News", "url": "https://www.bis.org/doclist/cbspeeches.rss", "category": "Crisis Indicators"},
    {"name": "CBOE VIX", "url": "https://www.cboe.com/rss/blog", "category": "Crisis Indicators"},
    {"name": "FRED Crisis", "url": "https://fred.stlouisfed.org/tags/series?t=financial+crisis&ob=pv&od=desc/rss", "category": "Crisis Indicators"},
    {"name": "Fear & Greed CNN", "url": "https://money.cnn.com/data/fear-and-greed/rss", "category": "Crisis Indicators"},
    {"name": "Financial Stress", "url": "https://www.clevelandfed.org/rss/indicators", "category": "Crisis Indicators"},
    {"name": "GDACS", "url": "https://www.gdacs.org/xml/rss.xml", "category": "Crisis Indicators"},
    {"name": "IMF Financial", "url": "https://www.imf.org/en/News/RSS?Language=ENG", "category": "Crisis Indicators"},
    {"name": "Market Insider", "url": "https://markets.businessinsider.com/rss/news", "category": "Crisis Indicators"},
    {"name": "Safety4Sea", "url": "https://www.safety4sea.com/feed/", "category": "Crisis Indicators"},
    {"name": "Seeking Alpha Market", "url": "https://seekingalpha.com/market_currents.xml", "category": "Crisis Indicators"},
    {"name": "Volatility Report", "url": "https://www.volatilityreport.com/feed/", "category": "Crisis Indicators"},
    {"name": "ZeroHedge", "url": "https://feeds.feedburner.com/zerohedge/feed", "category": "Crisis Indicators"},
    # --- Health & Medical ---
    {"name": "BBC Health", "url": "https://feeds.bbci.co.uk/news/health/rss.xml", "category": "Health & Medical"},
    {"name": "BioWorld Canada", "url": "https://www.bioworld.com/rss/27", "category": "Health & Medical"},
    {"name": "BioWorld Digital Health", "url": "https://www.bioworld.com/rss/topic/439-health-canada", "category": "Health & Medical"},
    {"name": "Express Pharma", "url": "https://www.expresspharma.in/rss", "category": "Health & Medical"},
    {"name": "Medscape News", "url": "https://www.medscape.com/cx/rssfeeds/2672-news.xml", "category": "Health & Medical"},
    # --- Cybersecurity ---
    {"name": "Dark Reading", "url": "https://www.darkreading.com/rss.xml", "category": "Cybersecurity"},
    {"name": "Decent Cybersecurity", "url": "https://decentcybersecurity.eu/feed/", "category": "Cybersecurity"},
    {"name": "Krebs on Security", "url": "https://krebsonsecurity.com/feed/", "category": "Cybersecurity"},
    {"name": "The Hacker News", "url": "https://feeds.feedburner.com/TheHackersNews", "category": "Cybersecurity"},
    # --- Maritime & Supply Chain ---
    {"name": "FreightWaves", "url": "https://www.freightwaves.com/news/feed", "category": "Maritime & Supply Chain"},
    {"name": "Lloyd's List", "url": "https://lloydslist.com/rss", "category": "Maritime & Supply Chain"},
    {"name": "Logistics Business", "url": "https://logisticsbusiness.com/feed/", "category": "Maritime & Supply Chain"},
    {"name": "Maritime Executive", "url": "https://www.maritime-executive.com/rss", "category": "Maritime & Supply Chain"},
    {"name": "Splash247", "url": "https://splash247.com/feed/", "category": "Maritime & Supply Chain"},
    {"name": "TradeWinds", "url": "https://www.tradewindsnews.com/rss", "category": "Maritime & Supply Chain"},
    {"name": "gCaptain", "url": "https://gcaptain.com/feed/", "category": "Maritime & Supply Chain"},
    # --- Agriculture ---
    {"name": "AgroDep", "url": "http://agrodep.org/feed/", "category": "Agriculture"},
    {"name": "FiBL Organic Agriculture", "url": "https://www.fibl.org/rss", "category": "Agriculture"},
    {"name": "USDA ERS", "url": "https://www.ers.usda.gov/rss-info/", "category": "Agriculture"},
    # --- Legal & Regulatory ---
    {"name": "CFPB Newsroom", "url": "https://www.consumerfinance.gov/about-us/newsroom/rss/", "category": "Legal & Regulatory"},
    {"name": "Congress.gov API", "url": "https://api.congress.gov/v3/bill", "category": "Legal & Regulatory"},
    {"name": "Law360", "url": "https://feeds.law360.com/news", "category": "Legal & Regulatory"},
    {"name": "SEC Press Releases", "url": "https://www.sec.gov/news/pressreleases.rss", "category": "Legal & Regulatory"},
    # --- Quality of Life ---
    {"name": "Global Health", "url": "https://www.globalhealthnow.org/rss", "category": "Quality of Life"},
    {"name": "HDI Index", "url": "https://hdr.undp.org/rss", "category": "Quality of Life"},
    {"name": "Happiness Report", "url": "https://worldhappiness.report/feed/", "category": "Quality of Life"},
    {"name": "OECD Better Life", "url": "https://www.oecd.org/social/rss", "category": "Quality of Life"},
    {"name": "UN Development", "url": "https://www.undp.org/rss", "category": "Quality of Life"},
    {"name": "Urban Institute", "url": "https://www.urban.org/rss/all", "category": "Quality of Life"},
    {"name": "WHO Health", "url": "https://www.who.int/rss-feeds/news-english.xml", "category": "Quality of Life"},
    {"name": "World Bank Development", "url": "https://blogs.worldbank.org/rss.xml", "category": "Quality of Life"},
]


def get_preset_feeds() -> List[Dict[str, str]]:
    """Returns a copy of the full preset feed catalog."""
    return [dict(feed) for feed in PRESET_FEEDS]


def get_preset_categories() -> List[str]:
    """Returns an ordered copy of all preset categories."""
    return list(PRESET_CATEGORIES)


def get_presets_by_category(category: str) -> List[Dict[str, str]]:
    """Returns all preset feeds matching a category (case-insensitive)."""
    cat = (category or "").strip().lower()
    if not cat or cat == "all" or cat == "all categories":
        return get_preset_feeds()
    return [
        dict(feed)
        for feed in PRESET_FEEDS
        if (feed.get("category") or "").strip().lower() == cat
    ]


def search_presets(query: str) -> List[Dict[str, str]]:
    """Returns preset feeds whose name/url/category match a text query."""
    q = (query or "").strip().lower()
    if not q:
        return get_preset_feeds()
    return [
        dict(feed)
        for feed in PRESET_FEEDS
        if q in (feed.get("name") or "").lower()
        or q in (feed.get("url") or "").lower()
        or q in (feed.get("category") or "").lower()
    ]


def feed_already_present(preset: Dict[str, str], existing: List[Dict[str, Any]] = None) -> bool:
    """Returns True if a preset URL/name already exists in the active feed list."""
    if existing is None:
        return False
    preset_url = (preset.get("url") or "").strip().rstrip("/")
    preset_name = (preset.get("name") or "").strip().lower()
    for feed in existing:
        feed_url = (feed.get("url") or "").strip().rstrip("/")
        feed_name = (feed.get("name") or "").strip().lower()
        if feed_url == preset_url or feed_name == preset_name:
            return True
    return False
