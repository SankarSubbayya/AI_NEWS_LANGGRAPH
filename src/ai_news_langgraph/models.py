from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional


class SubTopic(BaseModel):
    name: str
    description: str


class NewsItem(BaseModel):
    title: str
    url: str
    source: Optional[str] = None
    summary: Optional[str] = None
    relevance_score: Optional[float] = None


class SubtopicNews(BaseModel):
    sub_topic: SubTopic
    articles: List[NewsItem]


class CombinedNews(BaseModel):
    main_topic: str
    sub_topics: List[SubtopicNews]


