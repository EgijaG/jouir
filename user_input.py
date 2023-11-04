def get_tags_from_user_input(tag_class):
    tags = []
    print("Please enter the tag/s that you would like to search for on StackOverFlow:")
    while True:
        try:
            max_length = int(input("How many tags would you like to search for? "))
            break
        except ValueError:
            print("Enter a valid integer!")
    while len(tags) < max_length:
        tag = input("Enter the tag you are searching for: ")
        # TODO more checks, or transformations, because if you write tag - c++ - the + characters will fail the whole
        #  execution
        if tag.__contains__("+"):
            tag = tag.replace("+", "ç")
            print(f"found new tagname ", tag)
        if tag not in tags:
            tags.append(tag_class + tag)
    print(tags)
    return tags
