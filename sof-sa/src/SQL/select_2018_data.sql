/* Adding the column year */
ALTER TABLE public.raw_stackoverflow2018 
ADD year int;

/* Updating the newly added column with one value*/
UPDATE public.raw_stackoverflow2018
SET year = 2018;

/* Return new table*/
SELECT  
    "DatabaseDesireNextYear" AS "database_desire_next_year",
    "DatabaseWorkedWith" AS "database_worked_with",
    "LanguageDesireNextYear" AS "language_desire_next_year",
    "LanguageWorkedWith" AS "language_worked_with",
    "PlatformDesireNextYear" AS "platform_desire_next_year",
    "PlatformWorkedWith" AS "platform_worked_with",
    "FrameworkWorkedWith" AS "web_framework_have_worked_with",
    "FrameworkDesireNextYear" AS "web_framework_want_to_work_with",
    "year"
FROM public.raw_stackoverflow2018;