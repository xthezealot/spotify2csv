#!/usr/bin/env python3
"""Convert Spotify URLs to tracks info in CSV format."""

import argparse
import csv
import re
from bs4 import BeautifulSoup
from progress.bar import Bar
import requests

def main():
    """Convert Spotify URLs to tracks info in CSV format."""

    parser = argparse.ArgumentParser(
        description="Convert Spotify URLs to tracks info in CSV format.")
    parser.add_argument("in_file", metavar="input", type=str,
                        help="the Spotify URLs list (one per line) file")
    parser.add_argument("out_file", metavar="output", type=str,
                        help="the filename for saving the CSV data")

    args = parser.parse_args()

    # Get URLs
    urls = set()
    with open(args.in_file) as in_file:
        for url in in_file:
            # Ignore URLs of local files
            if "/local/" in url:
                continue
            urls.add(url.strip())
    if not urls:
        return

    # Get existent tracks
    tracks = []
    try:
        with open(args.out_file) as out_file:
            reader = csv.DictReader(out_file)
            for row in reader:
                tracks.append({
                    "title": row["title"],
                    "artist": row["artist"],
                    "album": row["album"],
                    "cover": row["cover"],
                    "url": row["url"],
                })
    except FileNotFoundError:
        pass

    session = requests.Session()

    errors = []

    progress_bar = Bar("Crawling Spotify", max=len(urls))
    for url in urls:
        progress_bar.next()

        # Do not duplicate tracks
        if track_exists(tracks, url):
            continue

        try:
            res = session.get(url)
            res.raise_for_status()
            body = BeautifulSoup(res.content, "html.parser")

            cover = body.select_one(".cover-art-image")["style"]
            cover = "https:" + re.findall(r"url\((.*?)\)", cover)[0]
            tracks.append({
                "title": body.select_one(".entity-info .media-bd h1").get_text(),
                "artist": body.select_one(".entity-info .media-bd h2 a").get_text(),
                "album": body.select_one(".featured-on .media-bd a").get_text(),
                "cover": cover,
                "url": url,
            })
        # pylint: disable=W0703
        except Exception as err:
            errors.append({"url": url, "error": err})

    progress_bar.finish()
    if errors:
        print("\nErrors:")
        for err in errors:
            print("\t", err["url"], "\n\t\t", err["error"], sep="")

    # Save tracks
    with open(args.out_file, "w") as out_file:
        fieldnames = ["title", "artist", "album", "cover", "url"]
        writer = csv.DictWriter(out_file, fieldnames)
        writer.writeheader()
        writer.writerows(tracks)

def track_exists(tracks, url):
    """Check that a track exists by URL."""
    for track in tracks:
        if track["url"] == url:
            return True
    return False

if __name__ == "__main__":
    main()
