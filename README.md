# Anilist to MAL
Anilist to MAL is a simple python tool that lets you export your anime list from [AniList](https://anilist.co) to [MyAnimeList](https://myanimelist.net).

This fork is maintained version of upstream, as the repo is being used for [nattadasu/animeManga-autoBackup](https://github.com/nattadasu/anime)

## Changes of this fork

* This version added more metadata to the XML file. Including, but not limited to:
  * Started date
  * Finished date
  * Anime/manga title (by default commented to avoid conflict with MAL romanization schema)
  * Comment and Tags (Note in AniList)
* Added `-h`/`--help` for show help and valid arguments list.
* Added long arguments for readability.
* `-f`/`--format` is unsupported, only XML is allowed for output.

## Usage
This app requires [Python 3](https://www.python.org/downloads/) and [Python Requests](http://docs.python-requests.org/en/master/).

Install Python Requests with `pip3 install requests`.

Once both are installed, run the app with `python3 main.py` and follow the instructions, or pass some [arguments](#arguments) into command.

### Arguments
In addition to the step-by-step method, you can pass some arguments to the script.

- `-u`, `--username <name>`: set username, if not filled, script will prompt
- `-t`, `--type <media>`: set list type, if not filled, script will prompt
  - options: `anime`, `manga`
- `-n <name>`, `-o <name>`, `--set-name <name>`, `--out-file <name>`: takes one argument, set the file name to be exported to

- `-s`, `--silent`: takes zero arguments, run in silent mode (no non-essential prints)
- `-p`, `--show-progress`: takes zero arguments, show progress while running

- `-l`, `--custom-list`: select a specific list to export of your profile (default `''`)

- `-h`, `--help`: shows help page. If argument added, it will end the script.
