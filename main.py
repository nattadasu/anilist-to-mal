#!/usr/bin/env python3

import requests, pprint, sys, getopt, datetime

# What kind of output do we want
outputFile = 'xml'
outputTxt = ''''''
silent = False
showProgress = False
listName = ''
complete = True
# Define our query variables and values that will be used in the query request
variables = {
  'username': '',
  'type': 'ANIME'
}
name = 'anilist-export_' + variables['type']

# Configure Banner
banner = '''
  ┏━━ AniList to MAL ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ┃ An export tool for Anilist to import to MyAnimeList.          ┃
  ┃ Enter your username, and this will generate an XML file       ┃
  ┃ to import here: https://myanimelist.net/import.php            ┃
  ┃ Made by Nathan Wentworth (https://nathanwentworth.co)         ┃
  ┠───────────────────────────────────────────────────────────────┨
  ┃ Forked and maintained by Natsu Tadama (https://nttds.my.id)   ┃ 
  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
'''

url = 'https://graphql.anilist.co'

def main(argv):
  global outputFile, silent, name, showProgress, listName, complete

  for index, arg in enumerate(argv):
    if arg == "-u" or arg == "--username":
      variables['username'] = argv[index + 1]
    elif arg == "-t" or arg == "--type":
      variables['type'] = argv[index + 1].upper()
    elif arg == "-s" or arg == "--silent":
      silent = True
    elif arg == "-n" or arg == "-o" or arg == "--set-name" or arg == "--out-file":
      name = argv[index + 1]
    elif arg == "-p" or arg == "--show-progress":
      showProgress = True
    elif arg == "-l" or arg == "--custom-list":
      listName = argv[index + 1]
    # Return help
    elif arg == "-h" or arg == "--help":
      print(banner + '''
Usage: python main.py [options...]
-u, --username <string>
    AniList Username
-t, --type <media>
    Set media type to export
    Default is ''
    Options: anime, manga
-n, --set-name <name>
-o, --out-file <name>
    Set file name
    Default is anilist-export<media>.<format>
-s, --silent
    Disable banner
-p, --show-progress
    Show progress bar
-l, --custom-list
    Select custom list
-h, --help
    Show this help menu
      ''')
      return

  if not silent:
    print(banner)

  if (listName != ''):
    complete = False

  if variables['username'] == '':
    getUserData()
  elif variables['type'] == '':
    getListType()
  else:
    getAnilistData()

def getUserData():
  variables['username'] = input("→ Anilist username: ")

  if variables['username'] == '':
    print('Please enter a valid username!')
    getUserData()
  elif variables['type'] == '':
    getListType()
  else:
    getAnilistData()

def getListType():
  variables['type'] = input("→ List type (ANIME or MANGA): ").upper()

  if variables['type'] != 'ANIME' and variables['type'] != 'MANGA':
    print('Please enter either ANIME or MANGA')
    getListType()
  else:
    getAnilistData()

def getAnilistData():
  # Make the HTTP Api request
  query = '''
  query ($username: String, $type: MediaType) {
    MediaListCollection(userName: $username, type: $type) {
      lists {
        name
        entries {
          id
          status
          score(format: POINT_10)
          progress
          notes
          repeat
          media {
            chapters
            volumes
            idMal
            episodes
            title { romaji }
          }
          startedAt{
            year
            month
            day
          }
          completedAt{
            year
            month
            day
          }
          updatedAt
          createdAt
        }
        name
        isCustomList
        isSplitCompletedList
        status
      }
    }
  }
  '''

  response = requests.post(url, json={'query': query, 'variables': variables})
  jsonData = response.json()

  if ('errors' in jsonData):
    for error in jsonData['errors']:
      print(error['message'])
    print('Your username may be incorrect, or Anilist might be down.')
    return

  statusLists = jsonData['data']['MediaListCollection']['lists']
  if len(statusLists) < 1:
    print('No items found in this list!\nDid you enter the wrong username?')
    return;
  convertAnilistDataToXML(statusLists)

def convertAnilistDataToXML(data):
  output = ''''''
  user_total_anime = 0
  user_total_watching = 0
  user_total_completed = 0
  user_total_onhold = 0
  user_total_dropped = 0
  user_total_plantowatch = 0

  for x in range(0, len(data)):
    if (data[x]['name'] == listName or complete):
      for item in data[x]['entries']:
        s = str(item['status'])
        # print(s)
        if s == "PLANNING":
          if variables['type'] == 'ANIME':
            s = "Plan to Watch"
          else:
            s = "Plan to Read"
          user_total_plantowatch += 1
        elif s == "DROPPED":
          s = "Dropped"
          user_total_dropped += 1
        elif s == "CURRENT":
          if variables['type'] == 'ANIME':
            s = "Watching"
          else:
            s = "Reading"
          user_total_watching += 1
        elif s == "PAUSED":
          s = "On-Hold"
          user_total_onhold += 1
        elif "completed" in s.lower():
          s = "Completed"
          user_total_completed += 1

        # Format time
        startedYear = str(item['startedAt']['year'])
        completedYear = str(item['completedAt']['year'])
        if startedYear == "None":
          startedDate = "0000-00-00"
        else:
          startedDate = datetime.datetime(int(startedYear), int(item['startedAt']['month']), int(item['startedAt']['day'])).strftime('%Y-%m-%d')
        if completedYear == "None":
          completedDate = "0000-00-00"  
        else:
          completedDate = datetime.datetime(int(completedYear), int(item['completedAt']['month']), int(item['completedAt']['day'])).strftime('%Y-%m-%d')

        notes = item['notes']
        if notes == "None" or notes is None:
          notes = ""

        animeItem = ''
        animeItem += '    <anime>\n'
        animeItem += '        <series_animedb_id>' + str(item['media']['idMal']) + '</series_animedb_id>\n'
        animeItem += '        <!-- <series_title>' + str(item['media']['title']['romaji']) + '</series_title> -->\n'
        animeItem += '        <series_episodes>' + str(item['media']['episodes']) + '</series_episodes>\n'
        animeItem += '        <my_watched_episodes>' + str(item['progress']) + '</my_watched_episodes>\n'
        animeItem += '        <my_start_date>' + startedDate + '</my_finish_date>\n'
        animeItem += '        <my_finish_date>' + completedDate + '</my_finish_date>\n'
        animeItem += '        <my_score>' + str(item['score']) + '</my_score>\n'
        animeItem += '        <my_status>' + s + '</my_status>\n'
        animeItem += '        <my_comments><![CDATA[' + str(notes) + ']]></my_comments>\n'
        animeItem += '        <my_tags><![CDATA[' + str(notes) + ']]></my_tags>\n'
        animeItem += '        <my_times_watched>' + str(item['repeat']) + '</my_times_watched>\n'
        animeItem += '        <update_on_import>1</update_on_import>\n'
        animeItem += '    </anime>\n\n'

        output += animeItem
        user_total_anime += 1


  outputStart = '''<?xml version="1.0" encoding="UTF-8" ?>
<!--
  Created by XML Export feature at MyAnimeList.net
  Programmed by Xinil
  Last updated 5/27/2008
  Exported at ''' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S %z') + '''
-->

<myanimelist>

    <myinfo>
        <user_id>123456</user_id>
        <user_name>''' + variables['username'] + '''</user_name>
        <user_export_type>1</user_export_type>
        <user_total_anime>''' + str(user_total_anime) + '''</user_total_anime>
        <user_total_watching>''' + str(user_total_watching) + '''</user_total_watching>
        <user_total_completed>''' + str(user_total_completed) + '''</user_total_completed>
        <user_total_onhold>''' + str(user_total_onhold) + '''</user_total_onhold>
        <user_total_dropped>''' + str(user_total_dropped) + '''</user_total_dropped>
        <user_total_plantowatch>''' + str(user_total_plantowatch) + '''</user_total_plantowatch>
    </myinfo>

'''
  output = outputStart + output + '</myanimelist>'

  writeToFile(output)

  if not silent:
    print('✔︎ Successfully exported!')
    print('\nGo to https://myanimelist.net/import.php and select "MyAnimeList Import" under import type.\n')


def writeToFile(output):
  f = open(name + '.' + outputFile, 'w', encoding="utf-8")
  f.write(output)
  f.close()

if __name__ == '__main__':
  main(sys.argv)
