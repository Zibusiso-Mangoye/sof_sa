/* Check if the year column exists and if it 
does not add column using year in int(2019 here) as default*/ 
ALTER TABLE public.raw_stackoverflow2021
ADD COLUMN IF NOT EXISTS year INTEGER DEFAULT 2021;

SELECT
    "DatabaseHaveWorkedWith" AS "databases",
    "LanguageHaveWorkedWith" AS "languages",
    "PlatformWantToWorkWith" AS "platforms",
    "WebframeHaveWorkedWith" AS "web_frameworks",
    "year"
FROM public.raw_stackoverflow2021;