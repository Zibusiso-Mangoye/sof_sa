/* Check if the year column exists and if it 
does not add column using year in int(2019 here) as default*/ 
ALTER TABLE public.raw_stackoverflow2018 
ADD COLUMN IF NOT EXISTS year INTEGER DEFAULT 2018;

SELECT  
    "DatabaseWorkedWith" AS "databases",
    "LanguageWorkedWith" AS "languages",
    "PlatformWorkedWith" AS "platforms",
    "FrameworkWorkedWith" AS "web_frameworks",
    "year"
FROM public.raw_stackoverflow2018;