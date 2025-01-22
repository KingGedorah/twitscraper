import asyncio
from twikit import Client
from configparser import ConfigParser
import json
import csv


QUERY = '#02 since:2023-11-01 until:2024-02-14 lang:id'

# Initialize client
client = Client('en-US')

async def main():
    
    # config = ConfigParser()
    # config.read('config.ini')
    # username = config['X']['username']
    # email = config['X']['email']
    # password = config['X']['password']
    
    # await client.login(auth_info_1=username, auth_info_2=email, password=password)
    # client.save_cookies('cookies.json')
    
    client.load_cookies('cookies.json')
    
    all_tweet_ids = set()
    
    tweets = await client.search_tweet(QUERY, 'Latest')
    
    with open('02.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'text', 'created_at', 'hashtags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while tweets:
            for tweet in tweets:
                if tweet.id not in all_tweet_ids:
                    all_tweet_ids.add(tweet.id)  # Add the tweet ID to the set

                    # Write the tweet to the CSV file
                    writer.writerow({
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at_datetime,
                        'hashtags': ', '.join(tweet.hashtags) if tweet.hashtags else '',
                    })

            # Check if there's a next batch of tweets
            if tweets.next:
                tweets = await tweets.next()
            else:
                break

    print(f'Tweets saved to 02.csv')


asyncio.run(main())