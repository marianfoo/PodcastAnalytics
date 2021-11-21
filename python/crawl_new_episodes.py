import update_spotify_metadata
import plotly.express as px
import pandas as pd
from pathlib import Path

dict_data = {
    'baywatchberlin' : {
        'filename_csv' : 'list_episodes_metadata_bwb.csv',
        'filename_other_csv' : 'list_episodes_metadata_bwb_other.csv',
        'spotify_show_id' : '3jtLk2Zlutfjo91QZYXmlA',
        'special_episodes' : [
            '4VYA0hxnzjKKtL9QCHDeDr', # Trailer
            '1KLAaERQGMmMxEtjNmojpj', # Schmitt vs Mentalist
            '0pf0XgtnCzNAlwq7bmWTUz', # Bonus Toni Kroos
        ],
        'plot' : {
            'title' : 'Baywatch Berlin',
            'filename_image' : 'bwb_duration.png'
        },
        'plot_other' : {
            'title' : 'Baywatch Berlin Spezial',
            'filename_image' : 'bwb_duration_other.png'
        }
        
    },
    'festflauschig' : {
        'filename_csv' : 'list_episodes_metadata_ff.csv',
        'filename_other_csv' : 'list_episodes_metadata_ff_other.csv',
        'spotify_show_id' : '1OLcQdw2PFDPG1jo3s0wbp',
        'special_episodes' : [
        ],
        'plot' : {
            'title' : 'Fest und Flauschig',
            'filename_image' : 'ff_duration.png'
        },
        'plot_other' : {
            'title' : 'Fest und Flauschig Spezial',
            'filename_image' : 'ff_duration_other.png'
        }

        
    },
    'evds' : {
        'filename_csv' : 'list_episodes_metadata_evds.csv',
        'filename_other_csv' : 'list_episodes_metadata_evds_other.csv',
        'spotify_show_id' : '3bL0TxU43Md3M384UAoIc5',
        'special_episodes' : [
            '7CWfRPC38OrBmm6mfCBBIb', # Trailer
        ],
        'plot' : {
            'title' : 'Eulen vor die Säue',
            'filename_image' : 'evds_duration.png'
        },
        'plot_other' : {
            'title' : 'Eulen vor die Säue Spezial',
            'filename_image' : 'evds_duration_other.png'
        }
        
    },
    "gemischtes-hack" : {
        "download": "False",
        "new_episodes" : [],
        "filename_csv" : "list_episodes_metadata_gh.csv",
        "filename_other_csv" : "list_episodes_metadata_gh_other.csv",
        "spotify_show_id" : "7BTOsF2boKmlYr76BelijW",
        "special_episodes" : [
            "4mS4sjzeN9CErnXa4a6sse",
            "5Fn1nq18i1FDszX8Svt0Rq",
            "1Fo1syQZc61L1KNGtEpNCJ",
            "6KOoIQfExicyCVVZJHKSzX",
            "0bnUbX1qZ3jP9SDSXIVAhx",
            "2g2WNcPnnLikAmliNGBYgV",
            "0XeT9ulNqscTwCfPSVdK7Y",
            "5ETygU0iaKqrBRpQsl5aGH",
            "7KZHTYHfUqtyJQ0VTxAXlU",
            "2BMk5tZtrYCmRPtWeMcJwD",
            "2qCyfaR131IEH8jn70CE1R",
            "4s13hiJyaMrKLJZPdjH3rD",
            "5u7XOTUdFgCB7tgbOJhCRJ",
            "4nLiClCoyBTtTrd8Lo3NwQ"
        ],
        "plot" : {
            "title" : "Gemischtes Hack",
            "filename_image" : "gh_duration.png"
        },
        "plot_other" : {
            "title" : "Gemischtes Hack Spezial",
            "filename_image" : "gh_duration_other.png"
        }
        
    }
}

def save_new_plot(csv,title,filename_image):
    df_ff = pd.read_csv(str(Path().resolve().parent.resolve()) + '/PodcastAnalyticsF-F-S-S/data/' + csv)
    fig = px.bar(df_ff, x='track', y='duration_sec')
    fig.update_layout(
        title=title,
        xaxis_tickfont_size=14,
        yaxis_title='duration in seconds ',
        xaxis_title='number show'
    )
    fig.write_image(str(Path().resolve().parent.resolve()) + "/PodcastAnalyticsF-F-S-S/docs/img/" + filename_image)


def update_metadata(show):
    update_spotify_metadata.update_data(
        show['spotify_show_id'],
        show['filename_csv'],
        show['filename_other_csv'],
        show['special_episodes']
    )

for show in dict_data:
    update_metadata(dict_data[show])
    save_new_plot(dict_data[show]['filename_csv'],dict_data[show]['plot']['title'],dict_data[show]['plot']['filename_image'])
    if len(dict_data[show]['special_episodes']) > 0 :
        save_new_plot(dict_data[show]['filename_other_csv'],dict_data[show]['plot_other']['title'],dict_data[show]['plot_other']['filename_image'])