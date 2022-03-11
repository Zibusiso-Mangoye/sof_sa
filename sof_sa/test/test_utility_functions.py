from ..utility_functions import open_db, get_credentials

def test_get_credentials() -> None:
    path = "sof_sa\conf\staging_db_credentials.json"
    print(get_credentials(path))
    
test_get_credentials()