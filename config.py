from utilities import get_frozen_status

app_name = "ePost Downloader"
app_version = "2.0.3"
app_build_date = "September 7, 2024"
zip_name = f"ePost Downloader v{app_version}.zip"

# Paths to deal with being in dev env or exe
vtp_path = "epost/epostconnect/vtp" if get_frozen_status() is True else "epostconnect/vtp"
logs_path = "epost/epostconnect/vtp/logs" if get_frozen_status() is True else "epostconnect/vtp/logs"
epost_connect_path = "epost/epostconnect" if get_frozen_status() is True else "epostconnect"
