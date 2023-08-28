from datetime import date, datetime

import pydantic


# Note: The code below uses Python type hints to clarify the variable types.
# More info: https://realpython.com/lessons/type-hinting/
# Define pydantic model for articles
class BlogInfo(pydantic.BaseModel):
    unique_id: str
    title: str
    description: str
    link: str
    blog_text: str
    published: date
    timestamp: datetime

    def get_filename(self):
        filename = f'{self.title.replace(" ", "_")}.json'
        return filename


# Define pydantic model for summaries
class BlogSummary(pydantic.BaseModel):
    unique_id: str  # TODO fix so same unique_id as for fulltext
    title: str
    blog_summary: str

    def get_filename(self):
        filename = f'{self.title.replace(" ", "_")}_summary.json'
        return filename
