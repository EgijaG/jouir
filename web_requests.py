import requests
from bs4 import BeautifulSoup


# make a request with 1 min timeout
def get_newest_post_with_vote(url, path, posts_class, votes_class, tags_class, provided_tags):
    print("found my url", url + path)
    response = requests.get(url=url + path, timeout=1)
    print(response)
    result_set = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.select(posts_class)
# need to fix it to only get ones with at least one vote
        for post in posts:
            print(post.text, " post and tag ", provided_tags)
            # Replace "vote_selector" with the CSS selector for the vote count element
            vote_count = post.select_one(votes_class)

            if vote_count and int(vote_count.text) >= 1:
                # Check if any of the specified tags are found in the post text
                for tag in provided_tags:
                    print(tag, "found the single tag")
                    res = post.select_one(tag)
                    if res:
                        result_set.append(res)
    return result_set
