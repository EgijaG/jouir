from database import posts


class Post:
    def __init__(self, full_text=None, excerpt=None, title=None, url=None):
        self.full_text = full_text
        self.excerpt = excerpt
        self.title = title
        self.url = url

    def save(self):
        posts.append(self)

    def __str__(self):
        return f"{self.title}  \n{self.excerpt} \n{self.url}"
