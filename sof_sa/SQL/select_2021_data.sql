/* Adding the column year */
ALTER TABLE public.raw_stackoverflow2021
ADD year int;

/* Updating the newly added column with one value*/
UPDATE public.raw_stackoverflow2021
SET year = 2021;

/* Return new table*/
SELECT
	"ResponseId" AS "respondent",
	"Age" AS "age",
    "Gender" AS "gender",
    "DatabaseWantToWorkWith" AS "database_desire_next_year",
    "DatabaseHaveWorkedWith" AS "database_worked_with",
    "LanguageWantToWorkWith" AS "language_desire_next_year",
    "LanguageHaveWorkedWith" AS "language_worked_with",
    "PlatformHaveWorkedWith" AS "platform_desire_next_year",
    "PlatformWantToWorkWith" AS "platform_worked_with",
    "WebframeHaveWorkedWith" AS "web_framework_have_worked_with",
    "WebframeWantToWorkWith" AS "web_framework_want_to_work_with", 
	"year"
FROM public.raw_stackoverflow2021;