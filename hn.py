#!/usr/bin/env python3

import os, time, random, requests
from dataclasses import dataclass
from ast import literal_eval

while True:
    try:
        top_stories = requests.get(
            "https://hacker-news.firebaseio.com/v0/topstories.json",
            headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
        ).text
        open("hn", "w").write(f"\nTop Stories: {repr(top_stories)}\n")
        stories = literal_eval(top_stories)
        for story in stories:
            story_data = requests.get(
                f"https://hacker-news.firebaseio.com/v0/item/{story}.json",
                headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
            ).text
            open("hn", "a").write(f"\nRaw Story: {repr(story_data)}")
            evaluated_story = literal_eval(story_data)
            score = evaluated_story["score"]
            open("hn", "a").write(f"\nScore: {score}")
            title = evaluated_story["title"]
            open("hn", "a").write(f"\nTitle: {title}")
            url = evaluated_story["url"]
            open("hn", "a").write(f"\nURL: {url}\n")
            open("hn", "a").write(f"\ncurl 'https://archive.fo/submit/' --data-raw 'url={url}'\n")
        os.system(f"curl 'https://archive.fo/submit/' --data-raw 'url={url}'")
    except Exception as err:
        print(str(err))
        open("hn", "a").write(str(err))
        continue
    time.sleep(360)
