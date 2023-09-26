# read config file, so every changing value could be changed outside code
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
def get_post(provided_tag):
    count = 0
    while count < 3:
        newest_post = get_newest_post_with_vote(config_data['start-url'], config_data['path'],
                                                config_data['posts-class-name'],
                                                config_data['votes-class-name'], config_data['tags-class-name'],
                                                provided_tag)
        # later this has to be saved to DB
        if newest_post:
            print('Got the newest post with at least one vote:', newest_post)
        count += 1
        time.sleep(60)


# ask the user for tags they want to see / read tags from config file
tags = get_tags_from_user_input(config_data['single-tag-class-name'])
get_post(tags)
# create a database connection (outside this file do all DB things - table, db, rights, connection etc.)

# save the newest post, that has at least 1 vote