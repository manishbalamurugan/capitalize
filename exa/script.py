from exa_py import Exa
from openai import OpenAI
import json
import pymongo
from pymongo import MongoClient
from pymongo.server_api import ServerApi

EXA_API_KEY = 'ENV.EXA_API_KEY'
exa = Exa(api_key = EXA_API_KEY)

# Initialize OpenAI API
client = OpenAI(
    api_key = 'ENV.OPENAI_API_KEY',
)

# MongoDB connection
uri = "mongodb+srv://manish:lemoncherrygelato@v0.b0xcqmc.mongodb.net/?retryWrites=true&w=majority&appName=v0"
mongo_client = MongoClient(uri, server_api=ServerApi('1'))
db = mongo_client['v0']

def generate_openai_response(query):
    prompt = f"""
        When provided a list of SearchResponses, transform each of the items about startups into concise posts suitable for a social media or 
        news app. The posts should include the title, URL, ID, a brief summary, and key highlights (generate based on the summary if not available). Ensure that the summary is clear and the information is easy to digest.

        Your response must be in a JSON object with the following structure:
        {{
            "posts": [
                {{
                    "title": "",
                    "url": "",
                    "id": "",
                    "summary": "",
                    "highlights": []
                }}
            ]
        }}
        """

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": query}
    ]

    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
    )
    return json.loads(response.choices[0].message.content)

def fetch_similar_sites(url):
    response = exa.find_similar_and_contents(url, text=True, highlights=True, num_results=2)
    response = str(response)
    return generate_openai_response(response)

# Exa API Fetch Company Data
def fetch_company_news(company_name):
    response = exa.search_and_contents(query=company_name, num_results=10, use_autoprompt=True, type='neural')
    response = str(response)
    return generate_openai_response(response)

def display_feed(news_feed):
    print(json.dumps(news_feed, indent=2))

def store_feed_in_db(company_id, feed_data):
    feed_collection = db['feed']
    for post in feed_data['posts']:
        feed_item = {
            "company_id": company_id,
            "title": post['title'],
            "content": post['summary'],
            "published_at": None,  # You might want to add a timestamp here
            "source": post['url']
        }
        feed_collection.insert_one(feed_item)

def get_company_id(company_name):
    companies_collection = db['company_profiles']
    company = companies_collection.find_one({"company_name": company_name})
    return company['_id'] if company else None

def main():
    company_name = "Reflex (YC W23)"
    company_id = get_company_id(company_name)
    
    if company_id:
        prompt = f'Latest updates on the following startup: {company_name}'
        news_feed = fetch_company_news(prompt)
        display_feed(news_feed)
        store_feed_in_db(company_id, news_feed)
    else:
        print(f"Company '{company_name}' not found in the database.")

    #site_feed = fetch_similar_sites("https://reflex.dev/")
    #display_feed(site_feed)

if __name__ == "__main__":
    main()