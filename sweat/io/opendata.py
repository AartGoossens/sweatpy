from collections import namedtuple
from os import listdir, path
import zipfile

from osfclient import api, cli
import pandas as pd

from .models import dataframes


PROJECT_ID = '6hfpz'


Args = namedtuple(
    'Args',
    ['project', 'remote', 'local', 'username', 'password', 'force', 'output'],
)


class Client:
    def __init__(self, project_id=PROJECT_ID):
        self.args = Args(
            project=project_id,
            remote=None,
            local=None,
            username=None,
            password=None,
            force=False,
            output=None,
        )
        self.osf = api.OSF()
        self.project = self.osf.project(project_id)
        self.store = next(self.project.storages)

    def download_all(self, *, consent_that_this_might_download_lots_of_data=False):
        if not consent_that_this_might_download_lots_of_data:
            raise ValueError(
                'Please be aware that running this method might download lots of data.'
                ' Add keyword argument consent_that_this_might_download_lots_of_data=True '
                'to accept this.'
            )

        cli.clone(self.args)
        for f in self.store.files:
            self._unzip_file(path.join(PROJECT_ID, 'osfstorage', f.name))

    def download_athlete(self, athlete_id):
        for f in self.store.files:
            if f.name.strip('.zip') == athlete_id:
                break
        file_path = path.join(PROJECT_ID, 'osfstorage', f.name)
        self.args = self.args._replace(
            remote=f.path,
            local=file_path,
        )
        cli.fetch(self.args)
        
        self._unzip_file(file_path)

    def list_athletes(self):
        """
        Assumes that each file belongs to one athlete.
        """
        athlete_ids = [f.name.strip('.zip') for f in self.store.files]

        return athlete_ids
    
    def _unzip_file(self, filename):
        with zipfile.ZipFile(filename,"r") as zip_ref:
            zip_ref.extractall(filename.strip('.zip'))

def list_athletes():
    athlete_ids = []
    for f in listdir(path.join(PROJECT_ID, 'osfstorage')):
        if path.isdir(path.join(PROJECT_ID, 'osfstorage', f)):
            athlete_ids.append(f)
    return athlete_ids

def get_athlete(athlete_id):
    pass

def get_activities_for_athlete(athlete_id):
    pass


def get_activity(athlete_id, filename):
    file_path = path.join(PROJECT_ID, 'osfstorage', athlete_id, filename)
    df = pd.read_csv(file_path)
    wdf = dataframes.WorkoutDataFrame(dict(
        time=df.secs,
        distance=df.km,
        power=df.power,
        heartrate=df.hr,
        cadence=df.cad,
        altitude=df.alt,
    ))
    return wdf
