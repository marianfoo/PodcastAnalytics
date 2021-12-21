from metadataApi import metadataApi
from datetime import datetime
from pathlib import Path
import locale
locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
metadataApiClass = metadataApi(str(Path().resolve().parent.resolve()) + '/PodcastAnalytics/docs/_data/data.json')
metadata_json = metadataApiClass.getMetaData()
def createEpisodePages(show,permalink_show,folder_name,grand_parent):
    track = 1
    for episode in metadata_json[show]['all_episodes']:
        episode_id = episode
        episode = metadata_json[show]['all_episodes'][episode]
        release_date_str = episode['release_date']
        release_date_obj = datetime.strptime(release_date_str, '%Y-%m-%d')
        release_date_format = date_time = release_date_obj.strftime("%d. %B %Y")
        title = episode['name']
        title = title.replace(':', '')
        safeTitle = metadataApiClass.makeTitleUrlSafe(title)

        permalink =  '/' + permalink_show + '/episoden/' + safeTitle
        layout = 'page'
        parent =  'Alle Episoden'
        nav_order = track
        track += 1
        # create a file with ending .md
        with open(str(Path().resolve().parent.resolve()) + '/PodcastAnalytics/docs/_pages/' + folder_name + '/episodes/' + safeTitle + '.md', 'w',encoding="utf-8") as f:
            # add new line to file
            f.write('---\n')
            # add title
            f.write('title: ' + title + '\n')
            f.write('layout: ' + layout + '\n')
            f.write('permalink: ' + permalink + '\n')
            f.write('parent: ' + parent + '\n')
            f.write('grand_parent: ' + grand_parent + '\n')
            f.write('nav_order: ' + str(nav_order) + '\n')
            f.write('---\n')
            f.write('\n')
            f.write('# ' + title + '\n')
            f.write(
                f"""<table class="resp-table dcf-table dcf-table-responsive dcf-table-bordered dcf-table-striped dcf-w-100%">
                    <tbody>
                        <tr>
                            <th scope="row">Veröffentlich am:</th>
                            <td data-label="Veröffentlich am:">{release_date_format}</td>
                        </tr>
                        <tr>
                            <th scope="row">Länge </th>
                            <td data-label="Länge ">{str(int(episode['duration_sec']/60))} Minuten</td>
                        </tr>"""
            )
            if 'spotify_url' in episode:
                f.write(f"""<tr>
                                <th scope="row">Spotify Link</th>
                                <td data-label="Spotify Link"><a href="{episode['spotify_url']}">Spotify Link</a></td>
                            </tr>""")
            f.write("""</tbody>
                </table>\n"""

            )
            f.write('\n')
            f.write('***\n')
            f.write('\n')
            # convert links in description to html links
            if episode['description'] != None:
                episode['description'] = episode['description'].replace('\n', ' <br> ')
                episode['description'] = metadataApiClass.convert_links_to_html_in_string(episode['description'])
                f.write('## Beschreibung der Folge' + '\n')
                f.write('\n')
                f.write('<div>\n')
                f.write(episode['description'] + '  \n')
                f.write('</div>\n')
                f.write('\n')
            found = False
            if 'samples_data' in episode:
                for type in episode['samples_data']:
                    for sample in episode['samples_data'][type]:
                        for sample_row in episode['samples_data'][type][sample]:
                            found = True
                            f.write('***\n')
                            f.write('\n')
                            f.write('## Gefundene Jingles' + '\n')
                            f.write('\n')
                            f.write("""<table style="display: table;">
                                    <tr>
                                        <th class="tableColumnTitle">Titel</th>
                                        <th class="tableColumnTimestamps">Timestamps</th>
                                    </tr>
                                    """)
                            break
                for type in episode['samples_data']:
                    for sample in episode['samples_data'][type]:
                        for sample_row in episode['samples_data'][type][sample]:
                            # round double to int
                            sample_row['duration_total_min'] = int(round(sample_row['duration_total_min']))
                            sample_row['duration_min'] = int(round(sample_row['duration_min']))
                            sample_row['duration_sec'] = int(round(sample_row['duration_sec']))
                            f.write(f"""<tr>
                                <td markdown="span"  class="tableColumnTitle">{ sample }</td>
                                <td markdown="span" class="tableColumnTimestamps">
                                <br>
                                <a href="https://open.spotify.com/episode/{ episode_id }?t={ sample_row['duration_total_min'] }">
                                { sample_row['duration_min']} Minuten / { sample_row['duration_sec']} Sekunden</a>
                                </td></tr>"""
                            )
                if found == False:
                    f.write('***\n')
                    f.write('\n')
                    f.write('## Keine Jingles gefunden')
                else:
                    f.write('</table>')

createEpisodePages('festflauschig','fest-flauschig','festflauschig','Fest und Flauschig')
createEpisodePages('baywatchberlin','baywatch-berlin','baywatchberlin','Baywatch Berlin')
createEpisodePages('sanftsorgfaeltig','sanft-sorgfältig','sanftsorgfältig','Sanft und Sorgfältig')
createEpisodePages('gemischtes-hack','gemischtes-hack','gemischteshack','Gemischtes Hack')
createEpisodePages('evds','eulen-vor-die-saeue','eulenvordiesaeue','Eulen vor die Säue')