import json, os

FILE = "CardGames\highscores.json"

def load_scores():
    if not os.path.exists(FILE):
        with open(FILE, 'w') as f:
            json.dump({}, f)
    with open(FILE, 'r') as f:
        return json.load(f)
    
def save_scores(scores):
    with open(FILE, 'w') as f:
        json.dump(scores, f, indent=2)

def get_high_score(game_name):
    scores = load_scores()
    if game_name not in scores:
        return 0, None, None
    data = scores[game_name]
    return data['score'], data['date'], data['time']

def update_high_score(game_name, score):
    scores = load_scores()
    current_high_score, _, _ = get_high_score(game_name)
    if score > current_high_score:
        from datetime import datetime
        now = datetime.now()
        scores[game_name] = {
            'score': score,
            'date': now.strftime("%m-%d-%Y"),
            'time': now.strftime("%H:%M")
        }
        save_scores(scores)
        return True
    return False