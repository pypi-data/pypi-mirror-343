# SignalWire ML

A Python package for generating SignalWire ML configurations.

## Installation 

## SignalWireSWML Class

The `SignalWireSWML` class is the core of this package. It allows you to programmatically build, configure, and export SWML (SignalWire Markup Language) configurations for AI-powered agents and applications.

### Key Features
- Add standard and AI applications to sections
- Configure AI prompts, post-prompts, hints, languages, and parameters
- Integrate SWAIG (SignalWire AI Gateway) functions, includes, and defaults
- Output configurations as JSON or YAML, with optional ordering for consistency

### Example: Building a MovieBot AI Agent

Below is a complete example of how to use `SignalWireSWML` to build a MovieBot agent with advanced AI and SWAIG integration:

```python
from signalwire_swml import SignalWireSWML

def build_movie_ai_agent():
    swml = SignalWireSWML(version="1.0.0")

    # Add standard applications
    swml.add_application("main", "answer")
    swml.add_application("main", "record_call", {
        "format": "wav",
        "stereo": True
    })

    # Set up SWAIG defaults and includes
    swml.add_aiswaigdefaults({
        "web_hook_url": "https://botworks/swaig/1/11"
    })
    swml.add_aiinclude({
        "url": "https://moviebot/swaig",
        "functions": [
            "search_movie",
            "get_movie_details",
            "discover_movies",
            "get_trending_movies",
            "get_movie_recommendations",
            "get_genre_list",
            "get_upcoming_movies",
            "get_similar_movies",
            "get_now_playing_movies",
            "multi_search",
            "get_person_detail",
            "get_movie_credits"
        ]
    })

    # Set AI language
    swml.add_ailanguage({
        "code": "en-US",
        "language": "English",
        "name": "English",
        "voice": "openai.alloy"
    })

    # Set AI params
    swml.add_aiparams({
        "debug_webhook_level": "2",
        "debug_webhook_url": "https://botworks/debugwebhook/1/11",
        "enable_accounting": "true"
    })

    # Set AI post prompt
    swml.set_aipost_prompt({
        "max_tokens": 0,
        "temperature": 0.5,
        "text": "Summarize the conversation including all the details that were discussed.",
        "top_p": 0.5
    })

    # Set AI post prompt URL
    swml.set_aipost_prompt_url({
        "post_prompt_url": "https://botworks/postprompt/1/11"
    })

    # Set AI prompt
    swml.set_aiprompt({
        "temperature": 0.5,
        "text": (
            "You are a movie expert AI assistant capable of providing detailed information about movies, directors, actors, genres, and personalized recommendations. "
            "You have access to the following functions to retrieve up-to-date movie data:\n\n"
            "1. search_movie: Search for movies by title.\n   - Parameters: query, language (default: \"en-US\")\n"
            "2. get_movie_details: Retrieve detailed information about a movie.\n   - Parameters: movie_id, language (default: \"en-US\")\n"
            "3. discover_movies: Discover movies by different criteria.\n   - Parameters: with_genres, primary_release_year, sort_by (default: \"popularity.desc\"), language (default: \"en-US\")\n"
            "4. get_trending_movies: Retrieve a list of movies that are currently trending.\n   - Parameters: time_window (default: \"week\"), language (default: \"en-US\")\n"
            "5. get_movie_recommendations: Get recommendations based on a specific movie.\n   - Parameters: movie_id, language (default: \"en-US\")\n"
            "6. get_movie_credits: Retrieve cast and crew information for a movie.\n   - Parameters: movie_id, language (default: \"en-US\")\n"
            "7. get_person_details: Retrieve detailed information about a person.\n   - Parameters: person_id, language (default: \"en-US\"), append_to_response\n"
            "8. get_genre_list: Retrieve the list of official genres.\n   - Parameters: language (default: \"en-US\")\n"
            "9. get_upcoming_movies: Retrieve movies that are soon to be released.\n   - Parameters: language (default: \"en-US\"), region\n"
            "10. get_now_playing_movies: Retrieve movies currently playing in theaters.\n    - Parameters: language (default: \"en-US\"), region\n"
            "11. get_similar_movies: Retrieve movies similar to a specified movie.\n    - Parameters: movie_id, language (default: \"en-US\")\n"
            "12. multi_search: Search for movies, TV shows, and people with a single query.\n    - Parameters: query, language (default: \"en-US\")\n\n"
            "When a user asks a question, determine if any of these functions can help provide the most accurate and up-to-date information. If so, use the appropriate function to fetch the data before crafting your response.\n\n"
            "Guidelines:\n"
            "- Always provide accurate and helpful information.\n"
            "- Use the latest data from the functions whenever possible.\n"
            "- Maintain a conversational and friendly tone.\n"
            "- Respect user preferences and provide personalized recommendations.\n"
            "- Adhere to OpenAI's policies and avoid disallowed content.\n\n"
            "Example:\n"
            "- User: \"Can you recommend a good sci-fi movie from last year?\"\n"
            "- Assistant:\n"
            "  1. Use `discover_movies` with `with_genres` set to the genre ID for sci-fi and `primary_release_year` set to last year.\n"
            "  2. Fetch the list of movies.\n"
            "  3. Recommend a movie from the list with a brief description.\n"
        ),
        "top_p": 0.5
    })

    # Add the AI application to the main section
    swml.add_aiapplication("main")

    # Output as JSON or YAML
    print(swml.render_json(ordered=True))
    # print(swml.render_yaml(ordered=True))  # Uncomment for YAML output

if __name__ == "__main__":
    build_movie_ai_agent()

---

For more details on the available methods, see the docstrings in the `SignalWireSWML` class or the [API documentation](#). 