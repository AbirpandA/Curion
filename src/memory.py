import json
from pathlib import Path

class UserMemory:
    def __init__(self, user_id="default"):
        self.user_dir = Path(f'user_profiles/{user_id}')
        self.user_dir.mkdir(exist_ok=True)
        self.profile = self.load_profile()

    def load_profile(self):
        profile_path = self.user_dir / "profile.json"
        if profile_path.exists():
            with open(profile_path) as f:
                return json.load(f)
        return {
            "learning_style": "socratic",
            "interests": {"philosophy": 0.8},
            "conversation_history": []
        }

    def update_memory(self, question, response):
        self.profile['conversation_history'].append({
            "q": question,
            "a": response
        })
        if 'quantum' in question.lower():
            self.profile["interests"]["physics"] = self.profile["interests"].get("physics", 0) + 0.1
        with open(self.user_dir / "profile.json", "w") as f:
            json.dump(self.profile, f)
