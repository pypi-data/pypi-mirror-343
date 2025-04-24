# src/osrs_hiscore/core.py

import requests

SKILLS = [
    "Overall", "Attack", "Defence", "Strength", "Hitpoints", "Ranged", "Prayer", "Magic",
    "Cooking", "Woodcutting", "Fletching", "Fishing", "Firemaking", "Crafting",
    "Smithing", "Mining", "Herblore", "Agility", "Thieving", "Slayer", "Farming",
    "Runecraft", "Hunter", "Construction"
]

MODES = {
    "Ultimate Ironman":       "index_lite_ultimate.ws",
    "Hardcore Ironman":       "index_lite_hardcore_ironman.ws",
    "Ironman":                "index_lite_ironman.ws",
    "Regular":                "index_lite.ws",
}
BASE_URL = "https://services.runescape.com/m=hiscore_oldschool/"

SPARK_CHARS = "▁▂▃▄▅▆▇█"


def xp_for_level(level: int) -> int:
    xp = 0
    for i in range(1, level):
        xp += int(i + 300 * 2 ** (i/7.0))
    return xp // 4


def make_sparkline(data: list[int]) -> str:
    mn, mx = min(data), max(data)
    span = mx - mn or 1
    return "".join(
        SPARK_CHARS[int((v - mn) / span * (len(SPARK_CHARS)-1))]
        for v in data
    )


def fetch_stats(username: str) -> tuple[str, list[dict]]:
    last_err = None
    for mode, ep in MODES.items():
        url = f"{BASE_URL}{ep}?player={username}"
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                lines = r.text.strip().splitlines()
                stats = []
                for skill, line in zip(SKILLS, lines):
                    rank, lvl, xp = map(int, line.split(","))
                    stats.append({
                        "skill": skill,
                        "rank": rank,
                        "level": lvl,
                        "xp": xp,
                    })
                return mode, stats
            if r.status_code not in (404,):
                r.raise_for_status()
        except Exception as e:
            last_err = e
    raise last_err or requests.HTTPError(f"User '{username}' not found.")
