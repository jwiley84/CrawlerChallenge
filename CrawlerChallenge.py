"""
Multi step scraper:
scrape page with Beautiful Soup
Compile list with heaps or Counter
Create compilable app
"""

import re
import requests
from bs4 import BeautifulSoup
from collections import Counter
from typing import List


def scrape_site(url: str) -> List[str]:
    #local testing for faster results
    #with open("test.html") as fp:
    #    soup = BeautifulSoup(fp, 'html.parser')

    #live testing
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    

    #start at the 'history' header. 
    results = soup.find("span", id='History')
    """
    Dev notes and thoughts: 
    The history section isn't set into a div (yay wikipedia!)
    You'll have to scrape from h2-id="History" to h2-id="Corporate_Affairs"
    The paragraphs aren't child tags, can't use that way.
    """

    text_content = []
    for item in results.parent.nextSiblingGenerator():
        if item.text == 'Corporate affairs':
            break
        else:
            if item.text != '\n':
                #add all the text bits to the text_content array for further analysis
                text_content.append(item.text.strip().split())

    #the above code results in a list of lists. need to flatten to count properly
    text_content = [word for sentence in text_content for word in sentence]

    return text_content

def count_words(words: List[str], excluded_words: List[str], top_count: int) -> dict:
    print("Here")

    """
    Python has a shortcut method to count the words in a list, and return the count quickly. 
    As I have use the python shortcut library of beautiful soup, I will use the Counter shortcut as well
    Below, commented out, is a method I would use if I were to do this in another language that didn't have Counter
    """

    counted_words = Counter(entry for entry in words if entry not in excluded_words)

    return counted_words.most_common(top_count)


    """
    count = collections.defaultdict(int)
    for word in words:
        if word not in excluded_words:
            count[word] += 1

    sorted_counts = sorted(counts.items(), key=lambda i: i[1], reverse=True)

    return sorted_counts

    for i in range(k):
        print(sorted_counts[i])
    """


if __name__ == "__main__":

    #configuration
    URL = "https://en.wikipedia.org/wiki/Microsoft"
    excluded_words = ["Windows", "Microsoft"]
    top_total_count = 10


    word_list = scrape_site(URL)
    solution = count_words(word_list, excluded_words, top_total_count)

    print(solution)


        