import os
import requests

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


def _mock_videos(query: str, max_results: int = 3):
    results = []
    for i in range(1, max_results + 1):
        results.append({
            'id': f'mock{i}',
            'title': f'{query} — Quick Recipe Tutorial #{i}',
            'channel': 'Cooking Channel',
            'thumbnail': f'https://via.placeholder.com/320x180.png?text=Video+{i}'
        })
    return results


def search_videos(query: str, max_results: int = 3):
    # If API key is missing, return mock videos so UI still shows content
    if not YOUTUBE_API_KEY:
        return _mock_videos(query, max_results)
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': f"{query} recipe",
        'type': 'video',
        'maxResults': max_results,
        'key': YOUTUBE_API_KEY
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        items = resp.json().get('items', [])
        results = []
        for it in items:
            snip = it.get('snippet', {})
            results.append({
                'id': it['id']['videoId'],
                'title': snip.get('title'),
                'channel': snip.get('channelTitle'),
                'thumbnail': snip.get('thumbnails', {}).get('high', {}).get('url')
            })
        return results
    except Exception:
        # fallback to mock videos
        return _mock_videos(query, max_results)
