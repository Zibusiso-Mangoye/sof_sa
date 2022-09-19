ALTER TABLE public.raw_stackoverflow2019 ADD COLUMN IF NOT EXISTS year INTEGER;

/* Updating the newly added column with one value*/
UPDATE public.raw_stackoverflow2019
SET year = 2019;

/* Return new table*/
SELECT  
    "WebFrameWorkedWith" AS "web_frameworks",
    "DatabaseWorkedWith" AS "databases",
    "LanguageWorkedWith" AS "languages",
    "PlatformWorkedWith" AS "platforms",
    "year"
FROM public.raw_stackoverflow2019;