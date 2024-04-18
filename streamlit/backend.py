import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    data = pd.read_csv("../Data/clean_data_tracks_by_artists_genres.csv")

    return data

def load_data_plot():
    data_plot=pd.read_csv("../Data/data_model.csv")
    
    return data_plot


def get_summary(data):
    
    #Data Frame with artists who are the most popular by gender and have the most popular song also by gender
    group_data=data.groupby("genre")
    genre=[]
    artist_popularity=[]
    song_popularity=[]
    for item in group_data:
        genre.append(item[0])
        artist_popularity.append(max(item[1]["artist_popularity"]))
        song_popularity.append(max(item[1]["song_popularity"]))

    the_populars=pd.DataFrame({"genre":genre,"artist_popularity":artist_popularity,"song_popularity":song_popularity})

    populars=pd.merge(the_populars, data, on=["genre","artist_popularity","song_popularity"])
    populars=populars.drop(["artist_id","song_id","album_month_release","album_day_release"], axis=1)
    
    #Data Frame with most popular song by gender, tie is not resolve. I want to show songs
    group_gender_artists_song=data.groupby(["genre"]).agg({"song_popularity": "max"}).reset_index()
    popular_song=pd.merge(group_gender_artists_song, data, on=["genre","song_popularity"])
    popular_song=popular_song[["genre","song_name","song_popularity","artist_name","song_artists","album_name","album_year_release","song_duration_min"]]
    
    
    #Data Frame, most popularity artist by gender. if tie, for popularity, the artists with max. artist_n_followers was choosen
    group_gender_artists=data.groupby(["genre"]).agg({"artist_popularity": "max"}).reset_index()

    df_group_gender_artists=pd.merge(group_gender_artists, data, on=["genre","artist_popularity"]).drop_duplicates(subset="artist_id")
    groups_followers=df_group_gender_artists.groupby("genre").agg({"artist_n_followers": "max"}).reset_index()

    max_artists_popularity_gender=pd.merge(df_group_gender_artists, groups_followers, on=["genre","artist_n_followers"])
    max_artists_gender=max_artists_popularity_gender[["genre","artist_name","artist_popularity","artist_n_followers"]]  
    
    return populars, popular_song, max_artists_gender

def plot_tracks(data_plot):
    
    fig=plt.figure(figsize=(9,15))

    fig_one=fig.add_subplot(3,1,1)
    plt.title("Amount artists per gender by years")
    plt.xlabel("Year")
    plt.ylabel("Genre")
    fig_one.scatter(data_plot.album_year_release, data_plot.genre, data_plot.amount_artists)

    fig_two=fig.add_subplot(3,1,2)
    plt.title("Amount songs per gender by years")
    plt.xlabel("Year")
    plt.ylabel("Genre")
    fig_two.scatter(data_plot.album_year_release, data_plot.genre, data_plot.amount_songs)

    fig_three= fig.add_subplot(3,1,3)
    plt.title("AVG Songs Popularity per gender")
    plt.xlabel("Song popularity")
    plt.ylabel("Genre")
    fig_three.scatter(data_plot.avg_song_popularity, data_plot.genre)


    return plt
