from metadataApi import metadataApi
from pathlib import Path
metadataApiClass = metadataApi(str(Path().resolve().parent.resolve()) + '/PodcastAnalytics/docs/_data/data.json')
metadataApiClass.fetch_new_episodes()
metadataApiClass.sort_episodes_from_all_shows_by_release_date()