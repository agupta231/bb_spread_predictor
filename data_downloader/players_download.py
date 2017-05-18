from string import ascii_lowercase
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import urllib2
import os


class Players_Handler:
    def __init__(self):
        pass

    def update_player_list(self):
        pool = ThreadPool(8)
        results = pool.map(Players_Handler._download_and_parse, ascii_lowercase)
        flatten = lambda l: [item for sublist in l for item in sublist]

        new_players_array = flatten(results)

        if os.path.isfile(os.getcwd() + "/../data/players.txt"):
            master_players_array = []
            players_data_file = open(os.getcwd() + "/../data/players.txt", "r")

            for line in players_data_file:
                raw_data = line.rstrip()
                sub_array = raw_data.split(",")

                master_players_array.append([sub_array[0], int(sub_array[1])])

            players_data_file.close()

            for player in new_players_array:
                if not (player in (i[0] for i in master_players_array)):
                    master_players_array.append([player, len(master_players_array) + 1])

                    print player + " added"

            players_data_file = open(os.getcwd() + "/../data/players.txt", "w")
            players_data_file.truncate()

            for arr in master_players_array:
                players_data_file.write(arr[0] + "," + str(arr[1]) + "\n")

            players_data_file.close()

        else:
            players_data_file = open(os.getcwd() + "/../data/players.txt", "w")

            for i in xrange(len(new_players_array)):
                players_data_file.write(new_players_array[i] + "," + str(i) + "\n")

            players_data_file.close()

    @staticmethod
    def _download_and_parse(letter):
        print "Downloading Letter: " + letter

        try:
            response = urllib2.urlopen("http://www.basketball-reference.com/players/" + letter + '/')
        except:
            print letter + " failed"
            return []

        buffer = response.read()

        table_markers = Players_Handler._find_string_locations(buffer, "tbody")
        player_data_raw = buffer[table_markers[-2]:table_markers[-1]]

        del buffer

        index = 0
        player_sublist = []

        while index < len(player_data_raw):
            index = player_data_raw.find('<a href="/players', index)

            if index == -1:
                break
            else:
                player_starting_index = player_data_raw.find(">", index)
                player_ending_index = player_data_raw.find("<", player_starting_index)

                player_sublist.append(player_data_raw[player_starting_index + 1:player_ending_index])

                index = player_ending_index + 1

        return player_sublist

    @staticmethod
    def _find_string_locations(string, substring):
        location_array = []
        index = 0

        while index < len(string):
            index = string.find(substring, index + 1)

            if index == -1:
                break
            else:
                location_array.append(index)

        return location_array

ph = Players_Handler()
ph.update_player_list()