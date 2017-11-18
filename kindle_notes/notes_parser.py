"""
Parse a Kindle Notes csv and make it a Jekyll post.
"""
import csv
import time


def parse_csv(file_name):
    """Open a csv file and return it."""
    reader = csv.reader(open(file_name, 'rb'))
    notes = {"notes": []}

    for i, row in enumerate(reader):
        if i == 1:
            notes["title"] = row[0].title()
        elif i == 2:
            notes["author"] = row[0]
        elif i == 4:
            notes["link"] = row[0]
        elif i > 7:
            notes["notes"].append(row[-1])
    return notes


def parse_txt(file_name):
    """Open a txt file and return the notes object."""
    notes = {
        "link": "",
        "notes": []
    }
    file = open(file_name, "r")
    for item in enumerate(file):
        i, line = item
        if i == 0:  # get title
            notes["title"] = line.split(" (")[0]
            notes["author"] = line.split(" (")[-1].rstrip().rstrip(')')
        elif i % 5 == 3:
            notes["notes"].append(line.rstrip())

    print(notes)
    return notes



def export_notes_to_post(notes, output):
    """Export notes to file."""
    date = today_date()
    title = notes["title"]
    author = notes["author"]
    link = notes["link"]

    output_file = open(output, 'w+')
    output_file.write("""---
title: Notes from {title} [raw]
date: {date}
layout: post
---
Raw Kindle notes for [{title} {author}]({link})\n\n
""".format(
    title=title, date=date, author=author, link=link))

    for note in notes["notes"]:
        output_file.write("%s  \n\n" % note)


def generate_post_from_notes(input_target):
    """Parse notes from input, export to output."""
    if ".csv" in input_target:
        notes = parse_csv(input_target)
    elif ".txt" in input_target:
        notes = parse_txt(input_target)
    else:
        return "not a supported format"

    title = "Notes-" + notes["title"].replace(" ", "-")
    output = "_posts/{}-{}.md".format(today_date(), title)
    export_notes_to_post(notes, output)

    return "done"


def today_date():
    """Return today's date formatted YYYY-MM-DD."""
    return time.strftime("%Y-%m-%d")


generate_post_from_notes("kindle_notes/rework.txt")
