# runescape-hiscore

[![PyPI version](https://img.shields.io/pypi/v/runescape-hiscore.svg)](https://pypi.org/project/runescape-hiscore/)  
![CI](https://github.com/JustinDeanS/runescape-hiscore/actions/workflows/python-package.yml/badge.svg)

A simple, polished CLI tool for fetching OldSchool RuneScape hiscores (Regular, Ironman, Hardcore, Ultimate).  
Features colored tables, XP-to-next-level/200 M calculations, ASCII sparklines, and JSON/CSV export.

---

## Features

- 🔍 **Auto-detect mode**: Regular / Ironman / Hardcore Ironman / Ultimate Ironman  
- 📊 **Rich table** via [Rich](https://github.com/Textualize/rich)  
- ⏳ **XP gaps**: XP until next level (for < 99) and until 200 million  
- 📈 **Sparkline**: ASCII chart of your XP distribution across skills  
- 📑 **Exports**: `--json` or `--csv` to dump raw data  
- 🎯 **Easy install** via PyPI  

---

## Installation

\`\`\`bash
pip install runescape-hiscore
\`\`\`

Or install the very latest from GitHub:

\`\`\`bash
pip install git+https://github.com/JustinDeanS/runescape-hiscore.git
\`\`\`

---

## Usage

\`\`\`bash
# Show your hiscores in a pretty table:
hiscore <username>

# Export to JSON:
hiscore --json myhiscores.json <username>

# Export to CSV:
hiscore --csv myhiscores.csv <username>
\`\`\`

### Example

\`\`\`bash
$ hiscore Zezima
──────────────────────── Hiscores for Zezima (Regular) ────────────────────────
XP distribution: █▁▁▁▁▁▁▁▁▁▁▁▄▁▁▁▁▁▁▁▁▁▁▁

 Skill          Lvl      XP           To Next      To 200 M        Rank  
 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 
 Overall        1465   27,957,906       —       172,042,094   1,332,933  
 Attack          76    1,343,681   131,900   198,656,319   1,312,184  
 Defence         76    1,342,072   133,509   198,657,928   1,197,925  
 …
\`\`\`

---

## CLI Options

\`\`\`text
Usage: hiscore [OPTIONS] USERNAME

Fetch OSRS OldSchool hiscores

Options:
  --json FILE    Write stats as JSON
  --csv FILE     Write stats as CSV
  -h, --help     Show this help message and exit
\`\`\`

---

## Development

\`\`\`bash
# Clone & enter repo
git clone https://github.com/JustinDeanS/runescape-hiscore.git
cd runescape-hiscore

# Create a dev environment
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'

# Lint your changes
flake8 src

# Run unit tests
pytest --maxfail=1 --disable-warnings -q

# Build distributions
python -m build

# Publish to PyPI (after bumping version in setup.cfg)
twine upload dist/*
\`\`\`

---

## Contributing

1. Fork the repo  
2. Create a feature branch: \`git checkout -b feat/my-feature\`  
3. Commit your changes & push: \`git push origin feat/my-feature\`  
4. Open a Pull Request  

Please follow the existing code style and add tests for new functionality.

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.
EOF
