import requests
import time
import os
import json
from datetime import datetime
from config import STORIES_URL, STORY_URL, HEADERS, CATEGORIES, MAX_PER_CATEGORY, MAX_TOP_STORIES

def fetch_top_story_ids():
    try:
        response = requests.get(STORIES_URL,headers= HEADERS)
        response.raise_for_status()
        return response.json()[:500]
    except Exception as e:
        print(f"Error While Fetching the Top Stories from {STORIES_URL} : {e}")
        return []

def fecth_story(id):
    try:
        story = requests.get(STORY_URL.format(id), headers= HEADERS)
        story.raise_for_status()
        return story.json()
    except Exception as e:
        print(f"Error occured while fetching the story with {id} : {e}")
        return None
    
def story_category(title):
    if not title:
        return None
    
    title_lower = title.lower()
    for category,keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    
    return None

