#!/usr/bin/python3
import re
import argparse
import os

# Construct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--filepath", help="List of IPs on which you want to install NSO, comma separated")
args = ap.parse_args()

# Build replacement regex
tcp_enable = re.compile('(<tcp>\\s+<enabled>)(\\w+)(<\\/enabled>\\s+<ip>\\S+<\\/ip>\\s+<port>8080<\\/port>)')
ssl_enable = re.compile(r"(<ssl>\s+<enabled>)(\w+)(<\/enabled>)", re.MULTILINE)

def parse_config(filepath: str):
    with open(filepath, "r") as f:
        text = f.read()
    
    with open(filepath, "w") as f:
        if ssl_enable.search(text):
            text = ssl_enable.sub(r"\1true\3", text)
        if tcp_enable.search(text):
            text = tcp_enable.sub(r"\1true\3", text)
        f.write(text)
    
if __name__ == "__main__":
    filepath = getattr(args, "filepath", None)
    if filepath and os.path.exists(path=filepath):
        print(f"Parsing {filepath}")
        parse_config(filepath=filepath)