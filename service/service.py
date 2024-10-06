from flask import Flask, request, jsonify
from collections import defaultdict
import logging
import time
import threading

service = Flask(__name__)
#app.config["DEBUG"] = True
logging.basicConfig(level=logging.INFO)
lock = threading.Lock()

def compute_anagrams(file):
    anagrams = defaultdict(list)
    with open(file, 'r') as file:
        for word in file:
            word = word.strip() # remove this?
            # anagrams look the same when they are sorted
            sorted_word = ''.join(sorted(word))
            anagrams[sorted_word].append(word)
    return anagrams


anagrams = compute_anagrams(file='./words_clean.txt')
words_count = sum(len(words) for words in anagrams.values())
requests_count = 0
total_time_ns = 0


# endpoint for similar words
@service.route('/api/v1/similar', methods=['GET'])
def get_anagrams_for_word():
    global requests_count, total_time_ns
    try:
        word = request.args.get('word').strip()
        if not word:
            raise ValueError("Missing a word to find anagrams for")

        logging.info(f"finding anagrams for word: {word}")
        start_time = time.time_ns()
        sorted_word = ''.join(sorted(word))
        similar_words = [w for w in anagrams.get(sorted_word) if w != word]
        end_time = time.time_ns()
        with lock:
            # update stats, to be used later by [get_stats]
            requests_count += 1
            total_time_ns += (end_time - start_time)
        return jsonify({'similar': similar_words})
    except Exception as e:
        # this exception will be caught by handle_exception
        raise e


# endpoint for statistics of the service itself
@service.route('/api/v1/stats', methods=['GET'])
def get_stats():
    logging.info("fetching stats")
    avg_processing_time_ns = total_time_ns // requests_count if requests_count > 0 else 0
    return jsonify({
        'totalWords': words_count,
        'totalRequests': requests_count,
        'avgProcessingTimeNs': avg_processing_time_ns
    })


@service.errorhandler(Exception)
def handle_exception(e):
    logging.error(f"An error occurred: {e}")
    return jsonify({"error": "An error occurred"}), 500


if __name__ == '__main__':
    # listen on all available network interfaces on the machine.
    service.run(host='0.0.0.0', port=8000)
