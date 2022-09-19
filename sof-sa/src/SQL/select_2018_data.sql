/* Adding the column year */
ALTER TABLE public.raw_stackoverflow2018 
ADD year int;

/* Updating the newly added column with one value*/
UPDATE public.raw_stackoverflow2018
SET year = 2018;

/* Return new table*/
SELECT  
    "DatabaseWorkedWith" AS "databases",
    "LanguageWorkedWith" AS "languages",
    "PlatformWorkedWith" AS "platforms",
    "FrameworkWorkedWith" AS "web_frameworks",
    "year"
FROM public.raw_stackoverflow2018;