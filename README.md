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

- Each Song will store information such as genre, mood, energy, tempo_bpm, and acousticness. These features will be used to compare songs to the user's preferences.
- The user profile will store the user's favorite genres, favorite moods (one or more of each), target_energy, target_tempo, and optionally likes_acoustic. This information will help determine which songs best match their taste.
- The Recommender will calculate a score for each song based on how closely it matches the user's preferences. Genre will have a weight of 40%, mood 30%, energy 20%, and tempo 10%. Genre and mood will receive a similarity score of 1 if they match the user's preference and 0 if they don't. For energy and tempo, the system will calculate how close the song's values are to the user's preferred values. Each similarity score will be multiplied by its weight, and the results will be added together and multiplied by 5 to give a final score out of 5 points. score = 5 * (0.40 * genre_sim + 0.30 * mood_sim + 0.20 * energy_sim + 0.10 * tempo_sim)

For energy and tempo, similarity will be calculated using:
similarity = max(0, 1 - abs(song_value - preferred_value) / range)
where the range is 1.0 for energy (energy is already on a 0–1 scale) and 100 BPM for tempo.

- After calculating a score for each song, the system will sort all songs from highest to lowest and recommend the top 5 matches. Songs with higher scores will be considered better matches for the user's preferences.

### Algorithim recipe: 
Each song will receive a score out of 5 points based on four features:

- Genre (40%): A matching genre earns 2 points.

- Mood (30%): A matching mood earns 1.5 points.

- Energy (20%): Songs earn up to 1 point based on how close their energy level is to the user's preferred energy.

- Tempo (10%): Songs earn up to 0.5 points based on how close their BPM is to the user's preferred tempo.

- For energy, the system will use max(0, 1 - abs(song.energy - target_energy)). For tempo, it will use 0.5 * max(0, 1 - abs(song.tempo_bpm - target_tempo) / 100).

- Acoustic bonus (optional): If the user sets likes_acoustic, songs earn an extra 0.5 points when their sound fits that preference (acousticness of 0.6 or higher if they like acoustic music, below 0.4 if they don't). This is why some scores in the experiments go above 5, up to a maximum of 5.5.

After calculating the scores, the system will sort the songs from highest to lowest. If two songs have the same score, the song with energy closer to the user's preference will rank higher.

### Potential Biases:
One potential bias is that the system might prioritize genre too much since it has the highest weight. This could cause songs with similar moods or energy levels to rank lower just because they belong to a different genre. The system also only rewards exact genre and mood matches, so it might overlook songs that are similar but not identical to the user's preferences.

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
---

## Experiments You Tried

- What happened when you changed the weight on genre from 2.0 to 1.0 and doubled the weight on energy from 1.0 to 2.0 

Note: This was a temporary experiment. After recording these results, I changed the weights back to the original values.

| Feature | Before | After |
|---|---|---|
| Genre match | +2.0 (40%) | **+1.0 (20%)** |
| Mood match | +1.5 (30%) | +1.5 (30%) |
| Energy closeness | up to +1.0 (20%) | **up to +2.0 (40%)** |
| Tempo closeness | up to +0.5 (10%) | up to +0.5 (10%) |
| **Max score** | 5.0 | **5.0** |

**Results after the change** (top 5 per profile; ↑/↓ marks songs that moved compared with the original weights):

```text
#### High-Energy Pop
#1  Gym Hero                   Max Pulse        pop, intense             energy 0.93  score 4.90   ↑ (was #2)
#2  Pulse Cathedral            Kinetic Array    edm, euphoric            energy 0.95  score 4.89   ↓ (was #1)
#3  Sunrise City               Neon Echo        pop, happy               energy 0.82  score 4.80
#4  Rooftop Lights             Indigo Parade    indie pop, happy         energy 0.76  score 4.71
#5  Storm Runner               Voltline         rock, intense            energy 0.91  score 3.84

#### Chill Lofi
#1  Library Rain               Paper Lanterns   lofi, chill              energy 0.35  score 5.49
#2  Coffee Shop Stories        Slow Stereo      jazz, relaxed            energy 0.37  score 5.38   ↑ (was #4)
#3  Focus Flow                 LoRoom           lofi, focused            energy 0.40  score 5.38   ↓ (was #2)
#4  Midnight Coding            LoRoom           lofi, chill              energy 0.42  score 5.34   ↓ (was #3)
#5  Spacewalk Thoughts         Orbit Bloom      ambient, chill           energy 0.28  score 5.29

#### Deep Intense Rock
#1  Storm Runner               Voltline         rock, intense            energy 0.91  score 5.44
#2  Fever Grid                 Static Bloom     punk, rebellious         energy 0.90  score 5.38   ↑ (was #3)
#3  Ashfall                    Grave Meridian   metal, angry             energy 0.97  score 5.36   ↓ (was #2)
#4  Gym Hero                   Max Pulse        pop, intense             energy 0.93  score 4.34
#5  Pulse Cathedral            Kinetic Array    edm, euphoric            energy 0.95  score 2.78

#### Conflict: Hyper but Sad
#1  Requiem for Glass          Hollow Quartet   classical, melancholic   energy 0.22  score 3.22
#2  Storm Runner               Voltline         rock, intense            energy 0.91  score 2.47
#3  Fever Grid                 Static Bloom     punk, rebellious         energy 0.90  score 2.37   ↑ (was #4)
#4  Gym Hero                   Max Pulse        pop, intense             energy 0.93  score 2.35   ↓ (was #3)
#5  Pulse Cathedral            Kinetic Array    edm, euphoric            energy 0.95  score 2.29

#### Unknown Genre & Mood
#1  Sunrise City               Neon Echo        pop, happy               energy 0.82  score 2.45
#2  Rooftop Lights             Indigo Parade    indie pop, happy         energy 0.76  score 2.40
#3  Night Drive Loop           Neon Echo        synthwave, moody         energy 0.75  score 2.35
#4  Concrete Kingdom           Block Theory     hip hop, confident       energy 0.78  score 2.33
#5  Gym Hero                   Max Pulse        pop, intense             energy 0.93  score 2.18

#### Likes Every Genre
#1  Midnight Coding            LoRoom           lofi, chill              energy 0.42  score 4.73
#2  Library Rain               Paper Lanterns   lofi, chill              energy 0.35  score 4.56
#3  Spacewalk Thoughts         Orbit Bloom      ambient, chill           energy 0.28  score 4.36
#4  Neon Shadows               Kuro Drift       trip hop, mysterious     energy 0.48  score 3.42
#5  Dusty Highway Prayer       Copper Lanes     country, hopeful         energy 0.55  score 3.39

#### Metal Fan Wants Calm
#1  Spacewalk Thoughts         Orbit Bloom      ambient, chill           energy 0.28  score 3.81
#2  Library Rain               Paper Lanterns   lofi, chill              energy 0.35  score 3.67
#3  Midnight Coding            LoRoom           lofi, chill              energy 0.42  score 3.50
#4  Requiem for Glass          Hollow Quartet   classical, melancholic   energy 0.22  score 2.46   ↑ (was #5)
#5  Paper Hearts in the Rain   Willow Static    folk, nostalgic          energy 0.30  score 2.21   NEW (Ashfall dropped out)

#### Out-of-Range Targets
#1  Pulse Cathedral            Kinetic Array    edm, euphoric            energy 0.95  score 3.40
#2  Ashfall                    Grave Meridian   metal, angry             energy 0.97  score 0.94
#3  Gym Hero                   Max Pulse        pop, intense             energy 0.93  score 0.86
#4  Storm Runner               Voltline         rock, intense            energy 0.91  score 0.82
#5  Fever Grid                 Static Bloom     punk, rebellious         energy 0.90  score 0.80

#### Messy Casing & Types
#1  Concrete Kingdom           Block Theory     hip hop, confident       energy 0.78  score 4.93
#2  Night Drive Loop           Neon Echo        synthwave, moody         energy 0.75  score 2.42
#3  Rooftop Lights             Indigo Parade    indie pop, happy         energy 0.76  score 2.33
#4  Sunrise City               Neon Echo        pop, happy               energy 0.82  score 2.25
#5  Sol de Domingo             Banda Mareia     reggae, carefree         energy 0.58  score 2.12

#### Empty Profile
#1  Velvet Hours               June Calloway    r&b, romantic            energy 0.52  score 0.00
#2  Neon Shadows               Kuro Drift       trip hop, mysterious     energy 0.48  score 0.00
#3  Dusty Highway Prayer       Copper Lanes     country, hopeful         energy 0.55  score 0.00
#4  Sol de Domingo             Banda Mareia     reggae, carefree         energy 0.58  score 0.00
#5  Midnight Coding            LoRoom           lofi, chill              energy 0.42  score 0.00
```

**What happened when I doubled energy and halved genre:**

The change made the recommendations **mostly different, and only slightly more accurate**.

- **Standard profiles mostly just reshuffled.** The same songs stayed in the top 5, but songs whose energy is closest to the target moved up (for example, Gym Hero passed Pulse Cathedral, and Fever Grid passed Ashfall). These songs were already within about 0.05 points of each other, so the "new" order reflects tiny energy differences, not a real improvement.
- **The gap between genre matches and non-matches shrank.** For High-Energy Pop, the #5 song (Storm Runner, wrong genre) went from 2.86 to 3.84, much closer to the top 4. Genre now matters less, so off-genre high-energy songs compete more.
- **One real improvement: Metal Fan Wants Calm.** Before, Ashfall (angry, energy 0.97) was #4 only because it was metal. With genre worth just 1.0, it fell out of the top 5 and was replaced by another quiet song (Paper Hearts in the Rain). That is closer to what this user asked for.
- **It did not fix the "Hyper but Sad" conflict.** Requiem for Glass (energy 0.22) is still #1, because genre + mood (1.0 + 1.5 = 2.5) still beat the extra energy points. The gap did shrink, from 2.42 to 0.75 points, so the system is closer to flipping but still ignores the user's energy request.
- **Profiles with no genre or mood match** (Unknown Genre & Mood, Messy Casing #2–#5) kept the same order, and their scores just went up by about 1 point. Their ranking was already based on energy alone, so doubling its weight changed the numbers but not the order.

**Conclusion:** The system is sensitive to the weights at the top of the list, where songs are nearly tied, but the overall picture stays the same. The weight shift helped in one edge case (genre no longer drags in a mismatched song), but it didn't fix the bigger problem: categorical matches (genre + mood) still outweigh numeric preferences when they conflict.

- How did your system behave for different types of users:
I ran `python -m src.main` against 10 user profiles: 3 standard profiles and 7 adversarial/edge-case profiles designed to try to "trick" the scoring logic. Below are the top 5 results for each (max score is 5.0, or 5.5 with the acoustic bonus). These results use the **original weights** (genre 2.0, mood 1.5, energy 1.0, tempo 0.5). See the weight-shift experiment above for the comparison.

#### Standard profiles

**High-Energy Pop** (genres: pop, indie pop, edm · moods: happy, euphoric, intense · energy 0.90 · tempo 125)

```text
#1  Pulse Cathedral            Kinetic Array    edm, euphoric            energy 0.95  score 4.94
#2  Gym Hero                   Max Pulse        pop, intense             energy 0.93  score 4.93
#3  Sunrise City               Neon Echo        pop, happy               energy 0.82  score 4.88
#4  Rooftop Lights             Indigo Parade    indie pop, happy         energy 0.76  score 4.86
#5  Storm Runner               Voltline         rock, intense            energy 0.91  score 2.86
```

**Chill Lofi** (genres: lofi, ambient, jazz · moods: chill, relaxed, focused · energy 0.35 · tempo 75 · likes acoustic)

```text
#1  Library Rain               Paper Lanterns   lofi, chill              energy 0.35  score 5.49
#2  Focus Flow                 LoRoom           lofi, focused            energy 0.40  score 5.42
#3  Midnight Coding            LoRoom           lofi, chill              energy 0.42  score 5.42
#4  Coffee Shop Stories        Slow Stereo      jazz, relaxed            energy 0.37  score 5.41
#5  Spacewalk Thoughts         Orbit Bloom      ambient, chill           energy 0.28  score 5.35
```

**Deep Intense Rock** (genres: rock, metal, punk · moods: intense, angry, rebellious · energy 0.92 · tempo 160 · prefers electronic/produced sound)

```text
#1  Storm Runner               Voltline         rock, intense            energy 0.91  score 5.45
#2  Ashfall                    Grave Meridian   metal, angry             energy 0.97  score 5.41
#3  Fever Grid                 Static Bloom     punk, rebellious         energy 0.90  score 5.40
#4  Gym Hero                   Max Pulse        pop, intense             energy 0.93  score 3.35
#5  Pulse Cathedral            Kinetic Array    edm, euphoric            energy 0.95  score 1.81
```

#### Adversarial / edge-case profiles

**Conflict: Hyper but Sad** (genre: classical · moods: melancholic, sad · energy 0.90 · tempo 150)

```text
#1  Requiem for Glass          Hollow Quartet   classical, melancholic   energy 0.22  score 3.90
#2  Storm Runner               Voltline         rock, intense            energy 0.91  score 1.48
#3  Gym Hero                   Max Pulse        pop, intense             energy 0.93  score 1.38
#4  Fever Grid                 Static Bloom     punk, rebellious         energy 0.90  score 1.37
#5  Pulse Cathedral            Kinetic Array    edm, euphoric            energy 0.95  score 1.34
```

The system was "tricked." Genre + mood (3.5 points) completely outweigh energy (max 1.0), so the calmest song in the catalog (energy 0.22) ranks #1 for a user who asked for 0.90 energy.

**Unknown Genre & Mood** (genre: k-pop · mood: sad · energy 0.80 · tempo 120)

```text
#1  Sunrise City               Neon Echo        pop, happy               energy 0.82  score 1.47
#2  Rooftop Lights             Indigo Parade    indie pop, happy         energy 0.76  score 1.44
#3  Night Drive Loop           Neon Echo        synthwave, moody         energy 0.75  score 1.40
#4  Concrete Kingdom           Block Theory     hip hop, confident       energy 0.78  score 1.35
#5  Gym Hero                   Max Pulse        pop, intense             energy 0.93  score 1.31
```

 Neither "k-pop" nor "sad" exists in the catalog, so no song can get genre or mood points. Ranking falls back to energy + tempo only. The user is never told their genre wasn't found, and a "sad" user gets "happy" songs on top.

**Likes Every Genre** (all 17 genres · mood: chill · energy 0.50 · tempo 100)

```text
#1  Midnight Coding            LoRoom           lofi, chill              energy 0.42  score 4.81
#2  Library Rain               Paper Lanterns   lofi, chill              energy 0.35  score 4.71
#3  Spacewalk Thoughts         Orbit Bloom      ambient, chill           energy 0.28  score 4.58
#4  Neon Shadows               Kuro Drift       trip hop, mysterious     energy 0.48  score 3.44
#5  Dusty Highway Prayer       Copper Lanes     country, hopeful         energy 0.55  score 3.44
```

Every song gets the +2.0 genre bonus, so genre stops mattering and mood decides the ranking. Scores are inflated for every song, which makes them look like strong matches when they aren't.

**Metal Fan Wants Calm** (genre: metal · mood: chill · energy 0.20 · tempo 65)

```text
#1  Spacewalk Thoughts         Orbit Bloom      ambient, chill           energy 0.28  score 2.90
#2  Library Rain               Paper Lanterns   lofi, chill              energy 0.35  score 2.81
#3  Midnight Coding            LoRoom           lofi, chill              energy 0.42  score 2.72
#4  Ashfall                    Grave Meridian   metal, angry             energy 0.97  score 2.23
#5  Requiem for Glass          Hollow Quartet   classical, melancholic   energy 0.22  score 1.48
```

Mood + energy narrowly beat the genre bonus, so the chill songs win. But Ashfall (angry, energy 0.97) still lands at #4 on genre alone, even though it is the opposite of what the user wants.

**Out-of-Range Targets** (genre: edm · mood: euphoric · energy 1.50 · tempo 300)

```text
#1  Pulse Cathedral            Kinetic Array    edm, euphoric            energy 0.95  score 3.95
#2  Ashfall                    Grave Meridian   metal, angry             energy 0.97  score 0.47
#3  Gym Hero                   Max Pulse        pop, intense             energy 0.93  score 0.43
#4  Storm Runner               Voltline         rock, intense            energy 0.91  score 0.41
#5  Fever Grid                 Static Bloom     punk, rebellious         energy 0.90  score 0.40
```

Nothing crashes, but there is no input validation. Every song gets 0 tempo points, and energy points shrink for all songs. The system silently accepts impossible values.

**Messy Casing & Types** (genre: `"  HIP HOP "` as a plain string · mood: Confident · energy `"0.75"` as text · tempo 95)

```text
#1  Concrete Kingdom           Block Theory     hip hop, confident       energy 0.78  score 4.96
#2  Night Drive Loop           Neon Echo        synthwave, moody         energy 0.75  score 1.43
#3  Rooftop Lights             Indigo Parade    indie pop, happy         energy 0.76  score 1.34
#4  Sunrise City               Neon Echo        pop, happy               energy 0.82  score 1.31
#5  Sol de Domingo             Banda Mareia     reggae, carefree         energy 0.58  score 1.29
```

Handled correctly. Whitespace and capitalization are normalized, a single string is accepted in place of a list, and the energy text is converted to a number.

**Empty Profile** (no preferences)

```text
#1  Velvet Hours               June Calloway    r&b, romantic            energy 0.52  score 0.00
#2  Neon Shadows               Kuro Drift       trip hop, mysterious     energy 0.48  score 0.00
#3  Dusty Highway Prayer       Copper Lanes     country, hopeful         energy 0.55  score 0.00
#4  Sol de Domingo             Banda Mareia     reggae, carefree         energy 0.58  score 0.00
#5  Midnight Coding            LoRoom           lofi, chill              energy 0.42  score 0.00
```

Every song scores 0.00, so the order comes entirely from the tie-breaker (energy closest to a default of 0.5). The system still returns a confident-looking "top 5" instead of saying it has nothing to go on.

#### Summary

- The system works well for clear, consistent tastes (all 3 standard profiles).
- Genre + mood (3.5 of 5 points) dominate, so they can override what the user said about energy (Hyper but Sad, Metal Fan Wants Calm).
- Genre and mood require exact word matches: "sad" never matches "melancholic," and unknown genres fail silently.
- There is no input validation: out-of-range values and empty profiles still produce recommendations without any warning.

---

## Limitations and Risks

One limitation of my recommender is that it only uses a dataset of 20 songs, so there aren't many options for certain genres. The system also relies on exact genre and mood matches, which can cause it to overlook songs with similar characteristics. Another issue is that certain features can have too much influence on the final score, causing songs to rank highly even when they don't match the user's other preferences. 

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

This project helped me understand how recommendation systems use data and weighted scoring to predict what listeners enjoy. I learned that changing the importance of differing features can affect which songs get recommended, but it doesn't always improve the results. It also showed me how bias can come from both the dataset and the algorithm itself. 
Throughout this project I utalized Claude Code to help me draft my ideal and implement logic in my application. Claude also helped me develop my user profiles, more specificslly, edge case user profiles which I used to stress test my application. If I extended this project, the next thing I would add would be input validation so my model dosent recommend songs when not given sufficent information.



