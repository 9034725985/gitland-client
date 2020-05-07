#!/usr/bin/env python3

import os, time, random, requests
from dataclasses import dataclass


@dataclass
class BoardPosition:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_neighbors(self, boardX: int, boardY: int):
        result = []
        if x > 0:
            result.append(BoardPosition(x=x - 1, y=y))
        if y > 0:
            result.append(BoardPosition(x=x, y=y - 1))
        if x < boardX:
            result.append(BoardPosition(x + 1, y))
        if y < boardY:
            result.append(BoardPosition(x, y + 1))
        return result


lastMove = "up"
opposites = {"left": "right", "right": "left", "up": "down", "down": "up"}

while True:
    try:
        x = int(
            requests.get(
                "https://raw.githubusercontent.com/programical/gitland/master/players/9034725985/x",
                headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
            ).text
        )

        y = int(
            requests.get(
                "https://raw.githubusercontent.com/programical/gitland/master/players/9034725985/y",
                headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
            ).text
        )
        my_map = requests.get(
            "https://raw.githubusercontent.com/programical/gitland/master/map",
            headers={"Cache-Control": "no-cache", "Pragma": "no-cache"},
        ).text
        array_from_map = [s.split(",") for s in my_map.split("\n")]
        currentPosition = BoardPosition(x, y)
        neighbors = currentPosition.get_neighbors(
            len(array_from_map), len(array_from_map[0])
        )
    except Exception as err:
        print(str(err))
        open("error", "a").write(str(err))
        continue

    open("map", "w").write(repr(array_from_map))
    status = array_from_map[x][y]
    open("neighbors", "w").write(repr(time.time()))
    open("neighbors", "a").write("\n\nMy position:\n")
    open("neighbors", "a").write(f"({currentPosition.x}, {currentPosition.y})")
    open("neighbors", "a").write("\n\nNeighbors:\n")
    for neighbor in neighbors:
        open("neighbors", "a").write(f"({neighbor.x}, {neighbor.y})")
        open("neighbors", "a").write("\n")
        open("neighbors", "a").write(f"{array_from_map[neighbor.x][neighbor.y]}\n")

    if currentPosition.x < 5:
        move = "right"
    elif currentPosition.x > 17:
        move = "left"
    elif currentPosition.y < 5:
        move = "down"
    elif currentPosition.y > 17:
        move = "up"
    else:
        allowedMoves = (
            "right left up down".replace(opposites[lastMove], "")
            .replace("  ", " ")
            .strip()
        )
        print("since the last move was " + lastMove + ", picking from " + allowedMoves)
        move = random.choice(allowedMoves.split(" "))

    open("act", "w").write(move)
    open("neighbors", "a").write(f"\n\nMy move: {move}")
    os.system("git add .")
    os.system('git commit -m "move ' + open("act").read().strip() + '"')
    os.system("git pull -r origin master")
    os.system("git push origin master")

    lastMove = move
    time.sleep(60)
