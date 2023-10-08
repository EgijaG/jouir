class Post:

    def __init__(self):
        self.full_text = None
        self.excerpt = None
        self.title = None
        self.url = None

    def set_values(self, title, excerpt, full_text, url):
        self.title = title.strip()
        self.excerpt = excerpt.replace('\n', ' ').strip()
        self.full_text = full_text.strip()
        self.url = url

    def __str__(self):
        return f"{self.title}  \n{self.excerpt} \n{self.url}"
