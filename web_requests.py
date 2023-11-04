import time

import requests
from bs4 import BeautifulSoup

from Post import Post


# make a request with 1 min timeout
# TODO see if refactoring would be possible, with pulling out some functionality
def get_newest_post_with_vote(config_data, provided_tags):
    print(f"found my url", config_data["start-url"] + config_data["path"])
    switch_to_next_page: bool = True
    page_number = 1
    p = Post()
    while switch_to_next_page:
        response = requests.get(
            url=config_data["start-url"] + config_data["path"] + str(page_number),
            timeout=1,
        )
        print(
            f"Full url: ",
            config_data["start-url"] + config_data["path"] + str(page_number),
        )
        print(response.status_code)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            posts = soup.select(config_data["posts-class-name"])
            print(len(posts), " -------------------------- page size (post list count)")
            for post in posts:
                vote_count = post.select_one(config_data["votes-class-name"])
                if int(vote_count.text) < 1:
                    print(
                        f"Vote count less than one, skipping this post", vote_count.text
                    )
                else:
                    # Check if any of the specified tags are found in the post text
                    for tag in provided_tags:
                        print(f"found the single tag", tag)
                        post_with_tag = post.select_one(tag)
                        if post_with_tag:
                            print(
                                f"Found the post that has corresponding tag and at least one vote"
                            )
                            title = post.select(config_data["post_title_class"])[0].text
                            excerpt = post.select(
                                config_data["post_text_excerpt_class"]
                            )[0].text
                            post_url = (
                                config_data["start-url"][:-1]
                                + post.find("a").attrs["href"]
                            )
                            if title and excerpt:
                                p.__init__("", title.strip(), excerpt.strip(), post_url)
                                p.save()
                                switch_to_next_page = False
        if not p.title:
            print(
                "No posts with those tags that meet the criteria found on this page. Let's check the next "
                "page..."
            )
            page_number += 1
            time.sleep(60)
            print("page number - ", page_number)
    return p
