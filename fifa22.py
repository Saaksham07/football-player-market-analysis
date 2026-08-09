import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


df = pd.read_csv(r"C:\Users\Saksham\Desktop\players_22.csv")

print(df.head())
print(df.shape)
print(df.info())

# Sirf relevant columns rakhte hain
cols = ['short_name', 'long_name', 'player_positions', 'overall', 'potential',
        'value_eur', 'wage_eur', 'age', 'height_cm', 'weight_kg', 'club_name',
        'league_name', 'nationality_name', 'preferred_foot', 'weak_foot',
        'skill_moves', 'pace', 'shooting', 'passing', 'dribbling', 
        'defending', 'physic', 'international_reputation', 'release_clause_eur']

df = df[cols]

# Missing values check
print(df.isnull().sum())

# Free agents drop karo (club nahi hai toh analysis mein kaam nahi aayenge)
df = df.dropna(subset=['club_name', 'value_eur', 'wage_eur'])

# Pace etc missing = goalkeeper hai, 0 se fill karo
df[['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']] = df[['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic']].fillna(0)

# Release clause missing = 0 se fill karo
df['release_clause_eur'] = df['release_clause_eur'].fillna(0)

print("Clean data rows:", len(df))
print(df.isnull().sum())

# Q1: Top 10 highest valued players
top_10_value = df[['short_name', 'club_name', 'overall', 'value_eur']].sort_values('value_eur', ascending=False).head(10)
print(top_10_value)

# Q2: Konsi league mein average player value sabse zyada hai?
top_leagues = df.groupby("league_name")["value_eur"].mean().sort_values(ascending=False).head(10)
print(top_leagues.apply(lambda x: f"€{x:,.0f}"))


# Pehla position lo sirf
df['main_position'] = df['player_positions'].str.split(',').str[0].str.strip()

# Q3: Konsa position sabse zyada earn karta hai?
top_positions = df.groupby("main_position")["wage_eur"].mean().sort_values(ascending=False).head(10)
print(top_positions.apply(lambda x: f"€{x:,.0f}"))

# Q4: Young undervalued players (age < 23, potential >= 85)
undervalued = df[(df["age"] < 23) & (df["potential"] >= 85)]
result = undervalued[['short_name', 'age', 'overall', 'potential', 'value_eur']].sort_values("value_eur").head(10).copy()
result['value_eur'] = result['value_eur'].apply(lambda x: f"€{x:,.0f}")
print(result)

# Q5: Konsi nationality ke players ki average value sabse zyada hai?
top_nations = df.groupby("nationality_name")["value_eur"].mean().sort_values(ascending=False).head(10)
print(top_nations.apply(lambda x: f"€{x:,.0f}"))

# Chart 1: Top 10 players by value
plt.figure(figsize=(10,6))
sns.barplot(x="value_eur", y="short_name", data=top_10_value)
plt.title("Top 10 Players by Market Value")
plt.xlabel("Market Value (€)")
plt.ylabel("Player")
plt.tight_layout()
plt.show()

# Chart 2: League wise average value
top_leagues_df = df.groupby("league_name")["value_eur"].mean().sort_values(ascending=False).head(10).reset_index()

plt.figure(figsize=(10,6))
sns.barplot(x="value_eur", y="league_name", data=top_leagues_df)
plt.title("Top 10 Leagues by Average Player Value")
plt.xlabel("Average Market Value (€)")
plt.ylabel("League")
plt.tight_layout()
plt.show()

# Chart 3: Age vs Market Value
plt.figure(figsize=(10,6))
sns.scatterplot(data=df, x="age", y="value_eur", alpha=0.5)
plt.title("Age vs Market Value")
plt.xlabel("Age")
plt.ylabel("Market Value (€)")
plt.tight_layout()
plt.show()

df = df.drop_duplicates()
print("After duplicates removed:", len(df))

# Age vs Value correlation
correlation = df["age"].corr(df["value_eur"])
print(f"Correlation between age and market value: {correlation:.2f}")

if correlation < -0.3:
    print("Older players tend to have lower market value.")
elif correlation > 0.3:
    print("Older players tend to have higher market value.")
else:
    print("Weak relationship between age and market value.")


 # Insight Q1: Mbappe is the highest valued player at €194M. Despite Lewandowski having the highest overall rating (92), his age (33) reduces his market value compared to younger players like Mbappe (23).

# Insight Q2: English Premier League has the highest average player value at €14M, followed by La Liga (€11.5M) and Serie A (€9.4M). This reflects EPL's massive TV revenue and commercial deals.

# Insight Q3: Centre Forwards (CF) earn the most at €21,611/week. Goals directly impact match results, making strikers the most valuable and highest paid position in football.

# Insight Q4: Players like R. Lavia (17, potential 85) and Gavi (16, potential 85) are highly undervalued with values under €2.5M despite exceptional potential. These represent high-value investment opportunities.

# Insight Q5: Egypt tops nationality rankings due to Mohamed Salah's extremely high value skewing the average. Portugal and Spain reflect consistent production of top European talent.

# Insight Q6: Correlation between age and market value is only 0.04 — almost no direct relationship. Age alone does not determine value; overall rating, potential, league, and position are stronger factors.