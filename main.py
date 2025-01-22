import asyncio
from twikit import Client
from configparser import ConfigParser
import json
import csv


QUERY = '#01 since:2023-11-01 until:2024-02-14 lang:id'

# Initialize client
client = Client('en-US')

async def TwikitScrape():
    
    # config = ConfigParser()
    # config.read('config.ini')
    # username = config['X']['username']
    # email = config['X']['email']
    # password = config['X']['password']
    
    # await client.login(auth_info_1=username, auth_info_2=email, password=password)
    # client.save_cookies('cookies.json')
    
    client.load_cookies('cookies.json')
    
    all_tweet_ids = set()
    processed_count = 0
    
    tweets = await client.search_tweet(QUERY, 'Latest')
    
    with open('01.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'text', 'created_at', 'hashtags']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        while tweets:
            for tweet in tweets:
                if tweet.id not in all_tweet_ids:
                    all_tweet_ids.add(tweet.id)  # Add the tweet ID to the set
                    processed_count += 1  # Increment the counter

                    # Write the tweet to the CSV file
                    writer.writerow({
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at_datetime,
                        'hashtags': ', '.join(tweet.hashtags) if tweet.hashtags else '',
                    })

                    # Sleep for 3 minutes after processing 100 tweets
                    if processed_count % 100 == 0:
                        print(f'{processed_count} tweets processed. Sleeping for 3 minutes...')
                        csvfile.flush()  # Ensure all data is written to the file before pausing
                        await asyncio.sleep(180) 

            # Check if there's a next batch of tweets
            if tweets.next:
                tweets = await tweets.next()
            else:
                break

    print(f'Tweets saved to 01.csv')


asyncio.run(TwikitScrape())