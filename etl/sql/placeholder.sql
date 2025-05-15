CREATE TABLE company_overviews (
	company_id INTEGER PRIMARY KEY, 
	symbol TEXT,
	asset_type TEXT,
    "name" TEXT, 
    description TEXT, 
    exchange TEXT,
    currency TEXT,
    sector TEXT,
    industry TEXT,
    web_site TEXT,
    market_cap NUMERIC,
    revenue_per_share NUMERIC,
    profit_margin NUMERIC,
    "52_week_high" NUMERIC,
    "52_week_low" NUMERIC,
    "50_day_moving_average" NUMERIC
);
	

CREATE TABLE daily_stocks_gmab (
	stock_id INTEGER PRIMARY KEY,
	company_id INTEGER REFERENCES company_overviews(company_id),
	"date" TIMESTAMP,
	"open" NUMERIC,
	high NUMERIC,
	low NUMERIC,
    "close" NUMERIC,
    volume NUMERIC
);

CREATE TABLE daily_stocks_argx (
	stock_id INTEGER PRIMARY KEY,
	company_id INTEGER REFERENCES company_overviews(company_id),
	"date" TIMESTAMP,
	"open" NUMERIC,
	high NUMERIC,
	low NUMERIC,
    "close" NUMERIC,
    volume NUMERIC
);

CREATE TABLE daily_stocks_pfe (
	stock_id INTEGER PRIMARY KEY,
	company_id INTEGER REFERENCES company_overviews(company_id),
	"date" TIMESTAMP,
	"open" NUMERIC,
	high NUMERIC,
	low NUMERIC,
    "close" NUMERIC,
    volume NUMERIC
);


CREATE TABLE daily_stocks_gsk (
	stock_id INTEGER PRIMARY KEY,
	company_id INTEGER REFERENCES company_overviews(company_id),
	"date" TIMESTAMP,
	"open" NUMERIC,
	high NUMERIC,
	low NUMERIC,
    "close" NUMERIC,
    volume NUMERIC
);