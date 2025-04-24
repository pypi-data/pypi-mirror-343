from datetime import datetime, timezone

def date_time_utc_column(column):
    return 'TO_CHAR({0} at time zone \'UTC\', \'yyyy-mm-dd hh24:mi:ss.ms"Z"\')'.format(column)

def get_utc_date_time():
    return str(datetime.now(timezone.utc))

def seconds_to_utc_timestamp(seconds):
    return str(datetime.fromtimestamp(seconds, tz=timezone.utc))

def get_utc_date_from_iso(date_time):
    dt = datetime.fromisoformat(date_time)
    dt_utc = dt.astimezone(timezone.utc)
    return str(dt_utc.date())
