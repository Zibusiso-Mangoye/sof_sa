/* Check if the year column exists*/ 
IF NOT (SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='public.raw_stackoverflow2019' and column_name='year')
THEN
    ALTER TABLE public.raw_stackoverflow2019 ADD COLUMN IF NOT EXISTS year INTEGER;
    UPDATE public.raw_stackoverflow2019 SET year = 2019;
END IF;

SELECT  
    "WebFrameWorkedWith" AS "web_frameworks",
    "DatabaseWorkedWith" AS "databases",
    "LanguageWorkedWith" AS "languages",
    "PlatformWorkedWith" AS "platforms",
    "year"
FROM public.raw_stackoverflow2019;