SELECT 
	Respondent,
	Age,
	ConvertedComp AS Salary,
	EdLevel AS FormalEducation,
	Ethnicity,
	Gender,
	Trans,
	DevType,
	JobSat AS JobSatisfaction,
	LanguageWorkedWith,
	DatabaseWorkedWith,
	PlatformWorkedWith,
	MiscTechWorkedWith AS FrameworkWorkedWith
FROM sofanalysis_staging_db.2020_data;