# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  
**MusicMatch v1  - Content-Based Music Recommender**  
---

## 2. Intended Use  

My music recommender is designed to suggest songs based on a user's preferences, including their favorite genres, moods, energy level, and tempo. It assumes the user has a general idea of what kind of music they enjoy. The system compares these preferences to the available songs and recommends the top 5 matches. This is mainly a coursework related project to explore how recommendation systems work rather than an application intended for real users.

---

## 3. How the Model Works  

My recommender uses content-based filtering to compare each song's features to the user's preferences. It looks at genre, mood, energy, and tempo, giving each feature a different weight based on its importance. Genre and mood earn points for exact matches, while energy and tempo earn points based on how close they are to the user's preferred values. The system also considers whether the user prefers acoustic music. It adds these points together to give each song a final score, then ranks the songs from highest to lowest and recommends the top 5. I also experimented with increasing the weight of energy and lowering genre to see how it affected the results.

---

## 4. Data  

My system uses a CSV dataset containing 20 songs across 17 different genres, including pop, rock, lofi, jazz, metal, and electronic music. Each song includes information such as its title, artist, genre, mood, energy, tempo, valence, danceability, and acousticness. I used the provided dataset without adding or removing any songs. One limitation is that most genres only have one song, so the system doesn't have many options for certain music preferences. It also doesn't include information like lyrics, listening history, or user ratings, which could help make recommendations more accurate.
---

## 5. Strengths  

My recommender works well when users have clear music preferences that match the available songs. For example, the High-Energy Pop profile received mostly energetic pop and EDM songs, while the Chill Lofi profile received slower, more relaxing music. The Deep Intense Rock profile also recommended rock, metal, and punk songs near the top. I think the system does a good job of distinguishing between different music tastes and explaining why each song was recommended.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 
  

The biggest weakness I found is a genre-and-mood filter bubble caused by exact-word matching on a very thin catalog: 14 of the 17 genres in `songs.csv` have only one song, and only lofi has more than two. That means a fan of a genre like classical or metal can only ever get genre points for a single song, and if that song also matches their mood it gets locked into the #1 spot no matter how badly it fits their other preferences. In my "Hyper but Sad" experiment, a user asking for 0.90 energy got a 0.22-energy classical requiem as their top pick, and even after I doubled the energy weight and halved the genre weight, the requiem still won because genre + mood together still outweighed energy. At the same time, lofi listeners get three strong genre matches, so the system quietly serves them better than fans of underrepresented genres. The energy gap adds a smaller related bias: because energy points drop off linearly from the target, a user with an extreme target like 0.0 averages only about 0.39 energy points per song, compared with about 0.77 for a user targeting 0.5, so mid-energy tastes look like "better matches" across the board.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 
- Profiles I tested: 
I tested 10 listener profiles against the 20-song catalog and looked at the top 5 songs for each:

- **3 normal listeners:** High-Energy Pop, Chill Lofi, and Deep Intense Rock.
- **7 "trick" listeners** built to find weak spots:
  - Hyper but Sad: wants high energy but a sad mood.
  - Unknown Genre & Mood: asks for k-pop and "sad," which aren't in the catalog.
  - Likes Every Genre: lists all 17 genres.
  - Metal Fan Wants Calm: likes metal but wants quiet, chill music.
  - Out-of-Range Targets: asks for impossible energy and tempo values.
  - Messy Casing & Types: types its preferences with odd capitals and spaces.
  - Empty Profile: gives no preferences at all.

For each one I asked: do the top songs actually sound like what this person asked for, and can I explain why each song made the list? I also ran every profile again after doubling the importance of energy and halving the importance of genre, to see how sensitive the results are.

### What surprised me

- The "Hyper but Sad" listener asked for very energetic music, but got the quietest song in the whole catalog (a slow classical piece) at #1. Matching the genre and mood labels earned that song more points than being the right energy, even after I made energy count twice as much.
- When I asked for a genre that doesn't exist (k-pop) or gave no preferences at all, it still returned a confident-looking top 5 rather than saying "I have nothing to go on."
- Doubling energy mostly swapped songs that were already nearly tied. Only one profile (Metal Fan Wants Calm) actually got a better list.

### Comparing profiles side by side

- High-Energy Pop vs. Chill Lofi: These two lists don't share a single song. The pop list is full of loud, fast, dance-y tracks (energy 0.76–0.95), while the lofi list is all quiet, slow, acoustic tracks (energy 0.28–0.42). This makes sense because the two listeners disagree on every setting: genre, mood, energy, tempo and acoustic sound. It's a good sign the system can tell opposite tastes apart.

- High-Energy Pop vs. Deep Intense Rock: Both lists want very high energy, so they share some songs. Gym Hero and Pulse Cathedral appear on both, and Storm Runner (rock) appears at #5 on the pop list. The difference is the order: the rock fan's top 3 are all rock, metal or punk, and pop songs only show up afterward as "high energy, wrong genre" filler. That's valid, because when energy matches, genre and mood decide the winner.

- Chill Lofi vs. Deep Intense Rock: These are complete opposites, with zero overlap. The lofi listener prefers acoustic sound and gets a bonus for guitar- and piano-heavy tracks, while the rock listener gets a bonus for electronic, heavily produced sound. This shows the acoustic setting pushes the two lists even further apart.

- Deep Intense Rock vs. Hyper but Sad: Both ask for about 0.9 energy, but their #1 songs are as different as possible: Storm Runner (0.91 energy) versus Requiem for Glass (0.22 energy). The only real difference between the profiles is the genre and mood words. That shows those labels, not energy, control the top spot. This is the clearest sign of the system's main weakness.

- Metal Fan Wants Calm vs. Deep Intense Rock: Both like metal, but the calm metal fan gets chill ambient and lofi songs, while the rock fan gets the aggressive metal song Ashfall near the top. This makes sense, because the calm metal fan's mood (chill) and energy (0.2) both point toward quiet music, and together they outvote the single genre match. With the original weights Ashfall still sneaked in at #4 for the calm listener. After I made genre count less, it dropped out, which is the more sensible result.

- **Empty Profile vs. everyone else:** With no preferences, every song scores exactly 0. The "top 5" is just the songs closest to medium energy, chosen by the tie-breaking rule. Compared with every other profile, this one shows that the order of the list only means something when the user has told the system something.

---

## 8. Future Work  

In the future, I would improve my recommender by using a larger dataset with more songs from each genre. I would also add partial matching for similar genres and moods instead of requiring exact matches. Another improvement would be allowing users to adjust how important each feature is to them, since some people might care more about energy or mood than genre. 

---

## 9. Personal Reflection  

This project has allowed me ot understand how recommendation systems, such as the one I use on Spotify, turn user prefrences and song data into scores and rankings. I learned that the weights assigned to different features can significantly affect which songs get recommended. One thing that surprised me was how a song could rank first even when it didn't match an important part of the user's preferences. It showed me that recommendations aren't always accurate just because they have a high score. I also realized how easily bias can appear in a recommendation system, especially when the dataset is small or certain features have too much influence. 
