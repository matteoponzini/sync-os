import re
import os
import sys
import json
import urllib.request

def create_url(url):
    """
    From the given url, produce a URL that is compatible with Github's REST API. Can handle blob or tree paths.
    """
    repo_only_url = re.compile(r"https:\/\/github\.com\/[a-z\d](?:[a-z\d]|-(?=[a-z\d])){0,38}\/[a-zA-Z0-9]+$")
    re_branch = re.compile("/(tree|blob)/(.+?)/")

    # Check if the given url is a url to a GitHub repo. If it is, tell the
    # user to use 'git clone' to download it
    if re.match(repo_only_url,url):
        print("✘ The given url is a complete repository. Use 'git clone' to download the repository",
                   "red")
        sys.exit()

    # extract the branch name from the given url (e.g master)
    branch = re_branch.search(url)
    download_dirs = url[branch.end():]
    api_url = (url[:branch.start()].replace("github.com", "api.github.com/repos", 1) +
              "/contents/" + download_dirs + "?ref=" + branch.group(2))
    return api_url, download_dirs


def download(repo_url, flatten=False, output_dir="./"):
    """ Downloads the files and directories in repo_url. If flatten is specified, the contents of any and all
     sub-directories will be pulled upwards into the root folder. """

    # generate the url which returns the JSON data
    api_url, download_dirs = create_url(repo_url)

    # To handle file names.
    if not flatten:
        if len(download_dirs.split(".")) == 0:
            dir_out = os.path.join(output_dir, download_dirs)
        else:
            dir_out = os.path.join(output_dir, "/".join(download_dirs.split("/")[:-1]))
    else:
        dir_out = output_dir

    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        response = urllib.request.urlretrieve(api_url)
    except KeyboardInterrupt:
        # when CTRL+C is pressed during the execution of this script,
        # bring the cursor to the beginning, erase the current line, and dont make a new line
        print("✘ Got interrupted")
        sys.exit()

    if not flatten:
        # make a directory with the name which is taken from
        # the actual repo
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
                print("Downloaded {}".format(data["name"]))

                return total_files
            except KeyboardInterrupt:
                # when CTRL+C is pressed during the execution of this script,
                # bring the cursor to the beginning, erase the current line, and dont make a new line
                print("✘ Got interrupted")
                sys.exit()

        for file in data:
            file_url = file["download_url"]
            file_name = file["name"]
            file_path = file["path"]

            if flatten:
                path = os.path.basename(file_path)
            else:
                path = file_path
            dirname = os.path.dirname(path)

            if dirname != '':
                os.makedirs(os.path.dirname(path), exist_ok=True)
            else:
                pass

            if file_url is not None:
                try:
                    opener = urllib.request.build_opener()
                    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
                    urllib.request.install_opener(opener)
                    # download the file
                    urllib.request.urlretrieve(file_url, path)

                    # bring the cursor to the beginning, erase the current line, and dont make a new line
                    print("Downloaded: {}".format(file_name))

                except KeyboardInterrupt:
                    # when CTRL+C is pressed during the execution of this script,
                    # bring the cursor to the beginning, erase the current line, and dont make a new line
                    print("✘ Got interrupted")
                    sys.exit()
            else:
                download(file["html_url"], flatten, download_dirs)

    return total_files

#url = create_url('https://github.com/matteoponzini/store/tree/main/configs/ulauncher')
#print(url)
#download(repo_url='https://github.com/matteoponzini/store/tree/main/configs/ulauncher/')



#Donwnloader().download('https://github.com/matteoponzini/store/tree/main/programs/ulauncher', name='./programs/ulauncher' )
#Donwnloader().download('https://github.com/matteoponzini/store/tree/main/configs/ulauncher', name='./configs/ulauncher')

#wget -r -nH --cut-dirs=2  -np -R "index.html*" --directory-prefix=configs  http://127.0.1.1/store/configs/sdkman/
#wget -r -nH --cut-dirs=2  -np -R "index.html*" --directory-prefix=AA  http://127.0.1.1/store/programs/sdkman/
#wget -r -nH --cut-dirs=2  -np -R "index.html*" --directory-prefix=programs  http://127.0.1.1/store/programs/gimp/