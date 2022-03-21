/* Adding the column year */
ALTER TABLE public.raw_stackoverflow2020
ADD year int;

/* Updating the newly added column with one value*/
UPDATE public.raw_stackoverflow2020
SET year = 2020;

/* Return new table*/
SELECT
	"Respondent" AS "respondent",
	"Age" AS "age",
	"Ethnicity" AS "ethnicity",
    "Gender" AS "gender",
	"DatabaseDesireNextYear" AS "database_desire_next_year",
    "DatabaseWorkedWith" AS "database_worked_with",
    "LanguageDesireNextYear" AS "language_desire_next_year",
    "LanguageWorkedWith" AS "language_worked_with",
    "PlatformDesireNextYear" AS "platform_desire_next_year",
    "PlatformWorkedWith" AS "platform_worked_with",
    "WebframeWorkedWith" AS "web_framework_have_worked_with",
    "WebframeDesireNextYear" AS "web_framework_want_to_work_with", 
	"year"
FROM public.raw_stackoverflow2020;