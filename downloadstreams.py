import praw
import youtube_dl
import pandas as pd
import os
import sys
import datetime

print('Initializing Reddit instance...')
reddit = praw.Reddit(
    client_id='f1sOngcl8SEMLonKC7_9-w',
    client_secret=None,
    redirect_uri="http://localhost:8080",
    user_agent="RPAN Downloader"
)
print('Reddit instance initialized')
    
print('Initializing streamer instance...')
try:
    streamer = reddit.redditor(str(sys.argv[1]))
except:
    username = input('Enter username: ')
    streamer = reddit.redditor(username)

subs = streamer.submissions.new(limit=None)
subs = iter(subs)
print('Streamer instance initialized')

def create_dataframe():
    print('Creating dataframe...')
    author = []
    created_utc = []
    id = []
    name = []
    num_comments = []
    permalink = []
    score = []
    subreddit = []
    title = []
    upvote_ratio = []
    url = []

    for i in subs:
        author.append(i.author)
        created_utc.append(i.created_utc)
        id.append(i.id)
        name.append(i.name)
        num_comments.append(i.num_comments)
        permalink.append(i.permalink)
        score.append(i.score)
        subreddit.append(i.subreddit)
        title.append(i.title)
        upvote_ratio.append(i.upvote_ratio)
        url.append(i.url)
        
    df = pd.DataFrame(list(zip(title, author, subreddit, created_utc, id, url, permalink, num_comments, score, upvote_ratio)), columns=['title', 'author', 'subreddit', 'created_utc', 'id', 'url', 'permalink', 'num_comments', 'score', 'upvote_ratio'])
    df = df.astype({'author': 'string', 'id': 'string', 'title': 'string', 'url': 'string', 'subreddit': 'string'})

    rpan_subreddits = ['AnimalsOnReddit', 'distantsocializing', 'GlamourSchool', 'HeadlineWorthy', 'lgbt', 'readwithme', 'RedditInTheKitchen', 'RedditMasterClasses', 'RedditSessions', 'RedditSets', 'redditsweats', 'shortcircuit', 'talentShow', 'TheArtistStudio', 'TheGamerLounge', 'TheYouShow', 'whereintheworld', 'GarageCrew']
    df = df[df['subreddit'].isin(rpan_subreddits)]

    print('Dataframe ready')

    df.to_csv(streamer.name + '.csv', index=False)
    
    # Checking if a time window has been inputted
    try:
        start_time = float(sys.argv[2])
        end_time = float(sys.argv[3])
        df = df[df['created_utc'].between(start_time, end_time)]
    except:
        pass
    
    return df

df = create_dataframe()

CHECK_FOLDER = os.path.isdir(streamer.name)

# If folder doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs(streamer.name)
    print("created folder: ", streamer.name)

os.chdir(streamer.name)

def download_streams():
    downloaded = []
    for i in os.listdir():
        downloaded.append(i[-10:-4])

    for index, row in df.iterrows():
        if row['id'] in downloaded:
                continue
    # video variable is the title of the video file we'll save
        video = row['title'] + ' - ' + row['author'] + ' - ' + row['subreddit'] + ' ' + str(datetime.datetime.utcfromtimestamp(row['created_utc']).strftime("%m-%d-%Y %H%M%S")) + ' ' + row['id'] + '.mp4'
    # We remove slashes in order to avoid confusing filenames
        video = video.replace("\\", "")
        video = video.replace("/", "")
        try:
            ydl_opts = {'outtmpl': video}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([row['url']])
        except:
            pass

print('Beginning stream downloads...')
# Calling the download function three times because youtube-dl can fail to download streams the first time
download_streams()
download_streams()
download_streams()
print('Finished stream downloads')

CHECK_FOLDER = os.path.isdir('comments')

# If folder doesn't exist, then create it.
if not CHECK_FOLDER:
    os.makedirs('comments')
    print("created folder: comments")

os.chdir('comments')

def download_comments():
    for index, row in df.iterrows():
        print("Scanning comments: " + row['url'])
        submission = reddit.submission(row['id'])
        created_utc = []
        author = []
        body = []
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            try:
                created_utc.append(comment.created_utc)
                author.append(str(comment.author))
                body.append(comment.body)
            except:
                pass
        print("Saving comments: " + row['url'])
        
        df1 = pd.DataFrame(list(zip(created_utc, author, body)), columns=['created_utc', 'author', 'body'])
    
    # video variable is the title of the CSV file we'll save
        video = row['title'] + ' - ' + row['author'] + ' - ' + row['subreddit'] + ' ' + str(datetime.datetime.utcfromtimestamp(row['created_utc']).strftime("%m-%d-%Y %H%M%S")) + ' ' + row['id'] + '.csv'
    # We remove slashes in order to avoid confusing filenames
        video = video.replace("\\", "")
        video = video.replace("/", "")
    
        df1.to_csv(video, index=False)

download_comments()