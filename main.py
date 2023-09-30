# read config file, so every changing value could be changed outside code
import sys
import time

import yaml
from web_requests import get_newest_post_with_vote
from user_input import get_tags_from_user_input


def read_config():
    try:
        with open('config.yaml', 'r') as file_object:
            data = yaml.load(file_object, Loader=yaml.SafeLoader)
            print('Successfully read data from config')
            return data
    except IOError as e:
        print('Error reading config file, as stated: ', e)


config_data = read_config()


# Find web request library
def get_post(provided_tags):
    print('Hello from getting single post or multiple')

    newest_post = get_newest_post_with_vote(config_data['start-url'], config_data['path'],
                                            config_data['posts-class-name'],
                                            config_data['votes-class-name'],
                                            provided_tags, config_data['post_text_excerpt_class'],
                                            config_data['post_title_class'])

    # later this has to be saved to DB
    if newest_post:
        print('Got the newest post with at least one vote:', newest_post)
        return newest_post


# ask the user for tags they want to see / read tags from config file
tags = get_tags_from_user_input(config_data['single-tag-class-name'])
print("Got the tags from user -> ", tags)
print("Final post ->", get_post(tags))
sys.exit(0)
# create a database connection (outside this file do all DB things - table, db, rights, connection etc.)

# save the newest post, that has at least 1 vote
