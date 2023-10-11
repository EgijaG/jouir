# read config file, so every changing value could be changed outside code
import sys
import yaml

from database import set_credentials, connect_to_mysql, insert_data
from web_requests import get_newest_post_with_vote
from user_input import get_tags_from_user_input


def read_config(file):
    try:
        with open(file, "r") as file_object:
            data = yaml.load(file_object, Loader=yaml.SafeLoader)
            print("Successfully read data from config")
            return data
    except IOError as e:
        print("Error reading config file, as stated: ", e)


config_data = read_config("web_selector_config.yaml")


# Find web request library
def get_post(provided_tags):
    print("Hello from getting newest post with at least one vote")
    newest_post = get_newest_post_with_vote(
        config_data["start-url"],
        config_data["path"],
        config_data["posts-class-name"],
        config_data["votes-class-name"],
        provided_tags,
        config_data["post_text_excerpt_class"],
        config_data["post_title_class"],
    )

    # later this has to be saved to DB
    if newest_post:
        print("Got the newest post with at least one vote:", newest_post)
        return newest_post


# ask the user for tags they want to see / read tags from config file
tags = get_tags_from_user_input(config_data["single-tag-class-name"])
print("Got the tags from user -> ", tags)


# save the newest post, that has at least 1 vote
result = get_post(tags)
print("Final post ->", result.__str__())
posts = {result.title: result.excerpt}

# save posts to database
# reading db config
db_config = read_config("configs/db_config.yaml")
set_credentials(
    db_config["host"], db_config["user"], db_config["pass"], db_config["database"]
)
# create a database connection (outside this file do all DB things - table, db, rights, connection etc.)
cursor = connect_to_mysql()
# insert data into DB
# TODO figure out what to do with the cursor & optimize to get the data to db
insert_data(connect_to_mysql(), result)
sys.exit(0)
