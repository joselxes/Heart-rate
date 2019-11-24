import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json",params={"key": "XpBeTod1UwDEF989WE4g", "isbns": "9781632168146"})
data=res.json()
rate=data["books"][0]["work_ratings_count"]
rate1=data["books"][0]["average_rating"]
print(rate,rate1)
