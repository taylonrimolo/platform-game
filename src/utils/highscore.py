import json
import os


class HighScoreManager:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.high_score = self._load()

    def _load(self) -> int:
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
            except:
                return 0
        return 0

    def update(self, score: int):
        if score > self.high_score:
            self.high_score = score
            data = {'high_score': self.high_score}
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'w') as f:
                json.dump(data, f)