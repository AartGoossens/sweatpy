from sweat.io import opendata
from sweat.io.models import dataframes


def test_get_activity():
    wdf = opendata.get_activity(
        athlete_id='5e8b9087-baad-4dfa-ba28-dc40331ee254',
        filename='2018_04_02_15_54_42.csv'
    )
    assert isinstance(wdf, dataframes.WorkoutDataFrame)
