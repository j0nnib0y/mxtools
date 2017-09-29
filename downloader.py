#!/usr/bin/env python3

import sys
import os
import math
import requests
import json

# hide useless tracebacks (not needed for production use)
sys.tracebacklimit = 0

# program info
__author__ = "Jon-Mailes 'Jonniboy' Gr"
__copyright__ = "Copyright 2017 - Jon-Mailes 'Jonniboy' Gr"
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Jon-Mailes Gr"
__email__ = "mail ät jonni pünktchen it"

# constants
MXAPI_SEARCH_URL = "https://{site}.mania-exchange.com/tracksearch2/search"
MXAPI_DOWNLOAD_URL = "https://{site}.mania-exchange.com/tracks/download/"
MXAPI_ALLOWED_SITES = ["tm", "sm"]
DEFAULT_ARGS = {"api": "on", "format": "json", "limit": 1}


def exception_handler(exception_type, exception, traceback):
    print("%s: %s" % (exception_type.__name__, exception))


def parse_args(args={}):
    limit = -1
    site = "tm"
    path = "./"
    newname = "gbx"

    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=', 1)
            if '=' in value:
                raise ValueError(arg + " is not a valid argument!")
            else:
                if key == "limit":
                    limit = int(value)
                elif key == "path":
                    path = str(value)
                elif key == "newname":
                    newname = str(value)
                else:
                    args[key] = value
        else:
            if arg in MXAPI_ALLOWED_SITES:
                site = arg
            else:
                raise ValueError(arg + " is not a valid argument!")

    return (site, args, path, newname, limit)


def search_maps(args, site):
    url = MXAPI_SEARCH_URL.replace("{site}", site)
    r = requests.get(url, params=args)

    if r.status_code == 200:
        data = json.loads(r.text)

        return data["totalItemCount"]
    else:
        raise IOError("'" + url + "' could not be reached! HTTP Code: " + str(r.status_code))


def get_map_list(args, site, count=None, limit=-1):
    if count is None:
        count = search_maps(args, site)

    if limit > 0 and limit < count:
        count = limit

    maps = []
    args["limit"] = 100

    for i in range(1, math.ceil(count / 100) + 1):
        args["page"] = i

        if limit > 0 and i == math.ceil(count / 100):
            args["limit"] = limit - (i - 1) * 100

        r = requests.get(MXAPI_SEARCH_URL.replace(
            "{site}", site), params=args)
        data = json.loads(r.text)
        maps += data["results"]

    return maps


def download_maps(maps, path, newname, site):
    for map_ in maps:
        url = MXAPI_DOWNLOAD_URL.replace(
            "{site}", site) + str(map_["TrackID"])
        r = requests.get(url)

        if r.status_code == 200:
            if newname == 'mx':
                fn = os.path.join(os.path.dirname(__file__), path, map_[
                    "Name"] + ".Map.Gbx")
            else:
                fn = os.path.join(os.path.dirname(__file__), path, map_[
                    "GbxMapName"] + ".Map.Gbx")

            try:
                with open(fn, 'xb') as f:
                    for chunk in r:
                        f.write(chunk)
            except FileExistsError:
                print("File '" + fn + "' already exists. Skipped!")
        else:
            raise IOError("'" + url + "' could not be reached! HTTP Code: " + str(r.status_code))


def main():
    # process args to get settings
    site, args, path, newname, limit = parse_args(DEFAULT_ARGS)
    print("Site:\t" + str(site))
    print("Args:\t" + str(args))
    print("Limit:\t" + str(limit) + "\n")

    # process search
    total_count = search_maps(args, site)

    # if there are any maps found, wait for accepting the download
    if total_count > 0:
        if limit > 0:
            print("Found " + str(total_count) +
                  " maps. Do you want to download " + str(limit) + " of them now?")
        else:
            print("Found " + str(total_count) +
                  " maps. Do you want to download them now?")
    else:
        print("No maps found for your search parameters. Try again!")

    while True:
        check = input("Type in y/[n]: ")

        if check == 'y':
            break
        elif check == 'n' or check == '':
            exit()
        else:
            print("Did not understand your input. Try again!")

    # get whole map list
    maps = get_map_list(args, site, total_count, limit)
    print("\nGot map list!")

    # finally, download the maps
    download_maps(maps, path, newname, site)
    print("Downloaded maps!")


if __name__ == '__main__':
    # show readable errors (comment for debugging)
    sys.excepthook = exception_handler

    print(u'#################################################################')
    print(u'#               Mania-Exchange.com Map Downloader               #')
    print(u'# (C) by Jon-Mailes "Jonniboy" Gr. (mail ät jonni pünktchen it) #')
    print(u'#################################################################')

    if len(sys.argv) > 1:
        main()
    else:
        print("Usage:\t\t\tdownloader.py tm/sm arg1=val1 arg2=val2")
        print("Possible arguments:\tpath (download path)")
        print("\t\t\tlimit (number of maps which get downloaded)")
        print("... and all arguments from this site at Track Search: https://api.mania-exchange.com/documents/reference")
