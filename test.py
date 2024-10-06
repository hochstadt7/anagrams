import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random
import logging

prefix_url = "http://my-service:8000/api/v1/"
base_word_url = f"{prefix_url}similar?word="
words = ["stressed", "apple", "banana", "listen", "silent", "evil", "vile", "enlist"]
num_requests = 100

# sends GET request to the server, and measures performance in ns
def send_request():
    word = random.choice(words)
    url = f"{base_word_url}{word}"
    start_time = time.time_ns()
    response = requests.get(url)
    end_time = time.time_ns()
    return {
        "url": url,
        "response_time_ns": end_time - start_time,
        "status_code": response.status_code,
        "content": response.json(),
    }


# using ThreadPoolExecutor to send multiple requests in parallel
def test_multi_requests():
    logging.info("Creating GET requests to the service")
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(send_request) for _ in range(num_requests)]
        for future in as_completed(futures):
            result = future.result()
            assert result['status_code'] == 200, f"request failed with status code {result["status_code"]}"

    stats_response = requests.get(f"{prefix_url}stats")
    assert stats_response.status_code == 200, f"request failed with status code {stats_response.status_code}"
    logging.info("Test passed")


# test the service's usability and performance when it is being accessed multiple times,
# in parallel
if __name__ == "__main__":
    test_multi_requests()
