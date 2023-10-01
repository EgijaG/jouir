import sys
import time

import requests
from bs4 import BeautifulSoup
from Post import Post


# make a request with 1 min timeout
# TODO see if refactoring would be possible, with pulling out some functionality
def get_newest_post_with_vote(url, path, posts_class, votes_class, provided_tags, post_excerpt_class, post_title_class):
    print("found my url", url + path)
    switch_to_next_page: bool = True
    page_number = 1
    p = Post()
    while switch_to_next_page:
        response = requests.get(url=url + path + str(page_number), timeout=1)
        print("Full url: ", url + path + str(page_number))
        print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            posts = soup.select(posts_class)
            # need to fix it to only get ones with at least one vote
            print(len(posts), " -------------------------- the size of posts list")
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
                            # TODO implement class for posts
                            print("found the post that has corresponding tag and at least one vote")
                            title = post.select(post_title_class)[0].text
                            print(title, " -------- post title")
                            excerpt = post.select(post_excerpt_class)[0].text
                            print(excerpt, " -------- post text")
                            if title and excerpt:
                                p.set_values(title, excerpt, '')
                                switch_to_next_page = False
        if not p.title:
            print("No posts with those tags that meet the criteria found on this page. Let's check the next "
                  "page...")
            page_number += 1
            time.sleep(60)
            print("page number - ", page_number)
    return p
