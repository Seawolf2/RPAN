# RPAN
This script lets you download all of a specified redditor's RPAN streams and the corresponding comments.

It relies on Reddit's PRAW API and the Python packages youtube-dl, pandas and PRAW.

## Running the script
To run the script, open your OS's command line interface (Terminal on Mac/Linux and Command Prompt on Windows) and navigate to the script in your OS's command line interface. This can be done on Mac and Linux with 

```
cd directory/where/downloadstreams.py/is/located
```

Install the required packages with

```
pip install -r requirements.txt
```

Then, run the script with

```
python downloadstreams.py [streamer's reddit username]
```

For example, to download all of yourusername's streams, enter

```
pip install -r requirements.txt
python downloadstreams.py yourusername
```

Mac users may need to replace python with python3 and pip with pip3, e.g.

```
pip3 install -r requirements.txt
python3 downloadstreams.py yourusername
```

## Download comments only

If you only want to download comments, run the downloadcomments.py script, e.g.

```
python downloadcomments.py yourusername
```
will download all comments on all of yourusername's streams.

## Download streams between between two dates

To select streams within a time window, you can specifiy a time window in UNIX time as follows
```
python downloadstreams.py [username] [start time] [end time]
```

For example,
```
python downloadstreams.py yourusername 1609579511 1669977683
```

To convert date time to UNIX time, visit https://www.unixtimestamp.com. For example, Sat Jan 02 2021 09:25:11 UTC is 1609579511 in UNIX time and Fri Dec 02 2022 10:41:23 UTC is 1669977683.