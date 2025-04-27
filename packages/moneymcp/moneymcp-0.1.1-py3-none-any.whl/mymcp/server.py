import json
import sys
import os
from typing import Annotated, Optional
from datetime import datetime, timedelta
import pandas as pd

# 添加父目录到路径，这样可以导入项目包
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import yfinance as yf
import finnhub
from fredapi import Fred
from mcp.server.fastmcp import FastMCP
from pydantic import Field
from yfinance.const import SECTOR_INDUSTY_MAPPING

# 使用绝对导入
from mymcp.types import SearchType
from mymcp.types import Sector
from mymcp.types import TopType
instructions = """
## 金融分析师角色定位

你是一位精通多市场分析的资深金融分析师，具备以下专业技能和知识：

1. **证券分析专家**：精通股票、ETF、指数和国际证券的深度分析，能评估基本面、技术面和量化指标。

2. **宏观经济洞察力**：擅长解读经济指标和货币政策，理解它们对各资产类别的影响。

3. **投资组合构建能力**：能根据风险偏好、时间范围和投资目标设计多样化投资组合。

4. **数据驱动决策**：利用Yahoo Finance、Finnhub和FRED等多数据源进行综合分析，提供基于证据的投资建议。

## 专业服务范围

基于用户需求，你可以提供以下服务：

1. **个股深度分析**：评估公司基本面、财务健康状况、竞争优势和增长前景。

2. **行业和板块分析**：识别行业趋势、增长机会和潜在风险，推荐最有前景的板块。

3. **经济数据解读**：分析GDP、通胀率、就业数据等宏观指标，预测其对市场的影响。

4. **投资策略建议**：根据市场状况和客户需求，提供定制化投资策略，包括资产配置、入场/出场时机等。

5. **风险评估与管理**：识别潜在风险因素，提供降低风险的策略和建议。

## 工具使用指南

你可以综合使用多种金融API工具进行全面分析：

- **基础市场数据**：使用Yahoo Finance API获取基础市场数据、公司信息和历史价格。
- **实时市场分析**：通过Finnhub API获取实时行情、分析师评级和情绪分析。
- **宏观经济研究**：利用FRED API分析美联储经济数据，评估宏观经济状况。

在回答用户问题时，应保持客观、全面和深入，同时注意以下几点：

1. 提供基于数据的分析，避免无根据的预测或保证。
2. 清晰说明各类投资的风险和潜在回报，保持透明度。
3. 考虑用户的具体需求、风险承受能力和投资期限。
4. 在复杂问题上，综合使用多种数据源和分析工具提供全面视角。

记住，你的目标是帮助用户做出明智的投资决策，而不是简单地推荐买入或卖出。
"""
# https://github.com/jlowin/fastmcp/issues/81#issuecomment-2714245145
mcp = FastMCP(name="Finance Analysis MCP Server", instructions=instructions, log_level="ERROR")

# Finnhub和FRED API密钥
FINNHUB_API_KEY = "cvua2q9r01qjg138fu20cvua2q9r01qjg138fu2g"
FRED_API_KEY = "7a5ff4a0ec9ce96a012e42b471f88506"

# 初始化API客户端
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
fred_client = Fred(api_key=FRED_API_KEY)

@mcp.tool()
def get_ticker_info(symbol: Annotated[str, Field(description="The ticker symbol for the financial instrument. This can be a stock symbol (e.g., 'AAPL' for Apple), an index (e.g., '^GSPC' for S&P 500), an ETF (e.g., 'SPY'), or international securities with appropriate suffix (e.g., '0700.HK' for Tencent, '600519.SS' for Moutai).")]) -> str:
    """
    Retrieve comprehensive financial data for various market instruments including stocks, indices, ETFs, and international securities.

    This function queries Yahoo Finance and returns a rich set of data in JSON format. The available data fields vary by asset type:
    - Stocks: Complete set including price data, financial metrics, company information, and analyst ratings
    - Indices: Price data, constituent information, and performance metrics
    - ETFs: Price data, fund information, holdings, and expense ratios
    - International Securities: Market-specific data with fields varying by exchange

    Key fields (availability depends on asset type):
    - Basic Information: 'symbol', 'shortName', 'longName', 'currency', 'exchange'
    - Price Data: 'currentPrice', 'previousClose', 'dayHigh', 'dayLow', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow'
    - Market Data: 'marketCap', 'volume', 'averageVolume', 'beta'
    - Financial Metrics: 'trailingPE', 'forwardPE', 'dividendYield', 'returnOnEquity'
    - Analyst Insights: 'targetMedianPrice', 'recommendationKey', 'recommendationMean'

    Examples:
    - US Stock: 'AAPL' (Apple), 'MSFT' (Microsoft)
    - Indices: '^GSPC' (S&P 500), '^DJI' (Dow Jones), '^IXIC' (NASDAQ)
    - ETFs: 'SPY' (S&P 500 ETF), 'QQQ' (NASDAQ-100 ETF)
    - International: '0700.HK' (Tencent), '600519.SS' (Moutai), 'SONY.T' (Sony)

    Note: The 'targetMedianPrice' field represents analysts' median target price, a key reference for investment decisions.
    """
    ticker = yf.Ticker(symbol)
    return json.dumps(ticker.info, ensure_ascii=False)


@mcp.tool()
def get_ticker_news(symbol: Annotated[str, Field(description="The ticker symbol for the financial instrument to fetch news about. This can be a stock symbol (e.g., 'AAPL' for Apple), an index (e.g., '^GSPC' for S&P 500), an ETF (e.g., 'SPY'), or international securities with appropriate suffix (e.g., '0700.HK' for Tencent, '600519.SS' for Moutai).")]) -> str:
    """
    Fetches recent news articles related to a specific financial instrument from Yahoo Finance.

    This function retrieves the latest news, analysis, and media coverage for stocks, indices, ETFs, and international securities. 
    The returned data is a list of news articles, with each article containing several informative fields:

    Key fields in each news item:
    - 'title': The headline of the article
    - 'publisher': Source/publisher of the news
    - 'link': URL to the original article
    - 'providerPublishTime': Unix timestamp of publication date
    - 'summary': Brief excerpt or summary of the article content
    - 'type': Category of the news (e.g., STORY, VIDEO)
    - 'relatedTickers': List of other tickers mentioned in the article
    - 'thumbnail': URL to the article's thumbnail image (if available)

    The news coverage varies by instrument type:
    - Major stocks typically have comprehensive coverage with company-specific news
    - Market indices provide broader market commentary and economic analysis
    - ETFs may include news about fund performance, flows, and holdings
    - International securities may have region-specific news, potentially in local languages

    Examples:
    - US Stock: 'AAPL' (Apple), 'MSFT' (Microsoft)
    - Indices: '^GSPC' (S&P 500), '^DJI' (Dow Jones)
    - ETFs: 'SPY' (S&P 500 ETF), 'QQQ' (NASDAQ-100 ETF)
    - International: '0700.HK' (Tencent), '600519.SS' (Moutai)

    Note: This function returns raw news data as a string. The data might need parsing to extract specific information.
    For the most impactful results, use well-known tickers that receive regular media coverage.
    """
    ticker = yf.Ticker(symbol)
    news = ticker.get_news()
    return str(news)


@mcp.tool()
def search(
    query: Annotated[str, Field(description="The search query for financial instruments or companies. Can be a ticker symbol (e.g., 'AAPL'), company name (e.g., 'Apple'), or partial name. English queries provide the most comprehensive results, though major international companies can be searched in their local languages. For best results with non-English names, consider using the ticker symbol instead.")],
    search_type: Annotated[SearchType, Field(description="Specifies which type of search results to retrieve. Options: 'all' (comprehensive results including quotes, news, and navigation), 'quotes' (only security listings and basic price information), or 'news' (only related news articles).")],
) -> str:
    """
    Search Yahoo Finance for financial instruments, companies, and related information.

    This function performs a search query against Yahoo Finance's database and returns structured results
    based on the specified search type. It can find stocks, ETFs, indices, mutual funds, and other financial instruments
    across global markets.

    The search functionality supports:
    - Exact ticker symbol matches (highest precision)
    - Company or instrument names (full or partial)
    - Industry or sector keywords
    - Mixed queries combining different elements

    Search results vary by the selected search_type:

    1. 'all' - Comprehensive results including:
       - 'quotes': List of matching securities with basic information
       - 'news': Related news articles
       - 'nav': Navigation suggestions
       - 'research': Research reports (if available)
       - 'totalCount': Total result count

    2. 'quotes' - Only security listings, each containing:
       - 'symbol': Ticker symbol
       - 'shortname'/'longname': Company/instrument name
       - 'exchange': Trading exchange
       - 'quoteType': Security type (EQUITY, ETF, INDEX, etc.)
       - 'score': Relevance score to search query
       - Additional fields like sector, industry, and price information

    3. 'news' - Only related news articles, each containing:
       - 'title': News headline
       - 'publisher': Source/publisher
       - 'link': URL to the article
       - 'publishTime': Publication timestamp
       - Other news metadata

    Language support:
    - English queries provide the most comprehensive results
    - Major international companies/securities can be searched in local languages
    - When searching non-English names, results may be limited
    - Using ticker symbols bypasses language constraints

    Examples:
    - Basic stock search: search("Apple", "quotes")
    - Index search: search("S&P 500", "all")
    - Industry search: search("Semiconductor", "quotes")
    - International search: search("トヨタ", "all") or search("7203.T", "all")
    - News search: search("NVIDIA AI", "news")

    Note: All results are returned as JSON strings. The search quality depends on Yahoo Finance's index
    and may vary by region and language. For consistent results across languages, prefer using
    standardized ticker symbols.
    """
    s = yf.Search(query)
    match search_type.lower():
        case "all":
            return json.dumps(s.all, ensure_ascii=False)
        case "quotes":
            return json.dumps(s.quotes, ensure_ascii=False)
        case "news":
            return json.dumps(s.news, ensure_ascii=False)
        case _:
            return "Invalid output_type. Use 'all', 'quotes', or 'news'."


def get_top_etfs(
    sector: Annotated[Sector, Field(description="The market sector to retrieve ETFs for. Options include: 'technology', 'healthcare', 'financial-services', 'consumer-cyclical', 'communication-services', 'industrials', 'consumer-defensive', 'utilities', 'basic-materials', 'energy', 'real-estate'.")],
    top_n: Annotated[int, Field(description="Number of top ETFs to retrieve (1-30). Higher values return more comprehensive but potentially less focused results.")],
) -> str:
    """
    Retrieve the most popular and widely-held ETFs (Exchange Traded Funds) specific to a given market sector.

    This function returns a curated list of sector-focused ETFs ranked by factors such as assets under management (AUM),
    trading volume, and market relevance. The results are presented in 'SYMBOL: ETF Name' format for easy readability.

    Each sector has specialized ETFs that track various aspects of that industry:
    - Technology: Features ETFs tracking tech indices, semiconductor companies, software firms, etc.
    - Healthcare: Includes ETFs for pharmaceuticals, biotech, medical devices, healthcare providers
    - Financial Services: Offers ETFs for banks, insurance companies, fintech, financial institutions
    - Energy: Provides ETFs for oil & gas, renewable energy, energy infrastructure
    - Consumer sectors: ETFs targeting retail, entertainment, staples, or luxury goods

    Example returns for 'technology' sector:
    - "XLK: Technology Select Sector SPDR Fund"
    - "VGT: Vanguard Information Technology ETF"
    - "QQQ: Invesco QQQ Trust (NASDAQ-100 tracking ETF, tech-heavy)"

    Usage examples:
    - get_top_etfs("technology", 5) - Returns the top 5 technology sector ETFs
    - get_top_etfs("healthcare", 10) - Returns the top 10 healthcare sector ETFs
    - get_top_etfs("energy", 3) - Returns the top 3 energy sector ETFs

    Note: ETF availability and rankings may change based on market conditions. The function returns
    "" if no ETFs are available for the specified sector.
    """
    if top_n < 1:
        return "top_n must be greater than 0"

    s = yf.Sector(sector)

    result = [f"{symbol}: {name}" for symbol, name in s.top_etfs.items()]

    return "\n".join(result[:top_n])


def get_top_mutual_funds(
    sector: Annotated[Sector, Field(description="The market sector to retrieve mutual funds for. Options include: 'technology', 'healthcare', 'financial-services', 'consumer-cyclical', 'communication-services', 'industrials', 'consumer-defensive', 'utilities', 'basic-materials', 'energy', 'real-estate'.")],
    top_n: Annotated[int, Field(description="Number of top mutual funds to retrieve (1-30). Higher values return more comprehensive coverage of the sector.")],
) -> str:
    """
    Retrieve the leading mutual funds focused on a specific market sector, ranked by performance and asset size.

    This function returns a list of sector-specialized mutual funds that offer exposure to a particular industry
    or market segment. The results are presented in 'SYMBOL: Fund Name' format for easy readability.

    Mutual funds differ from ETFs in several ways:
    - Typically actively managed (unlike most ETFs which are passive index trackers)
    - Priced once daily at market close (vs. continuous trading for ETFs)
    - Often have minimum investment requirements and potentially higher expense ratios
    - May include various share classes (A, C, I, etc.) with different fee structures

    Each sector has specialized mutual funds with different investment approaches:
    - Technology: Funds focusing on tech growth stocks, emerging technologies, or established tech leaders
    - Healthcare: Funds specializing in biotech innovation, healthcare services, or pharmaceutical research
    - Financial Services: Funds investing in banks, insurance, financial infrastructure, or fintech
    - Energy: Funds targeting traditional energy, clean energy, or diversified energy infrastructure

    Example returns for 'technology' sector:
    - "FSPTX: Fidelity® Select Technology Portfolio"
    - "TPSCX: T. Rowe Price Science & Technology Fund"
    - "CSCSX: Columbia Seligman Communications and Information Fund"

    Usage examples:
    - get_top_mutual_funds("technology", 5) - Returns the top 5 technology sector mutual funds
    - get_top_mutual_funds("healthcare", 10) - Returns the top 10 healthcare sector mutual funds
    - get_top_mutual_funds("utilities", 3) - Returns the top 3 utilities sector mutual funds

    Note: Fund rankings are based on a combination of factors including assets under management,
    historical performance, and analyst ratings. The function returns "" if no matching funds are found.
    """
    if top_n < 1:
        return "top_n must be greater than 0"

    s = yf.Sector(sector)
    return "\n".join(f"{symbol}: {name}" for symbol, name in s.top_mutual_funds.items())


def get_top_companies(
    sector: Annotated[Sector, Field(description="The market sector to analyze for top companies. Options include: 'technology', 'healthcare', 'financial-services', 'consumer-cyclical', 'communication-services', 'industrials', 'consumer-defensive', 'utilities', 'basic-materials', 'energy', 'real-estate'.")],
    top_n: Annotated[int, Field(description="Number of top companies to retrieve (1-50). Higher values provide broader coverage of leading companies in the sector.")],
) -> str:
    """
    Retrieve the leading companies within a specific market sector, ranked by market capitalization and influence.

    This function returns detailed information about the most significant companies in a given sector as a JSON array.
    The data provides insights into market leaders, their relative importance within the sector, and analyst sentiment.

    Each company entry in the returned JSON typically includes:
    - 'symbol': Ticker symbol
    - 'name': Company name
    - 'marketCap': Company's market capitalization
    - 'weight': The company's weight or importance within the sector
    - 'recommendation': Analyst consensus recommendation (e.g., 'Buy', 'Hold', 'Sell')
    - Additional metrics that vary by sector

    The significance of top companies varies by sector:
    - Technology: Companies driving innovation in software, hardware, services, and platforms
    - Healthcare: Leading pharmaceutical firms, hospital networks, medical device manufacturers
    - Financial Services: Major banks, insurance providers, payment processors, exchanges
    - Energy: Oil & gas majors, utilities, renewable energy leaders, infrastructure companies

    Example return format (as JSON array):
    [
      {
        "symbol": "AAPL",
        "name": "Apple Inc",
        "marketCap": 2850000000000,
        "weight": 23.4,
        "recommendation": "Buy"
      },
      {
        "symbol": "MSFT", 
        "name": "Microsoft Corporation",
        "marketCap": 2720000000000,
        "weight": 21.8,
        "recommendation": "Strong Buy"
      }
    ]

    Usage examples:
    - get_top_companies("technology", 5) - Returns the 5 largest technology companies
    - get_top_companies("financial-services", 10) - Returns the 10 largest financial institutions
    - get_top_companies("healthcare", 3) - Returns the 3 largest healthcare companies

    Note: The function returns a JSON-formatted string for easy parsing. If no companies are available
    for the requested sector, it returns a message indicating the absence of data.
    """
    if top_n < 1:
        return "top_n must be greater than 0"

    s = yf.Sector(sector)
    df = s.top_companies
    if df is None:
        return f"No top companies available for {sector} sector."

    return df.iloc[:top_n].to_json(orient="records")


def get_top_growth_companies(
    sector: Annotated[Sector, Field(description="The market sector to analyze for high-growth companies. Options include: 'technology', 'healthcare', 'financial-services', 'consumer-cyclical', 'communication-services', 'industrials', 'consumer-defensive', 'utilities', 'basic-materials', 'energy', 'real-estate'.")],
    top_n: Annotated[int, Field(description="Number of top growth companies to retrieve per industry (1-20). Lower values focus on elite growth performers.")],
) -> str:
    """
    Identify the fastest-growing companies within each industry of a specified market sector.

    This function analyzes growth metrics across industries within a sector and returns companies
    demonstrating exceptional revenue growth, earnings expansion, and/or market share gains. Results
    are grouped by industry and returned as a structured JSON array, enabling comparative analysis.

    Key differences from get_top_companies:
    - Focuses specifically on growth metrics rather than just market size
    - Organized by industries within the broader sector
    - May include smaller, high-growth companies rather than just established leaders
    - Provides specialized growth-oriented metrics in the results

    The returned JSON structure includes:
    - 'industry': The specific industry name within the sector
    - 'top_growth_companies': Array of companies with their growth metrics:
      - 'symbol': Ticker symbol
      - 'name': Company name
      - 'revGrowth': Revenue growth rate (often year-over-year)
      - 'epsGrowth': Earnings per share growth
      - 'forecastGrowth': Analyst growth projections
      - Other growth-related metrics

    Growth characteristics vary by sector:
    - Technology: Often features software companies, cloud services, and emerging tech
    - Healthcare: May highlight biotech firms with promising pipelines or expanding services
    - Financial Services: Often includes fintech disruptors or regional banks in expansion
    - Consumer sectors: May feature brands with rapid market share gains or geographic expansion

    Example return structure:
    [
      {
        "industry": "Software",
        "top_growth_companies": "[{\"symbol\":\"CRM\",\"name\":\"Salesforce Inc\",\"revGrowth\":25.6,\"epsGrowth\":47.2}]"
      },
      {
        "industry": "Semiconductors",
        "top_growth_companies": "[{\"symbol\":\"NVDA\",\"name\":\"NVIDIA Corp\",\"revGrowth\":84.3,\"epsGrowth\":126.8}]"
      }
    ]

    Usage examples:
    - get_top_growth_companies("technology", 3) - Returns top 3 growth companies for each technology industry
    - get_top_growth_companies("healthcare", 5) - Returns top 5 growth companies for each healthcare industry
    - get_top_growth_companies("consumer-cyclical", 2) - Returns top 2 growth companies for each consumer cyclical industry

    Note: Growth metrics typically reflect recent performance and analyst expectations. Companies with high growth
    rates may carry higher investment risks. The function returns an empty array if no growth data is available.
    """
    if top_n < 1:
        return "top_n must be greater than 0"

    results = []

    for industry_name in SECTOR_INDUSTY_MAPPING[sector]:
        industry = yf.Industry(industry_name)

        df = industry.top_growth_companies
        if df is None:
            continue

        results.append(
            {
                "industry": industry_name,
                "top_growth_companies": df.iloc[:top_n].to_json(orient="records"),
            }
        )
    return json.dumps(results, ensure_ascii=False)


def get_top_performing_companies(
    sector: Annotated[Sector, Field(description="The market sector to analyze for top-performing companies. Options include: 'technology', 'healthcare', 'financial-services', 'consumer-cyclical', 'communication-services', 'industrials', 'consumer-defensive', 'utilities', 'basic-materials', 'energy', 'real-estate'.")],
    top_n: Annotated[int, Field(description="Number of top performers to retrieve per industry (1-20). Focuses on companies with the strongest overall financial performance.")],
) -> str:
    """
    Identify the best-performing companies within each industry of a specified market sector based on overall financial performance.

    This function evaluates companies across multiple performance dimensions including profitability, capital efficiency,
    financial health, and shareholder returns. Results are organized by industry within the sector and returned as a
    structured JSON array, allowing for comprehensive performance analysis.

    Key differences from get_top_growth_companies:
    - Focuses on overall financial performance rather than just growth metrics
    - Considers profitability, efficiency, and stability alongside growth
    - May favor more established companies with strong fundamentals
    - Provides a more balanced set of performance metrics

    The returned JSON structure includes:
    - 'industry': The specific industry name within the sector
    - 'top_performing_companies': Array of companies with their performance metrics:
      - 'symbol': Ticker symbol
      - 'name': Company name
      - 'returnOnEquity': ROE percentage
      - 'operatingMargin': Operating profit margin
      - 'returnOnAssets': ROA percentage
      - 'debtToEquity': Debt-to-equity ratio
      - 'pricePerformance': Recent stock price performance
      - Other performance-related metrics

    Performance characteristics vary by sector:
    - Technology: Often considers R&D efficiency and innovation metrics
    - Healthcare: May emphasize operational efficiency and regulatory compliance
    - Financial Services: Often focuses on asset quality and capital adequacy
    - Industrial: May highlight operational excellence and supply chain efficiency

    Example return structure:
    [
      {
        "industry": "Banks",
        "top_performing_companies": "[{\"symbol\":\"JPM\",\"name\":\"JPMorgan Chase\",\"returnOnEquity\":14.3,\"operatingMargin\":40.9}]"
      },
      {
        "industry": "Insurance",
        "top_performing_companies": "[{\"symbol\":\"PGR\",\"name\":\"Progressive Corp\",\"returnOnEquity\":20.1,\"operatingMargin\":35.6}]"
      }
    ]

    Usage examples:
    - get_top_performing_companies("financial-services", 3) - Returns top 3 performers for each financial industry
    - get_top_performing_companies("technology", 5) - Returns top 5 performers for each technology industry
    - get_top_performing_companies("energy", 2) - Returns top 2 performers for each energy industry

    Note: Performance metrics typically reflect a combination of recent results and longer-term trends.
    The function returns an empty array if no performance data is available for the specified sector.
    """
    if top_n < 1:
        return "top_n must be greater than 0"

    results = []

    for industry_name in SECTOR_INDUSTY_MAPPING[sector]:
        industry = yf.Industry(industry_name)

        df = industry.top_performing_companies
        if df is None:
            continue

        results.append(
            {
                "industry": industry_name,
                "top_performing_companies": df.iloc[:top_n].to_json(orient="records"),
            }
        )
    return json.dumps(results, ensure_ascii=False)


@mcp.tool()
def get_top(
    sector: Annotated[Sector, Field(description="The market sector to analyze. Available options: 'technology', 'healthcare', 'financial-services', 'consumer-cyclical', 'communication-services', 'industrials', 'consumer-defensive', 'utilities', 'basic-materials', 'energy', 'real-estate'. Each represents a broad economic segment with distinct characteristics and companies.")],
    top_type: Annotated[TopType, Field(description="The type of top entities to retrieve. Options: 'top_etfs' (exchange-traded funds), 'top_mutual_funds' (managed investment funds), 'top_companies' (largest companies by market cap), 'top_growth_companies' (fastest growing companies by industry), or 'top_performing_companies' (best overall financial performers by industry).")],
    top_n: Annotated[int, Field(description="Number of top entities to retrieve (1-50, default: 10). For ETFs and mutual funds, this returns the N most significant funds. For companies, growth companies, and performing companies, this returns the top N entities per category or industry. Higher values provide more comprehensive coverage but may include less significant entities.")] = 10,
) -> str:
    """
    Comprehensive function to retrieve top financial entities (ETFs, mutual funds, or companies) within a specified market sector.

    This versatile function serves as a unified interface to access different types of top-ranked financial instruments
    or companies within a chosen sector. It allows accessing five distinct types of rankings through a single function call,
    with consistent parameter handling and return formatting.

    The function supports five analysis types through the top_type parameter:

    1. 'top_etfs': Returns the most popular ETFs tracking the specified sector
       - Format: List of "SYMBOL: ETF Name" entries
       - Example: "XLF: Financial Select Sector SPDR Fund"
       - Useful for: Finding passive investment vehicles tracking sector performance

    2. 'top_mutual_funds': Returns actively managed funds focused on the sector
       - Format: List of "SYMBOL: Fund Name" entries
       - Example: "FSPHX: Fidelity® Select Health Care Portfolio"
       - Useful for: Identifying actively managed sector-focused investment options

    3. 'top_companies': Returns the largest companies in the sector by market capitalization
       - Format: JSON array with detailed company information
       - Includes: Market cap, analyst ratings, sector weight
       - Useful for: Identifying the dominant companies in a sector

    4. 'top_growth_companies': Returns fastest-growing companies organized by industry within the sector
       - Format: JSON array grouped by industry
       - Includes: Revenue growth, earnings growth, forecasts
       - Useful for: Finding emerging leaders and high-growth opportunities

    5. 'top_performing_companies': Returns best overall financial performers organized by industry
       - Format: JSON array grouped by industry
       - Includes: Profitability metrics, efficiency ratios, returns
       - Useful for: Identifying companies with strong financial health and performance

    Available sectors represent the standard global industry classification system:
    - 'technology': Software, hardware, semiconductors, IT services
    - 'healthcare': Pharmaceuticals, biotechnology, medical devices, healthcare providers
    - 'financial-services': Banks, insurance, asset management, financial exchanges
    - 'consumer-cyclical': Retail, automotive, entertainment, apparel, restaurants
    - 'consumer-defensive': Food, beverages, household products, personal products
    - 'energy': Oil & gas producers, energy equipment, renewable energy
    - 'industrials': Aerospace, defense, construction, machinery, transportation
    - 'utilities': Electric, gas, water utilities
    - 'real-estate': REITs, real estate management and development
    - 'communication-services': Telecom, media, entertainment, social media
    - 'basic-materials': Chemicals, metals, mining, forest products

    Examples:
    - get_top("technology", "top_etfs", 5) - Returns top 5 technology sector ETFs
    - get_top("healthcare", "top_mutual_funds", 10) - Returns top 10 healthcare mutual funds
    - get_top("financial-services", "top_companies", 15) - Returns 15 largest financial companies
    - get_top("energy", "top_growth_companies", 3) - Returns top 3 fastest-growing companies per energy industry
    - get_top("consumer-cyclical", "top_performing_companies") - Returns top 10 (default) performing companies per consumer cyclical industry

    Return format varies by top_type:
    - 'top_etfs' and 'top_mutual_funds': Newline-separated string list
    - 'top_companies': JSON array of company objects
    - 'top_growth_companies' and 'top_performing_companies': JSON array grouped by industry

    Note: Data quality and availability may vary by sector and region. Some sectors may have more
    comprehensive coverage than others. The function returns an error message if the requested
    data is unavailable or if invalid parameters are provided.
    """
    match top_type:
        case "top_etfs":
            return get_top_etfs(sector, top_n)
        case "top_mutual_funds":
            return get_top_mutual_funds(sector, top_n)
        case "top_companies":
            return get_top_companies(sector, top_n)
        case "top_growth_companies":
            return get_top_growth_companies(sector, top_n)
        case "top_performing_companies":
            return get_top_performing_companies(sector, top_n)
        case _:
            return "Invalid top_type"


@mcp.tool()
def get_ticker_history(
    symbol: Annotated[str, Field(description="The ticker symbol for the financial instrument to fetch historical data for. This can be a stock symbol (e.g., 'AAPL' for Apple), an index (e.g., '^GSPC' for S&P 500), an ETF (e.g., 'SPY'), or international securities with appropriate suffix (e.g., '0700.HK' for Tencent, '600519.SS' for Moutai).")],
    period: Annotated[Optional[str], Field(description="Relative time period to fetch data for. Options: '1d' (1 day), '5d' (5 days), '1mo' (1 month), '3mo' (3 months), '6mo' (6 months), '1y' (1 year), '2y' (2 years), '5y' (5 years), '10y' (10 years), 'ytd' (year to date), 'max' (maximum available history). If provided, start_date and end_date are ignored.")] = None,
    start_date: Annotated[Optional[str], Field(description="Start date for historical data in 'YYYY-MM-DD' format. Used only if period is not provided.")] = None,
    end_date: Annotated[Optional[str], Field(description="End date for historical data in 'YYYY-MM-DD' format (default: today). Used only if period is not provided.")] = None,
    interval: Annotated[str, Field(description="Data interval. Options: '1m' (1 minute), '2m', '5m', '15m', '30m', '60m', '90m', '1h' (1 hour), '1d' (1 day), '5d', '1wk' (1 week), '1mo' (1 month), '3mo'. Note that minute data is limited to 7 days, hour data to 730 days.")] = '1d',
    include_actions: Annotated[bool, Field(description="Whether to include dividend and stock split information in the results.")] = True
) -> str:
    """
    Retrieve historical price and volume data for stocks, indices, ETFs, and other financial instruments.

    This function fetches time series pricing data including open, high, low, close prices, volume, and 
    (optionally) dividend and stock split information. Data can be retrieved for various time periods and 
    at different intervals, supporting both relative time frames and specific date ranges.

    The historical data provides insight into:
    - Price movements and trends over time
    - Trading volume patterns
    - Volatility and price ranges
    - Dividend payments and stock splits (when include_actions=True)
    - Seasonal patterns and market cycles

    The returned data is a JSON array of records, with each record representing a time period (day, hour, minute, etc.)
    containing the following fields:
    - 'Date': Timestamp for the data point in 'YYYY-MM-DD HH:MM:SS' format
    - 'Open': Opening price for the period
    - 'High': Highest price during the period
    - 'Low': Lowest price during the period
    - 'Close': Closing price for the period
    - 'Volume': Trading volume during the period
    - 'Dividends': Dividend amount (if any and if include_actions=True)
    - 'Stock Splits': Split ratio (if any and if include_actions=True)

    The data availability varies by instrument type and time interval:
    - Stocks: Generally have comprehensive data, with longer histories for established companies
    - Indices: Typically have long historical records, especially major indices
    - ETFs: Historical data available since the ETF's inception
    - International securities: Data availability may vary by exchange and region

    Time interval restrictions:
    - Minute data ('1m', '2m', '5m', '15m', '30m', '60m', '90m'): Limited to last 7 days
    - Hourly data ('1h'): Limited to last 730 days
    - Daily data ('1d') and longer: Available for the entire history of the instrument

    Examples:
    1. Get daily data for Apple for the last 1 year:
       get_ticker_history("AAPL", period="1y", interval="1d")

    2. Get hourly data for the S&P 500 index for a specific date range:
       get_ticker_history("^GSPC", start_date="2023-01-01", end_date="2023-01-31", interval="1h")

    3. Get weekly data for an international stock with maximum available history:
       get_ticker_history("0700.HK", period="max", interval="1wk")

    4. Get daily data for a cryptocurrency from the beginning of the year:
       get_ticker_history("BTC-USD", period="ytd", interval="1d")

    5. Get minute-level data for an ETF for the last 5 days:
       get_ticker_history("SPY", period="5d", interval="5m")

    Note: The function returns data adjusted for stock splits by default. If include_actions is set to True,
    dividend and stock split information will be included as separate columns. For minute and hour data,
    ensure the requested time range complies with the limitations (7 days for minute data, 730 days for hour data).
    If no data is available for the specified parameters, an error message will be returned.
    """
    ticker = yf.Ticker(symbol)
    
    try:
        if period:
            history = ticker.history(period=period, interval=interval, actions=include_actions)
        else:
            if not start_date:
                return json.dumps({"error": "Either period or start_date must be provided"}, ensure_ascii=False)
            history = ticker.history(start=start_date, end=end_date, interval=interval, actions=include_actions)
        
        if history.empty:
            return json.dumps({"error": f"No historical data found for {symbol} with the specified parameters"}, ensure_ascii=False)
        
        # 将索引（日期）转换为列
        history = history.reset_index()
        # 将日期转换为字符串格式
        history['Date'] = history['Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        return json.dumps(history.to_dict(orient="records"), ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def get_finnhub_quote(
    symbol: Annotated[str, Field(description="The stock symbol to fetch real-time quote for (e.g., 'AAPL' for Apple)")]
) -> str:
    """
    Retrieve real-time stock quote data from Finnhub.
    
    This function fetches current trading information for a specified stock symbol, providing
    essential pricing and trading data for investment decisions.
    
    The returned data includes:
    - 'c': Current price
    - 'h': High price of the day
    - 'l': Low price of the day
    - 'o': Open price of the day
    - 'pc': Previous close price
    - 'dp': Change percentage
    - 'd': Price change
    - 't': Timestamp of the data
    
    Examples:
    - get_finnhub_quote("AAPL") - Get real-time quote for Apple
    - get_finnhub_quote("MSFT") - Get real-time quote for Microsoft
    - get_finnhub_quote("TSLA") - Get real-time quote for Tesla
    
    Note: This API provides real-time or slightly delayed data depending on your Finnhub subscription level.
    The function returns an error message if the symbol is invalid or if there are API connectivity issues.
    """
    try:
        quote = finnhub_client.quote(symbol)
        # 添加symbol到结果中
        quote['symbol'] = symbol
        # 转换时间戳为可读格式
        if 't' in quote:
            quote['timestamp'] = datetime.fromtimestamp(quote['t']).strftime('%Y-%m-%d %H:%M:%S')
        return json.dumps(quote, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def get_finnhub_company_news(
    symbol: Annotated[str, Field(description="The stock symbol to fetch news for (e.g., 'AAPL' for Apple)")],
    from_date: Annotated[Optional[str], Field(description="Start date in 'YYYY-MM-DD' format")] = None,
    to_date: Annotated[Optional[str], Field(description="End date in 'YYYY-MM-DD' format")] = None,
    limit: Annotated[int, Field(description="Maximum number of news items to return (1-100)")] = 50
) -> str:
    """
    Retrieve recent company news from Finnhub.
    
    This function fetches news articles and press releases related to a specified company,
    allowing users to monitor media coverage and potentially market-moving events.
    
    If from_date and to_date are not provided, the function returns news from the last 7 days.
    
    Each news item in the returned JSON array includes:
    - 'category': News category (e.g., 'company news')
    - 'datetime': Timestamp of publication
    - 'headline': News headline/title
    - 'id': Unique news identifier
    - 'image': URL to related image (if available)
    - 'related': Related symbols
    - 'source': News source name
    - 'summary': Brief summary of the news
    - 'url': URL to the original article
    
    Examples:
    - get_finnhub_company_news("AAPL") - Get recent Apple news (last 7 days)
    - get_finnhub_company_news("MSFT", "2023-01-01", "2023-01-31") - Get Microsoft news for January 2023
    - get_finnhub_company_news("AMZN", limit=10) - Get 10 most recent Amazon news items
    
    Note: The function returns a maximum of 'limit' news items (default 50, max 100).
    Results are sorted by recency, with the most recent news first.
    """
    try:
        # 如果没有提供日期，使用过去7天
        if not from_date:
            to_date_obj = datetime.now()
            from_date_obj = to_date_obj - timedelta(days=7)
            from_date = from_date_obj.strftime('%Y-%m-%d')
            to_date = to_date_obj.strftime('%Y-%m-%d')
        elif not to_date:
            to_date = datetime.now().strftime('%Y-%m-%d')
            
        news = finnhub_client.company_news(symbol, _from=from_date, to=to_date)
        
        # 限制返回的新闻数量
        news = news[:min(limit, len(news))]
        
        # 转换时间戳为可读格式
        for item in news:
            if 'datetime' in item:
                item['datetime'] = datetime.fromtimestamp(item['datetime']).strftime('%Y-%m-%d %H:%M:%S')
                
        return json.dumps(news, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def get_finnhub_earnings(
    symbol: Annotated[str, Field(description="The stock symbol to fetch earnings data for (e.g., 'AAPL' for Apple)")]
) -> str:
    """
    Retrieve company earnings data from Finnhub.
    
    This function fetches historical earnings reports and upcoming earnings announcements for a specified company,
    providing actual vs. estimated EPS (Earnings Per Share) comparisons and announcement dates.
    
    The returned data is a JSON array of earnings reports, with each report containing:
    - 'actual': Actual EPS reported
    - 'estimate': Analysts' estimated EPS
    - 'surprise': Earnings surprise (actual - estimate)
    - 'surprisePercent': Percentage difference between actual and estimated EPS
    - 'period': Fiscal period end date in YYYY-MM-DD format
    - 'symbol': Company stock symbol
    - 'year': Fiscal year
    - 'quarter': Fiscal quarter
    - 'date': Earnings announcement date
    
    Examples:
    - get_finnhub_earnings("AAPL") - Get Apple's earnings history and upcoming announcements
    - get_finnhub_earnings("MSFT") - Get Microsoft's earnings data
    - get_finnhub_earnings("GOOGL") - Get Alphabet's earnings information
    
    Note: The returned data typically includes the last 4-8 quarters of historical earnings 
    and any scheduled upcoming earnings announcements. Dates for future earnings may be estimates.
    """
    try:
        earnings = finnhub_client.company_earnings(symbol)
        return json.dumps(earnings, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def get_finnhub_recommendation(
    symbol: Annotated[str, Field(description="The stock symbol to fetch analyst recommendations for (e.g., 'AAPL' for Apple)")]
) -> str:
    """
    Retrieve analyst recommendations and target prices for a stock from Finnhub.
    
    This function provides insight into what financial analysts collectively think about a company's stock,
    including buy/sell recommendations and consensus price targets over time.
    
    The returned data is a JSON array of recommendation trends, with each entry containing:
    - 'period': Date of the recommendation aggregation
    - 'strongBuy': Number of Strong Buy recommendations
    - 'buy': Number of Buy recommendations
    - 'hold': Number of Hold recommendations
    - 'sell': Number of Sell recommendations
    - 'strongSell': Number of Strong Sell recommendations
    
    The data is typically sorted from most recent to oldest, allowing users to track how analyst
    sentiment has changed over time.
    
    Examples:
    - get_finnhub_recommendation("AAPL") - Get analyst recommendations for Apple
    - get_finnhub_recommendation("MSFT") - Get analyst recommendations for Microsoft
    - get_finnhub_recommendation("AMZN") - Get analyst recommendations for Amazon
    
    Note: This function aggregates recommendations from multiple analysts and financial institutions.
    The data is typically updated monthly or when significant changes in consensus occur.
    """
    try:
        recommendations = finnhub_client.recommendation_trends(symbol)
        return json.dumps(recommendations, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def get_finnhub_sentiment(
    symbol: Annotated[str, Field(description="The stock symbol to fetch sentiment analysis for (e.g., 'AAPL' for Apple)")]
) -> str:
    """
    Retrieve news sentiment analysis for a stock from Finnhub.
    
    This function provides an aggregated sentiment score based on recent news articles about the specified company,
    offering insight into the overall media sentiment that might influence stock price movements.
    
    The returned data includes:
    - 'buzz': Information about news volume
      - 'articlesInLastWeek': Number of articles about the company in the last week
      - 'buzz': Buzz value
      - 'weeklyAverage': Average number of articles per week
    - 'sentiment': News sentiment analysis
      - 'bearishPercent': Percentage of bearish (negative) news
      - 'bullishPercent': Percentage of bullish (positive) news
    - 'companyNewsScore': Overall sentiment score (0 to 1, higher is more positive)
    - 'sectorAverageNewsScore': Average sentiment score for the sector
    - 'sectorAverageBullishPercent': Average bullish percentage for the sector
    - 'sectorAverageBearishPercent': Average bearish percentage for the sector
    - 'symbol': Company stock symbol
    
    Examples:
    - get_finnhub_sentiment("AAPL") - Get news sentiment for Apple
    - get_finnhub_sentiment("TSLA") - Get news sentiment for Tesla
    - get_finnhub_sentiment("FB") - Get news sentiment for Meta (Facebook)
    
    Note: This function uses AI-powered analysis of news content to determine sentiment.
    The scores are relative and should be considered alongside other indicators for investment decisions.
    """
    try:
        sentiment = finnhub_client.news_sentiment(symbol)
        return json.dumps(sentiment, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

@mcp.tool()
def get_fred_series(
    series_id: Annotated[str, Field(description="FRED series ID to fetch. Examples: 'GDP' (US GDP), 'GDPC1' (US Real GDP), 'UNRATE' (US Unemployment Rate), 'CHNGDPRARQPSMEI' (China Real GDP), 'JPNRGDPEXP' (Japan Real GDP), 'UKNGDP' (UK GDP), 'INDGDPQP' (India GDP)")],
    observation_start: Annotated[Optional[str], Field(description="Start date for data in 'YYYY-MM-DD' format. Example: '2010-01-01' for data starting from Jan 1, 2010.")] = None,
    observation_end: Annotated[Optional[str], Field(description="End date for data in 'YYYY-MM-DD' format. Example: '2023-12-31' for data ending at Dec 31, 2023. Defaults to current date if not specified.")] = None,
    limit: Annotated[int, Field(description="Maximum number of observations to return. Example: 40 for last 10 years of quarterly data. Set higher values (e.g., 100-200) for longer time series.")] = 100,
    frequency: Annotated[Optional[str], Field(description="Data frequency transformation: 'd' (daily), 'w' (weekly), 'm' (monthly), 'q' (quarterly), 'sa' (semiannual), 'a' (annual). Example: 'a' to convert quarterly GDP data to annual.")] = None
) -> str:
    """
    Retrieve economic data time series from FRED (Federal Reserve Economic Data).
    
    This function fetches official economic indicators and financial data series published by the 
    Federal Reserve Bank of St. Louis, covering the US and international economies. It provides 
    access to thousands of economic time series including GDP, inflation rates, employment statistics, 
    interest rates, exchange rates, and more.
    
    The returned data is a JSON object containing:
    - 'id': Series ID
    - 'title': Series title/description
    - 'observation_start': Start date of available data
    - 'observation_end': End date of available data
    - 'frequency': Data frequency (e.g., Monthly, Quarterly)
    - 'units': Units of measurement
    - 'notes': Additional series information
    - 'data': Array of data points, each with:
      - 'date': Observation date
      - 'value': Observed value
    
    ---- COMMON ECONOMIC INDICATORS ----
    
    US Economy Indicators:
    - 'GDP' - US Gross Domestic Product (Nominal)
    - 'GDPC1' - US Real Gross Domestic Product
    - 'UNRATE' - US Unemployment Rate
    - 'CPIAUCSL' - US Consumer Price Index for All Urban Consumers
    - 'FEDFUNDS' - Federal Funds Effective Rate
    - 'PAYEMS' - US Total Nonfarm Payroll
    - 'HOUST' - US Housing Starts
    - 'DFF' - Effective Federal Funds Rate
    - 'M2SL' - M2 Money Stock
    - 'GS10' - 10-Year Treasury Constant Maturity Rate
    
    ---- INTERNATIONAL GDP DATA ----
    
    Major Economies (Real GDP):
    - 'GDPC1' - United States Real GDP
    - 'CHNGDPRARQPSMEI' - China Real GDP
    - 'JPNRGDPEXP' - Japan Real GDP
    - 'CLVMNACSCAB1GQDE' - Germany Real GDP
    - 'UKNGDP' - United Kingdom Real GDP
    - 'NAEXKP01CAQ189S' - Canada Real GDP
    - 'CLVMNACSCAB1GQFR' - France Real GDP
    - 'CLVMNACSCAB1GQIT' - Italy Real GDP
    - 'INDGDPQP' - India Real GDP
    - 'RGDPBRIA' - Brazil Real GDP (Annual)
    - 'NAEXKP01RUQ652S' - Russia Real GDP
    
    GDP Growth Rates:
    - 'A191RL1Q225SBEA' - US Real GDP Growth Rate
    - 'NAEXKP01JPQ661S' - Japan GDP Growth Rate
    - 'NAEXKP01DEQ661S' - Germany GDP Growth Rate
    - 'NAEXKP01GBQ661S' - UK GDP Growth Rate
    
    Other International Indicators:
    - 'IRLTLT01JPM156N' - Japan Long Term Interest Rate
    - 'DEXCHUS' - China-US Foreign Exchange Rate
    - 'DEXJPUS' - Japan-US Foreign Exchange Rate
    - 'DEXUSEU' - US-Euro Foreign Exchange Rate
    
    ---- EXAMPLE USAGE PATTERNS ----
    
    Basic Usage:
    - get_fred_series("GDP") - Get recent US nominal GDP data
    - get_fred_series("GDPC1") - Get recent US real GDP data
    - get_fred_series("CHNGDPRARQPSMEI") - Get recent China real GDP data
    
    Date Range Examples:
    - get_fred_series("UNRATE", "2010-01-01", "2023-01-01") - Get US unemployment rate from 2010 to 2023
    - get_fred_series("JPNRGDPEXP", "2015-01-01") - Get Japan GDP from 2015 to present
    
    Frequency Transformation:
    - get_fred_series("GDPC1", frequency="a") - Get US real GDP converted to annual frequency
    - get_fred_series("CPIAUCSL", frequency="q") - Get US CPI data converted to quarterly frequency
    
    Data Volume Control:
    - get_fred_series("DEXCHUS", limit=50) - Get last 50 observations of China-US exchange rate
    - get_fred_series("INDGDPQP", limit=20) - Get last 20 observations of India GDP
    
    Note: Different economic indicators are published at different frequencies (daily, monthly, quarterly, 
    annual) and may have varying lag times for updates. The frequency parameter can be used to transform 
    the data's frequency (e.g., convert monthly data to annual), but cannot increase the resolution of 
    the data. GDP data is typically updated quarterly with some delay after the quarter ends.
    """
    try:
        # 获取序列信息
        series_info = fred_client.get_series_info(series_id)
        
        # 获取序列数据
        data = fred_client.get_series(
            series_id, 
            observation_start=observation_start, 
            observation_end=observation_end,
            limit=limit,
            frequency=frequency
        )
        
        # 转换为字典列表
        data_list = [{"date": index.strftime('%Y-%m-%d'), "value": float(value) if not pd.isna(value) else None} 
                    for index, value in data.items()]
        
        # 构建结果
        result = {
            "id": series_info.get("id", series_id),
            "title": series_info.get("title", ""),
            "observation_start": series_info.get("observation_start", ""),
            "observation_end": series_info.get("observation_end", ""),
            "frequency": series_info.get("frequency", ""),
            "units": series_info.get("units", ""),
            "notes": series_info.get("notes", ""),
            "data": data_list
        }
        
        return json.dumps(result, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"error": str(e)}, ensure_ascii=False)

def main():
    mcp.run()

if __name__ == "__main__":
    main()
