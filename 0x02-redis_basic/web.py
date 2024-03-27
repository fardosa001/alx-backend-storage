#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker
obtain the HTML content of a particular URL and returns it."""
import requests
import redis


def get_page(url: str) -> str:
    """ track how many times a particular URL was accessed in the key
        "count:{url}"
        and cache the result with an expiration time of 10 seconds """
    redis_client = redis.Redis()

    redis_client.incr(f"count:{url}")
    resp = requests.get(url)
    content = resp.text

    redis_client.setex(url, 10, content)

    return content


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
