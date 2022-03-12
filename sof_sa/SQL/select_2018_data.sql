SELECT 
	Respondent,
	Age,
    ConvertedSalary AS Salary,
	FormalEducation,
	RaceEthnicity AS Ethnicity,
    Gender,
    DevType,
    JobSatisfaction,
    LanguageWorkedWith,
    DatabaseWorkedWith,
    PlatformWorkedWith,
    FrameworkWorkedWith
FROM sofanalysis_staging_db.2018_data;