# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

My project is a music recommendation system that suggests songs based on a user's music preferences. It compares features like genre, mood, energy, and tempo to determine how closely each song matches what the user likes. Each feature is given a different weight, and the system calculates a score for every song. It then ranks the songs from highest to lowest to recommend the best matches.

---

## How The System Works

Real world recommendation systems use data like listening history, likes, skips, and song features to predict what users might enjoy. They can recommend songs based on what similar users listen to or by comparing song attributes to a user's preferences. My system will focus on content-based filtering by comparing genre, mood, energy, and tempo. Genre and mood will have the highest weights, while energy and tempo will help determine how closely a song matches the user's preferences. Songs will then be ranked based on their scores to recommend the best matches.

Some prompts to answer:

- Each Song will store information such as genre, mood, energy, and tempo_bpm. These features will be used to compare songs to the user's preferences.
- The UserProfile will store the user's favorite_genre, favorite_mood, target_energy, target_tempo, and likes_acoustic. This information will help determine which songs best match their taste.
- The Recommender will calculate a score for each song based on how closely it matches the user's preferences. Genre will have a weight of 40%, mood 30%, energy 20%, and tempo 10%. Genre and mood will receive a similarity score of 1 if they match the user's preference and 0 if they don't. For energy and tempo, the system will calculate how close the song's values are to the user's preferred values. Each similarity score will be multiplied by its weight, and the results will be added together to give a final score between 0 and 1.
score = 0.40 * genre_sim + 0.30 * mood_sim + 0.20 * energy_sim + 0.10 * tempo_sim

For energy and tempo, similarity will be calculated using:
similarity = max(0, 1 - abs(song_value - preferred_value) / range)
- After calculating a score for each song, the system will sort all songs from highest to lowest and recommend the top 5 matches. Songs with higher scores will be considered better matches for the user's preferences.

Algorithim recipe:
Each song will receive a score out of 5 points based on four features:

- Genre (40%): A matching genre earns 2 points.

- Mood (30%): A matching mood earns 1.5 points.

- Energy (20%): Songs earn up to 1 point based on how close their energy level is to the user's preferred energy.

- Tempo (10%): Songs earn up to 0.5 points based on how close their BPM is to the user's preferred tempo.

- For energy, the system will use 1 - abs(song.energy - target_energy). For tempo, it will use 0.5 * max(0, 1 - abs(song.tempo_bpm - target_tempo) / 100).

After calculating the scores, the system will sort the songs from highest to lowest. If two songs have the same score, the song with energy closer to the user's preference will rank higher.

Potential Biases:
One potential bias is that the system might prioritize genre too much since it has the highest weight. This could cause songs with similar moods or energy levels to rank lower just because they belong to a different genre. The system also only rewards exact genre and mood matches, so it might overlook songs that are similar but not identical to the user's preferences.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
Loaded 20 songs from data/songs.csv

============================================================
                  TOP SONG RECOMMENDATIONS                  
============================================================
Genres : rock, synthwave, indie pop
Moods  : intense, moody, confident
Energy : 0.8   Tempo: 130 BPM
------------------------------------------------------------

#1  Night Drive Loop  by Neon Echo
    Score: 4.85 / 5.00   (synthwave, moody)
    Why:
      - genre match: synthwave (+2.0)
      - mood match: moody (+1.5)
      - energy 0.75 vs target 0.80 (+0.95)
      - tempo 110 BPM vs target 130 (+0.40)

#2  Storm Runner  by Voltline
    Score: 4.78 / 5.00   (rock, intense)
    Why:
      - genre match: rock (+2.0)
      - mood match: intense (+1.5)
      - energy 0.91 vs target 0.80 (+0.89)
      - tempo 152 BPM vs target 130 (+0.39)

#3  Rooftop Lights  by Indigo Parade
    Score: 3.43 / 5.00   (indie pop, happy)
    Why:
      - genre match: indie pop (+2.0)
      - energy 0.76 vs target 0.80 (+0.96)
      - tempo 124 BPM vs target 130 (+0.47)

#4  Gym Hero  by Max Pulse
    Score: 2.86 / 5.00   (pop, intense)
    Why:
      - mood match: intense (+1.5)
      - energy 0.93 vs target 0.80 (+0.87)
      - tempo 132 BPM vs target 130 (+0.49)

#5  Concrete Kingdom  by Block Theory
    Score: 2.80 / 5.00   (hip hop, confident)
    Why:
      - mood match: confident (+1.5)
      - energy 0.78 vs target 0.80 (+0.98)
      - tempo 94 BPM vs target 130 (+0.32)

============================================================
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



