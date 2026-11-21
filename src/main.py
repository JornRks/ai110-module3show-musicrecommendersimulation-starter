"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# Standard taste profiles
# Genres and moods are lists, so a song gets credit if it matches ANY of them.
# Weights: genre 40%, mood 30%, energy 20%, tempo 10% (see score_song).
# ---------------------------------------------------------------------------
STANDARD_PROFILES = {
    "High-Energy Pop": {
        "favorite_genres": ["pop", "indie pop", "edm"],
        "favorite_moods": ["happy", "euphoric", "intense"],
        "target_energy": 0.90,
        "target_tempo": 125,
    },
    "Chill Lofi": {
        "favorite_genres": ["lofi", "ambient", "jazz"],
        "favorite_moods": ["chill", "relaxed", "focused"],
        "target_energy": 0.35,
        "target_tempo": 75,
        "likes_acoustic": True,
    },
    "Deep Intense Rock": {
        "favorite_genres": ["rock", "metal", "punk"],
        "favorite_moods": ["intense", "angry", "rebellious"],
        "target_energy": 0.92,
        "target_tempo": 160,
        "likes_acoustic": False,
    },
}


# ---------------------------------------------------------------------------
# Adversarial / edge-case profiles
# Each one is designed to probe a specific weakness in the scoring logic.
# ---------------------------------------------------------------------------
ADVERSARIAL_PROFILES = {
    # Conflict: wants very high energy but a sad mood. The only melancholic
    # song in the catalog is a 0.22-energy classical piece. Which signal wins?
    "Conflict: Hyper but Sad": {
        "favorite_genres": ["classical"],
        "favorite_moods": ["melancholic", "sad"],
        "target_energy": 0.90,
        "target_tempo": 150,
    },
    # Vocabulary gap: "sad" and "k-pop" never appear in songs.csv, so genre
    # and mood can never match. Ranking falls back to energy + tempo only.
    "Unknown Genre & Mood": {
        "favorite_genres": ["k-pop"],
        "favorite_moods": ["sad"],
        "target_energy": 0.80,
        "target_tempo": 120,
    },
    # Genre spam: listing every genre makes the 2.0 genre bonus universal,
    # so it stops discriminating at all.
    "Likes Every Genre": {
        "favorite_genres": [
            "pop", "lofi", "rock", "ambient", "jazz", "synthwave", "indie pop",
            "folk", "hip hop", "edm", "metal", "r&b", "reggae", "classical",
            "country", "punk", "trip hop",
        ],
        "favorite_moods": ["chill"],
        "target_energy": 0.50,
        "target_tempo": 100,
    },
    # Genre dominance: a metal fan who wants chill, quiet music. Does the
    # 2.0 genre bonus drag a 0.97-energy angry song above actual chill tracks?
    "Metal Fan Wants Calm": {
        "favorite_genres": ["metal"],
        "favorite_moods": ["chill"],
        "target_energy": 0.20,
        "target_tempo": 65,
    },
    # Out-of-range numbers: energy above 1.0 and an impossible tempo.
    # Energy points get clamped, tempo points all collapse to 0.
    "Out-of-Range Targets": {
        "favorite_genres": ["edm"],
        "favorite_moods": ["euphoric"],
        "target_energy": 1.50,
        "target_tempo": 300,
    },
    # Messy input: odd casing/whitespace and a bare string instead of a list.
    "Messy Casing & Types": {
        "favorite_genres": "  HIP HOP ",
        "favorite_moods": ["Confident"],
        "target_energy": "0.75",
        "target_tempo": 95,
    },
    # Empty profile: no preferences at all. Every song scores 0, so the
    # order is decided entirely by the tie-breaker (default energy 0.5).
    "Empty Profile": {},
}


def main() -> None:
    songs = load_songs("data/songs.csv")

    print("\n" + "#" * 60)
    print("STANDARD PROFILES".center(60))
    print("#" * 60)
    for name, prefs in STANDARD_PROFILES.items():
        recommendations = recommend_songs(prefs, songs, k=5)
        print_recommendations(name, prefs, recommendations)

    print("\n" + "#" * 60)
    print("ADVERSARIAL / EDGE-CASE PROFILES".center(60))
    print("#" * 60)
    for name, prefs in ADVERSARIAL_PROFILES.items():
        recommendations = recommend_songs(prefs, songs, k=5)
        print_recommendations(name, prefs, recommendations)


def _as_text(value) -> str:
    """Show a list or a bare string preference uniformly."""
    if value is None:
        return "(none)"
    if isinstance(value, str):
        return value
    return ", ".join(value) if value else "(none)"


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Print the ranked recommendations in a readable terminal layout."""
    width = 60
    print()
    print("=" * width)
    print(f"PROFILE: {name}".center(width))
    print("=" * width)
    print(f"Genres : {_as_text(user_prefs.get('favorite_genres'))}")
    print(f"Moods  : {_as_text(user_prefs.get('favorite_moods'))}")
    print(f"Energy : {user_prefs.get('target_energy')}   "
          f"Tempo: {user_prefs.get('target_tempo')} BPM")
    if "likes_acoustic" in user_prefs:
        print(f"Acoustic: {user_prefs['likes_acoustic']}")
    print("-" * width)

    if not recommendations:
        print("No recommendations found.")
        return

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f"#{rank}  {song['title']}  by {song['artist']}")
        print(f"    Score: {score:.2f}   ({song['genre']}, {song['mood']}, "
              f"energy {song['energy']:.2f})")
        print("    Why:")
        reasons = explanation.split("; ") if explanation else ["no matching features"]
        for reason in reasons:
            print(f"      - {reason}")

    print()
    print("=" * width)


if __name__ == "__main__":
    main()
