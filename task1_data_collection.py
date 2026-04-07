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


def main():
    top_stories = fetch_top_story_ids()
    fetched_stories =[]
    category_counts = {cat: 0 for cat in CATEGORIES.keys() }

    print("Fetching and  categorizing stories ...")

    for category in CATEGORIES.keys():
        print(f"\n Processiing Category: {category}")

        for top_story in top_stories:
            if category_counts[category] >= MAX_PER_CATEGORY:
                break

            story = fecth_story(top_story)
            if not story:
                continue

            title = story.get("title","")
            assigned_category = story_category(title)
            if assigned_category != category:
                continue

            story_data ={
                "post_id": story.get("id"),
                "title": title,
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            fetched_stories.append(story_data)
            category_counts[category] += 1

        #Sleep After finishing each category
        time.sleep(2)
    
    #create data folder if it doesnot exist
    os.makedirs("data",exist_ok=True)

    #File name with current date
    filename =  f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    #save Json
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(fetched_stories, f, indent=4)

    print(f"\n collected {len(fetched_stories)} stories. saved to {filename}")

if __name__ == "__main__":
    main()