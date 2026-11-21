"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Taste profile: an energetic listener who likes several related styles.
    # Genres and moods are lists, so a song gets credit if it matches ANY of them.
    user_prefs = {
        "favorite_genres": ["rock", "synthwave", "indie pop"],  # 40%
        "favorite_moods": ["intense", "moody", "confident"],    # 30%
        "target_energy": 0.80,                                  # 20% (0-1)
        "target_tempo": 130,                                    # 10% (BPM)
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(user_prefs, recommendations)


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Print the ranked recommendations in a readable terminal layout."""
    width = 60
    print()
    print("=" * width)
    print("TOP SONG RECOMMENDATIONS".center(width))
    print("=" * width)
    print(f"Genres : {', '.join(user_prefs.get('favorite_genres', []))}")
    print(f"Moods  : {', '.join(user_prefs.get('favorite_moods', []))}")
    print(f"Energy : {user_prefs.get('target_energy')}   "
          f"Tempo: {user_prefs.get('target_tempo')} BPM")
    print("-" * width)

    if not recommendations:
        print("No recommendations found.")
        return

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"#{rank}  {song['title']}  by {song['artist']}")
        print(f"    Score: {score:.2f} / 5.00   ({song['genre']}, {song['mood']})")
        print("    Why:")
        reasons = explanation.split("; ") if explanation else ["no matching features"]
        for reason in reasons:
            print(f"      - {reason}")

    print()
    print("=" * width)


if __name__ == "__main__":
    main()
