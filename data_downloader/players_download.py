import urllib2
import os

class Players_Handler:
    def __init__(self):
        self.master_players_list = []

    def update_player_list(self):
        if os.path.isfile(os.getcwd() + "/../data/players.txt"):
            pass
        else:
            print False

    def _download_and_parse(self, url):
        response = urllib2.urlopen(url)
        buffer = response.read()

        table_markers = self._find_string_locations(buffer, "tbody")
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

    def _find_string_locations(self, string, substring):
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