# https://api.quotable.io
# 180 requests per minute

# GET /quotes

# Get all quotes matching a given query. By default, this will return a paginated list of all quotes, sorted by _id. Quotes can also be filter by author, tag, and length.


# Example file output:

# now-i-am-become-death-the-destroyer-of-worlds.md:

#       ---
#       tag: dailyquote
#       ---


#       #dailyquote

#       # Daily Quote
#       ### Now I am become Death, the destroyer of worlds ^quote
#       *-Oppenheimer* ^author

import requests
import json
import os
import time
import random
import threading
import datetime as dt

# Store files in same directory as script
path = os.path.dirname(os.path.abspath(__file__))


def get_page(pagenum):
    print("Requesting page " + str(pagenum))
    url = "https://api.quotable.io/quotes?page=" + str(pagenum)
    response = requests.get(url)
    return response.json()


class GetThread(threading.Thread):
    def __init__(self, pagenum):
        threading.Thread.__init__(self)
        self.pagenum = pagenum
        self.result = None

    def run(self):
        self.result = get_page(self.pagenum)


def convert_page(content):
    # Response
    # {
    #   // The number of quotes returned in this response
    #   count: number
    #   // The total number of quotes matching this query
    #   totalCount: number
    #   // The current page number
    #   page: number
    #   // The total number of pages matching this request
    #   totalPages: number
    #   // The 1-based index of the last result included in the current response.
    #   lastItemIndex: number
    #   // The array of quotes
    #   results: Array<{
    #     _id: string
    #     // The quotation text
    #     content: string
    #     // The full name of the author
    #     author: string
    #     // The `slug` of the quote author
    #     authorSlug: string
    #     // The length of quote (number of characters)
    #     length: number
    #     // An array of tag names for this quote
    #     tags: string[]
    #   }>
    # }

    # Extract all quotes from page, store each in a list with the following format:
    # [content, author]
    quotes = []
    for quote in content["results"]:
        quotes.append([quote["content"], quote["author"]])
    return quotes


def save_quotes(quotes):
    # Save quotes to file
    for quote in quotes:
        print("Saving quote: " + quote[0])
        # Create file name from first 5 words of quote
        filename = quote[0].split(" ")[0:5]
        filename = "-".join(filename)
        filename = filename.lower()

        # Illegal characters
        filename = filename.replace(":", "")
        filename = filename.replace("?", "")
        filename = filename.replace("!", "")
        filename = filename.replace(",", "")
        filename = filename.replace(".", "")
        filename = filename.replace("'", "")
        filename = filename.replace('"', "")
        filename = filename.replace(";", "")
        filename = filename.replace("(", "")
        filename = filename.replace(")", "")
        filename = filename.replace("[", "")
        filename = filename.replace("]", "")
        filename = filename.replace("{", "")
        filename = filename.replace("}", "")
        filename = filename.replace("/", "")
        filename = filename.replace("\\", "")
        filename = filename.replace("|", "")
        filename = filename.replace("<", "")
        filename = filename.replace(">", "")
        filename = filename.replace("*", "")
        filename = filename + ".md"

        # Create file (UTF-8)
        with open(os.path.join(path, filename), "w", encoding="utf-8") as f:
            # Write front matter
            f.write("---\n")
            f.write("tag: dailyquote\n")
            f.write("---\n\n")

            # Write body
            f.write("#dailyquote\n\n")
            f.write("# Daily Quote\n\n")
            f.write("### " + quote[0] + " ^quote\n")
            f.write("*-" + quote[1] + "* ^author\n")


def test():
    # Test function
    page = get_page(1)
    quotes = convert_page(page)
    save_quotes(quotes)


def main():
    # Rate limit: 180 requests per minute
    # Do one request
    page = get_page(1)
    total_pages = page["totalPages"]
    quotes = convert_page(page)
    save_quotes(quotes)

    # Main loop
    # Spawn 30 threads, each thread will do one request
    # Collect all data from threads, save to file
    # Check rate limit, sleep if necessary
    finished = False
    pages_in_minute = 0
    pages_completed = 1
    current_minute = dt.datetime.now().minute

    print("Total pages: " + str(total_pages))
    print("Starting main loop")

    while not finished:
        threads = []
        todo = total_pages - pages_completed
        if todo > 30:
            todo = 30
        for i in range(todo):
            t = GetThread(pages_completed + i + 1)
            threads.append(t)
            t.start()
            time.sleep(0.1)

        for t in threads:
            t.join()

        for t in threads:
            quote = convert_page(t.result)
            save_quotes(quote)

        # Check rate limit
        if dt.datetime.now().minute != current_minute:
            current_minute = dt.datetime.now().minute
            pages_in_minute = 0

        pages_in_minute += 30
        if pages_in_minute >= 180:
            print("Rate limit reached, sleeping for 60 seconds")
            time.sleep(60)
            pages_in_minute = 0

        pages_completed += 30
        if pages_completed >= total_pages:
            finished = True


if __name__ == "__main__":
    main()
