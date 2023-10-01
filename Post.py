class Post:

    def __init__(self):
        self.full_text = None
        self.excerpt = None
        self.title = None

    def set_values(self, title, excerpt, full_text):
        self.title = title.strip()
        self.excerpt = excerpt.strip().replace('\n', ' ')
        self.full_text = full_text.strip()

    def __str__(self):
        return f"{self.title}  \n {self.excerpt}"
