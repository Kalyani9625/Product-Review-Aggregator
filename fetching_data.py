import requests
from bs4 import BeautifulSoup

target_url = "https://www.amazon.in/Apple-iPhone-13-128GB-Product/product-reviews/B09G99CW2N/ref=cm_cr_arp_d_viewopt_srt?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber=1&filterByStar=all_stars"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'}

review_div_ids = ["viewpoint-R3GOVGYSAE4XKY", "viewpoint-R2CT5DGNONWDZ2", "R2L404SBO4GNSS", "R3PPPVAXHKMD4W", "R4Y46DDQN0R5O", "R3I6ZT9GWVQQLR", "R23UYJ76AQOA0F", "R2FN1MJ0HBS7WP", "R236WVG304NZ24", "R1OMHMI8XD3ZLC", "R1655J7UU1AFPL", "R115H9MIG0F7QL"]

# --- Fetch and parse HTML ---
response = requests.get(target_url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# --- Extract reviews ---
reviews =[]
for review_id in review_div_ids:
    review_div = soup.find("div", id=review_id)  # Find the specific review

    if review_div:  # Check if the review element exists
        review_text = review_div.get_text(strip=True)
        reviews.append(review_text)
    else:
        print(f"Review with ID {review_id} not found.")


# --- Store reviews in a file ---
with open("reviews.txt", "w", encoding="utf-8") as f:
    for review in reviews:
        f.write(review + "\n")
