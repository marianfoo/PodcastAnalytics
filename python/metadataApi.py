import json

class metadataApi:
    def __init__(self, metaDataLocation):
        self.metaDataLocation = metaDataLocation
        self.loadMetaData()
        # '../data/data.json'
    def loadMetaData(self, metaDataLocation = None):
        if metaDataLocation == None:
            metaDataLocation = self.metaDataLocation
        with open(metaDataLocation) as json_file:
            self.metadata_json  = json.load(json_file)
        return self.metadata_json
    def getMetaData(self):
        if self.metadata_json == None:
            self.loadMetaData()
        return self.metadata_json
    def saveMetaData(self):
        with open(self.metaDataLocation, 'w') as outfile:
            json.dump(self.metadata_json, outfile, indent=4)
    def getShow(self,show_id):
        return self.metadata_json[show_id]
    def getShowAllEpisodes(self, show_id):
        return self.metadata_json[show_id]['all_episodes']
    def getEpisodeById(self, episode_id):
        for show in self.metadata_json:
            for episode in self.metadata_json[show]['all_episodes']:
                if episode == episode_id:
                    return self.metadata_json[show]['all_episodes'][episode]
        # not found
        return None
    def getEpisodeByIdAndShow(self, show_id, episode_id):
        return self.metadata_json[show_id]['all_episodes'][episode_id]
        # not found
        return None
    def setNewEpisode(self, episode_id, show_id, episode_data):
        all_episodes = self.metadata_json[show_id]['all_episodes']
        all_episodes[episode_id] = episode_data
    def updateEpisode(self, episode_id, show_id, episode_data):
        self.metadata_json[show_id]['all_episodes'][episode_id] = episode_data
    def setEpisodeTag(self, episode_id, show_id, tag, show_in_all):
        episode = self.getEpisodeByIdAndShow(show_id, episode_id)
        if 'tags' not in episode:
            episode['tags'] = {}
        if tag not in episode['tags']:
            episode['tags'][tag] = show_in_all
        for tag in episode['tags']:
            if episode['tags'][tag] == False:
                episode['show_in_all'] = False
                break
        self.updateEpisode(episode_id, show_id, episode)
    def setTagsFromMetadata(self):
        for show in self.metadata_json:
            for episode in self.metadata_json[show]['all_episodes']:
                self.metadata_json[show]['all_episodes'][episode]['show_in_all'] = True
        for show in self.metadata_json:
            if 'special_episodes' in self.metadata_json[show]:
                special_episodes = self.metadata_json[show]['special_episodes']
                for special_episode in special_episodes:
                    episodes = special_episodes[special_episode]['episodes']
                    show_in_all = special_episodes[special_episode]['show_in_all']
                    for episode in episodes:
                        self.setEpisodeTag(episode, show, special_episode,show_in_all)
    def generate_sample_data_new_episode(self, episode, show):
        if 'samples' in self.metadata_json[show]:
            samples = self.metadata_json[show]['samples']
            if 'samples_data_scannend' not in episode:
                episode['samples_data_scannend'] = {}
            for sample in samples:
                if samples[sample]['type'] not in episode['samples_data_scannend']:
                    episode['samples_data_scannend'][samples[sample]['type']] = {}
                if sample not in episode['samples_data_scannend'][samples[sample]['type']]:
                    episode['samples_data_scannend'][samples[sample]['type']][sample] = {}  
                episode['samples_data_scannend'][samples[sample]['type']][sample] = {
                    "scanned": False,
                    "createdAt": ""
                }
        return episode
    def fetch_new_episodes(self):
        import spotify_api

        for show in self.metadata_json:
            all_episodes = self.metadata_json[show]['all_episodes']
            if 'spotify_show_id' in self.metadata_json[show]:
                episodes = spotify_api.get_all_episodes_show(self.metadata_json[show]['spotify_show_id'])
                for episode in episodes:
                    if episode['id'] not in all_episodes:
                        data = {
                                "release_date": episode['release_date'],
                                "duration_sec":    episode['duration_ms'] / 1000,
                                "spotify_url": episode['external_urls']['spotify'],
                                "name": episode['name'],
                                "description": episode['description'],
                                "show_in_all" : True
                        }
                        data = self.generate_sample_data_new_episode(data,show)
                        self.setNewEpisode(episode['id'], show , data)
            self.saveMetaData()
    def sort_episodes_from_all_shows_by_release_date(self):
        for show in self.metadata_json:
            all_episodes = self.metadata_json[show]['all_episodes']
            sorted_episodes = sorted(all_episodes.items(), key=lambda x: x[1]['release_date'])
            self.metadata_json[show]['all_episodes'] = {}
            for episode in sorted_episodes:
                self.metadata_json[show]['all_episodes'][episode[0]] = episode[1]
        self.saveMetaData()
        