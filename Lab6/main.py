from nltk.sentiment import SentimentIntensityAnalyzer

def check_mood(text):
    analyzer = SentimentIntensityAnalyzer()
    mood_score = analyzer.polarity_scores(text)
    
    compound_score = mood_score['compound']
    
    if compound_score >= 0.05:
        mood = "OMG, YOU PASSED, but not so fast, you got one more challenge ahead"
    elif compound_score <= -0.05:
        mood = "BOOOOOOOO, SEE YOU NEXT YEAR LOSER"
    else:
        mood = "I guess.... everything is alright??!!"
    
    return mood, mood_score

def main():
    text = input("Give me my verdict... ")
    mood, score = check_mood(text)
    
    print(f"Your verdict: {mood}")
    print(f"Mood Score: {score}")

if __name__ == "__main__":
    main()
