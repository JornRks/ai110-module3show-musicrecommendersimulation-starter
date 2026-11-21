import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv with the csv module and return a list of dicts with numeric fields converted."""
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song: Dict = {}
            for key, value in row.items():
                key = key.strip()
                value = value.strip()
                if key in int_fields:
                    song[key] = int(value)
                elif key in float_fields:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, list of reasons)."""
    # Algorithm Recipe (max 5.0 points, plus an optional acoustic bonus):
    #   genre match       +2.0  (40%)
    #   mood match        +1.5  (30%)
    #   energy closeness  up to +1.0  (20%)
    #   tempo closeness   up to +0.5  (10%)
    #   acoustic bonus    +0.5  (only if the user specifies likes_acoustic)
    GENRE_POINTS = 2.0
    MOOD_POINTS = 1.5
    ENERGY_POINTS = 1.0
    TEMPO_POINTS = 0.5
    TEMPO_RANGE = 100.0  # a BPM gap this large (or more) earns 0 tempo points
    ACOUSTIC_POINTS = 0.5

    score = 0.0
    reasons: List[str] = []

    # Accept either a list ("favorite_genres") or a single value ("favorite_genre").
    def as_set(plural_key: str, singular_key: str) -> set:
        value = user_prefs.get(plural_key, user_prefs.get(singular_key, []))
        if isinstance(value, str):
            value = [value]
        return {v.strip().lower() for v in value}

    genres = as_set("favorite_genres", "favorite_genre")
    moods = as_set("favorite_moods", "favorite_mood")

    # 1. Genre match
    song_genre = str(song["genre"]).strip().lower()
    if song_genre in genres:
        score += GENRE_POINTS
        reasons.append(f"genre match: {song['genre']} (+{GENRE_POINTS:.1f})")

    # 2. Mood match
    song_mood = str(song["mood"]).strip().lower()
    if song_mood in moods:
        score += MOOD_POINTS
        reasons.append(f"mood match: {song['mood']} (+{MOOD_POINTS:.1f})")

    # 3. Energy similarity: closer to the target earns more points
    if "target_energy" in user_prefs:
        target_energy = float(user_prefs["target_energy"])
        energy = float(song["energy"])
        energy_points = ENERGY_POINTS * max(0.0, 1.0 - abs(energy - target_energy))
        score += energy_points
        reasons.append(
            f"energy {energy:.2f} vs target {target_energy:.2f} (+{energy_points:.2f})"
        )

    # 4. Tempo similarity: scaled so a gap of TEMPO_RANGE BPM or more earns 0
    if "target_tempo" in user_prefs:
        target_tempo = float(user_prefs["target_tempo"])
        tempo = float(song["tempo_bpm"])
        tempo_points = TEMPO_POINTS * max(0.0, 1.0 - abs(tempo - target_tempo) / TEMPO_RANGE)
        score += tempo_points
        reasons.append(
            f"tempo {tempo:.0f} BPM vs target {target_tempo:.0f} (+{tempo_points:.2f})"
        )

    # 5. Optional acoustic bonus
    if "likes_acoustic" in user_prefs:
        acousticness = float(song["acousticness"])
        if user_prefs["likes_acoustic"] and acousticness >= 0.6:
            score += ACOUSTIC_POINTS
            reasons.append(f"acoustic sound {acousticness:.2f} (+{ACOUSTIC_POINTS:.1f})")
        elif not user_prefs["likes_acoustic"] and acousticness < 0.4:
            score += ACOUSTIC_POINTS
            reasons.append(f"electronic/produced sound {acousticness:.2f} (+{ACOUSTIC_POINTS:.1f})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, rank highest first (ties broken by energy closeness), and return the top k."""
    target_energy = float(user_prefs.get("target_energy", 0.5))

    # Score every song once, keeping (song, score, explanation) together.
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    # Rank highest score first; break ties by energy closest to the target.
    ranked = sorted(
        scored,
        key=lambda item: (-item[1], abs(item[0]["energy"] - target_energy)),
    )

    return ranked[:k]
