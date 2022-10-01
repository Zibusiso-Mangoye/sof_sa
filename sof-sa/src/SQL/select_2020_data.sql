/* Check if the year column exists and if it 
does not add column using year in int(2019 here) as default*/ 
ALTER TABLE public.raw_stackoverflow2020 
ADD COLUMN IF NOT EXISTS year INTEGER DEFAULT 2020;

SELECT
    "WebframeWorkedWith" AS "web_frameworks",
    "DatabaseWorkedWith" AS "databases",
    "LanguageWorkedWith" AS "languages",
    "PlatformWorkedWith" AS "platforms",
    "year"
FROM public.raw_stackoverflow2020;