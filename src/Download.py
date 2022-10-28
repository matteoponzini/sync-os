#!/usr/bin/python3
import os
import urllib.request
import json
import sys
import re

class Donwnloader:

    def download(self, url, name, output_dir="./"):
        """ Downloads the files and directories in repo_url. If flatten is specified, the contents of any and all
         sub-directories will be pulled upwards into the root folder. """
        # generate the url which returns the JSON data
        api_url = url
        dir_out = os.path.join(output_dir, "/".join(name.split("/")[:-1]))
        try:
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            urllib.request.install_opener(opener)
            response = urllib.request.urlretrieve(api_url)
        except KeyboardInterrupt:
            sys.exit()

        os.makedirs(dir_out, exist_ok=True)

        # total files count
        total_files = 0

        with open(response[0], "r") as f:
            data = json.load(f)
            # getting the total number of files so that we
            # can use it for the output information later
            total_files += len(data)

            # If the data is a file, download it as one.
            if isinstance(data, dict) and data["type"] == "file":
                try:
                    # download the file
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(data["download_url"], os.path.join(dir_out, data["name"]))
                    # bring the cursor to the beginning, erase the current line, and dont make a new line
                    print("Downloaded: {}".format(data["name"]))
                    return total_files
                except KeyboardInterrupt:
                    # when CTRL+C is pressed during the execution of this script,
                    # bring the cursor to the beginning, erase the current line, and dont make a new line
                    sys.exit()

            for file in data:
                file_url = file["download_url"]
                file_name = file["name"]
                file_path = file["path"]

                path = file_path
                os.makedirs(dir_out, exist_ok=True)

                if file_url is not None:
                    try:
                        opener = urllib.request.build_opener()
                        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                        urllib.request.install_opener(opener)
                        # download the file
                        urllib.request.urlretrieve(file_url, os.path.join(dir_out, file_name))

                        # bring the cursor to the beginning, erase the current line, and dont make a new line
                        print("Downloaded: {}".format(file_name))

                    except KeyboardInterrupt:
                        # when CTRL+C is pressed during the execution of this script,
                        # bring the cursor to the beginning, erase the current line, and dont make a new line
                        sys.exit()

        return total_files

    def remote(self, url):
        """
        From the given url, produce a URL that is compatible with Github's REST API. Can handle blob or tree paths.
        """
        repo_only_url = re.compile(r"https:\/\/github\.com\/[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}\/[a-zA-Z0-9]+$")
        re_branch = re.compile("/(tree|blob)/(.+?)/")
        # Check if the given url is a url to a GitHub repo. If it is, tell the
        # user to use 'git clone' to download it
        if re.match(repo_only_url,url):
            sys.exit()
        # extract the branch name from the given url (e.g master)
        branch = re_branch.search(url)
        download_dirs = url[branch.end():]
        api_url = (url[:branch.start()].replace("github.com", "api.github.com/repos", 1) +
                  "/contents/" + download_dirs + "?ref=" + branch.group(2))
        return api_url
