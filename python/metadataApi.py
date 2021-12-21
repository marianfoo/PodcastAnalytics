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
                                "description": episode['html_description'],
                                "show_in_all" : True,
                                "internal_url": self.makeTitleUrlSafe(episode['name'])
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
    def makeTitleUrlSafe(self, title):
        import re
        title = title.replace("ä", "ae")
        title = title.replace("Ä", "Ae")
        title = title.replace("Ü", "Ue")
        title = title.replace("ü", "ue")
        title = title.replace("ö", "oe")
        title = title.replace("Ö", "Oe")
        title = title.replace("ß", "ss")
        title = title.replace(" ", "-")
        title = title.replace("&", "und")
        title = title.replace("---", "-")
        title = title.replace("--", "-")
        title =  re.sub(r'[^a-zA-Z0-9-]','', title)
        # remove last character from title if it is a -
        if title[-1] == '-':
            title = title[:-1]
        return title
    def convert_links_to_html_in_string(self, description):
        import re
        URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
        links = re.findall(URL_REGEX,description)
        for link in links:
            if description[description.find(link)-1:description.find(link)] == ' ':
                description = description.replace(link, '<a href="' + link + '">' + link + '</a>')
        return description
