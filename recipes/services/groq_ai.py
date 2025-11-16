import os
import requests
import json

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_API_URL = os.getenv('GROQ_API_URL', 'https://api.groq.ai/v1/llama3/generate')


def _mock_recipe_from_ingredients(ingredients: str) -> dict:
    items = [i.strip() for i in ingredients.split(',') if i.strip()]
    title = ' / '.join(items[:3]) + ' Bowl' if items else 'Simple Recipe'
    return {
        'title': title,
        'description': f'A delicious {title.lower()} created from your ingredients.',
        'time': f"{15 + len(items)*5} mins",
        'difficulty': 'easy' if len(items) <= 3 else 'medium',
        'ingredients': items or ['water', 'salt'],
        'steps': [
            f'Prepare the ingredients: {", ".join(items)}.',
            'Combine everything in a bowl and season to taste.',
            'Cook or serve as needed.'
        ]
    }


def generate_recipe(ingredients: str) -> dict:
    """Generate a recipe using Groq Llama-3 when available.
    If `GROQ_API_KEY` is not set or remote call fails, return a deterministic mock recipe so the UI works.
    """
    if not GROQ_API_KEY:
        return _mock_recipe_from_ingredients(ingredients)

    prompt = f"""
You are an expert chef. Given the ingredients below, output a JSON object with keys:
title, description, time, difficulty, ingredients (array), steps (array).
Ingredients: {ingredients}
Return only valid JSON.
"""
    headers = {'Authorization': f'Bearer {GROQ_API_KEY}', 'Content-Type': 'application/json'}
    payload = {'prompt': prompt, 'max_tokens': 600}
    try:
        resp = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        text = data.get('text') or data.get('output') or ''
        try:
            parsed = json.loads(text)
            return parsed
        except Exception:
            # try to extract JSON substring
            import re
            m = re.search(r"\{.*\}", text, re.S)
            if m:
                try:
                    return json.loads(m.group(0))
                except Exception:
                    pass
    except Exception:
        # network / parse errors fall through to mock
        pass

    return _mock_recipe_from_ingredients(ingredients)
