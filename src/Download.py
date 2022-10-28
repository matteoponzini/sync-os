#!/usr/bin/python3
import subprocess

class Donwnloader:

    def download(self, url, name, output_dir="./"):
        process = subprocess.Popen(
            "wget -r -nH --cut-dirs=2  -np -R \"index.html*\" --directory-prefix={}  {}".format(output_dir, url),
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True,
            shell = True
        )
        std_out, std_err = process.communicate()
        #print(std_out.strip(), std_err)
        
    def remote(self, url):
        return url+'/'
