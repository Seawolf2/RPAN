# RPAN
This script lets you download all of a specified redditor's RPAN streams and the corresponding comments.

It relies on Reddit's PRAW API and the Python packages youtube-dl, pandas and PRAW.

To run the script, navigate to the script in your OS's command line interface and install the required packages with

```
pip install -r requirements.txt
```

Then, run the script with

```
python downloadstreams.py [streamer's reddit username]
```

For example, to download all of EddieEWI's streams, enter

```
python downloadstreams.py EddieEWI
```

Mac users may need to replace python with python3 and pip with pip3, e.g.

```
pip3 install -r requirements.txt
python3 downloadstreams.py EddieEWI
```
