from datetime import date, datetime
from typing import Optional

import pydantic


# Note: The code below uses Python type hints to clarify the variable types.
# More info: https://realpython.com/lessons/type-hinting/
# Define pydantic model for articles
class BlogInfo(pydantic.BaseModel):
    unique_id: str
    title: str
    description: Optional[str] = None
    link: str
    blog_text: str
    published: date
    timestamp: datetime

    def get_filename(self):
        filename = f'{self.title.replace(" ", "_")}.json'
        return filename


# Define pydantic model for summaries
class BlogSummary(pydantic.BaseModel):
    unique_id: str
    title: str
    blog_summary_technical: str
    blog_summary_non_technical: str

    def get_filename(self):
        filename = f'{self.title.replace(" ", "_")}_summary.json'
        return filename
