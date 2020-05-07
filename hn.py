#!/usr/bin/env python3

import os, time, random, requests
from dataclasses import dataclass
try:
    top_stories = requests.get(
        "https://hacker-news.firebaseio.com/v0/topstories.json",
        headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
    ).text
    open("hn", "a").write(f"\nTop Stories: {repr(top_stories)}\n")
    
except Exception as err:
    print(str(err))
    open("hn", "a").write(str(err))