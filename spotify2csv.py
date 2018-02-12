#!/usr/bin/env python3
"""Convert Spotify URLs to tracks info in CSV format."""

import argparse
import csv
import re
from collections.abc import MutableSet

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar


class Tracks(MutableSet):
    """A set of unique tracks."""

    def __init__(self, *args):
        self.items = set(args)

    def __contains__(self, item):
        return self.items.__contains__(item)

    def __iter__(self):
        return self.items.__iter__()

    def __len__(self):
        return self.items.__len__()

    def add(self, item):
        return self.items.add(item)

    def discard(self, item):
        return self.items.discard(item)

    def clean(self):
        """Remove tracks that have no minimal info."""
        self.items = [item for item in self.items if item.complete()]


class Track(object):
    """A track with its info, including the Spotify URL."""

    fieldnames = ['artist', 'title', 'album', 'cover', 'url']

    def __init__(self, url, artist='', title='', album='', cover=''):
        """Initiates a Spotify track with URL.

        :param url: a Spotify track URL
        :param cover: a Spotify cover image URL
        """

        self.url = url
        self._validate_url()

        self.artist = artist
        self.title = title
        self.album = album
        self.cover = cover

    def __eq__(self, other):
        return self.url == other

    def __hash__(self):
        return hash(self.url)

    def _validate_url(self):
        pattern = r'^https://open\.spotify\.com/track/[a-zA-Z0-9]+\Z$'
        if not re.match(pattern, self.url):
            raise ValueError(self.url)

    def fetch_info(self, session=None):
        """Scrap and update track info from Spotify's website."""

        if not session:
            session = requests.Session()
        res = session.get(self.url)
        res.raise_for_status()
        body = BeautifulSoup(res.content, 'html.parser')

        html_artists = body.select('.entity-info .media-bd h2 a')
        artists = []
        for html_artist in html_artists:
            artists.append(html_artist.get_text())

        self.artist = ', '.join(artists)
        self.title = body.select_one('.entity-info .media-bd h1').get_text()
        self.album = body.select_one('.featured-on .media-bd a').get_text()
        self.cover = body.select_one('[property="og:image"]')['content']

    def complete(self):
        """Tells if track has minimal info (artist and title)."""
        return self.artist and self.title


def main():
    """Convert Spotify URLs to tracks info in CSV format."""

    parser = argparse.ArgumentParser(
        description='Convert Spotify URLs to tracks info in CSV format.')
    parser.add_argument('urls_file',
                        help='the Spotify URLs list file (one URL per line)')
    parser.add_argument('tracks_file',
                        help='the filename for saving the tracks info as CSV')
    parser.add_argument('-u', '--update', action='store_true',
                        help='also update info from tracks file (if it '
                             'already exists and contains tracks)')
    args = parser.parse_args()

    tracks = Tracks()

    # Get tracks from final CSV file if it already exists
    try:
        with open(args.tracks_file) as tracks_file:
            reader = csv.DictReader(tracks_file)
            for row in reader:
                tracks.add(Track(row['url'],
                                 artist=row['artist'],
                                 title=row['title'],
                                 album=row['album'],
                                 cover=row['cover']))
    except FileNotFoundError:
        pass

    # Get tracks from URLs file
    errors = []
    with open(args.urls_file) as urls_file:
        for url in urls_file:
            try:
                tracks.add(Track(url.strip()))
            except ValueError as e:
                errors.append(e)
    if errors:
        print('Error — These URLs cannot be used:')
        for e in errors:
            print('\t', e)

    # Fetch tracks info
    session = requests.Session()
    progress = Bar('Crawling Spotify', max=len(tracks))
    errors = []

    for track in tracks:
        progress.next()
        if not args.update and track.complete():
            continue
        try:
            track.fetch_info(session=session)
        except Exception as e:
            errors.append({'url': track.url, 'error': e})

    # Finish: show errors
    progress.finish()
    if errors:
        print('\nError — No info was found for these URLs:')
        for e in errors:
            print('\t', e['url'], '\n\t\t', e['error'], sep='')

    # Clean and save tracks
    if tracks:
        tracks.clean()
        with open(args.tracks_file, 'w') as tracks_file:
            writer = csv.DictWriter(tracks_file, Track.fieldnames)
            writer.writeheader()
            for track in tracks:
                writer.writerow(vars(track))


if __name__ == '__main__':
    main()
