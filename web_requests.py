import requests
from bs4 import BeautifulSoup
import time


# make a request with 1 min timeout
def get_newest_post_with_vote(url, path, posts_class, votes_class, tags_class, provided_tag):
    print("found my url", url + path)
    response = requests.get(url=url + path, timeout=1)
    print(response)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.select(posts_class)
        for post in posts:
            print(post.text, " post and tag ", provided_tag)
            if post.select_one(tags_class) == provided_tag:
                vote_count = post.select_one(votes_class)
                print('vote count -> ', vote_count)
                if vote_count and int(vote_count.text) >= 1:
                    return post.text
    return None
