import re
import requests
import pymongo
import progressbar


class ExtractorTool(object):
    def __init__(self):
        """

        :rtype: object
        """
        try:
            # todo: create a config file and load database/collection name from there
            self.mongo = pymongo.MongoClient(serverSelectionTimeoutMS=1)
            self.mongo.server_info()
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print(e)

        self.link = 'http://corpora.aifdb.org/'
        self.dl_link = 'http://aifdb.org/json/'
        self.print_stats()
        self.update()
        #self.print_stats()

    def update(self):
        corpora_r = requests.get(self.link)

        if corpora_r.status_code == requests.codes.ok:
            codenames = re.findall(r'href=[\'"]?([a-zA-Z0-9]+)[\'"]?\sclass=\"corporalink\"', corpora_r.text)

            for code in codenames:
                self.download_arguments(code)

    def download_arguments(self, code):
        print('\nchecking collection: ' + self.link + code)
        map_r = requests.get(self.link + code)

        if map_r.status_code == requests.codes.ok:
            # find all the maps present on the webpage
            maps = re.findall(r'var\snsIDs\s=\s\[([\d,]*)\]', map_r.text)[0].split(",")

            # todo: add a check to make sure the website format didn't change maybe ie. check if list empty
            col_count = self.mongo['arguments'][code].count()
            print('\nTotal # of maps available: ' + str(len(maps)) +
                  '\nTotal # maps in collection: ' + str(col_count))

            # if the number is not equal (shortage)
            if col_count < len(maps):
                cursor = self.mongo['arguments'][code].find(projection={'_id': True})

                # if the database has some data, only download those missing
                if cursor.count() > 0:
                    current = {doc['_id'] for doc in cursor}
                    updates = {x for x in maps if x not in current}

                # else the database is empty, download all the maps
                elif cursor.count() == 0:
                    updates = {x for x in maps}

                else:
                    updates = None

                if updates is not None:
                    # iterate through the updates and download missing
                    update_bar = progressbar.ProgressBar()
                    for map_number in update_bar(updates):
                        json_r = requests.get(self.dl_link + map_number)

                        # check to see the requested link is valid
                        if json_r.status_code == requests.codes.ok:
                            try:
                                json_doc = json_r.json()
                                json_doc['_id'] = map_number
                                self.mongo['arguments'][code].insert_one(json_doc)
                            except ValueError:
                                pass

                        else:
                            print("Link not valid, link format could have changed.")

    def print_stats(self):
        total = 0
        for x in self.mongo['arguments'].collection_names():
            total = total + self.mongo['arguments'][x].count()
            print(x + ': ' + str(self.mongo['arguments'][x].count()))
        print('Total # of Arguments Collected: ' + str(total))

    def close_connection(self):
        self.mongo.close()

if __name__ == '__main__':
    ExtractorTool()
