import sys
import time

import requests
from bs4 import BeautifulSoup


# make a request with 1 min timeout
def get_newest_post_with_vote(url, path, posts_class, votes_class, provided_tags, post_excerpt_class, post_title_class):
    print("found my url", url + path)
    switch_to_next_page: bool = True
    page_number = 1
    result_set = {}
    while switch_to_next_page:
        response = requests.get(url=url + path + str(page_number), timeout=1)
        print("Full url: ", url + path + str(page_number))
        print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            posts = soup.select(posts_class)
            # need to fix it to only get ones with at least one vote
            for post in posts:
                print(" post and tag ", provided_tags)
                vote_count = post.select_one(votes_class)
                print(vote_count.text, ' -> vote count')
                if int(vote_count.text) < 1:
                    print("Vote count less than one, skipping this post", vote_count.text)
                else:
                    # Check if any of the specified tags are found in the post text
                    print('muhaha got in the else statement')
                    for tag in provided_tags:
                        print(tag, "found the single tag")
                        post_with_tag = post.select_one(tag)
                        if post_with_tag:
                            print("found the post that has corresponding tag and at least one vote")
                            # TODO need to figure out how to get title and text from post
                            result_set[post.select_one(post_title_class).text] = (post.select_one(post_excerpt_class)
                                                                                  .text)
                            switch_to_next_page = False
        if len(result_set) < 1:
            print("No posts with those tags that meet the criteria found on this page. Let's check the next "
                  "page...")
            page_number += 1
            time.sleep(60)
            print("page number - ", page_number)

    return result_set
