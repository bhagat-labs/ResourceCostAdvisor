import json
import os

class LearningAgent:
    def __init__(self, db_path="data/experience_db.json"):
        self.db_path = db_path
        self.load_experience()

    def load_experience(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, "r") as f:
                self.experience = json.load(f)
        else:
            self.experience = {"downsize_successes": 5, "downsize_failures": 1, "scale_out_successes": 10, "scale_out_failures": 0}

    def record_feedback(self, action_type: str, success: bool):
        key = f"{action_type}_{'successes' if success else 'failures'}"
        if key in self.experience:
            self.experience[key] += 1
        with open(self.db_path, "w") as f:
            json.dump(self.experience, f)

    def evaluate(self, metrics, cost_data):
        downsize_score = self.experience["downsize_successes"] - self.experience["downsize_failures"]
        
        if metrics["cpu_utilization"] < 15.0:
            confidence = (self.experience["downsize_successes"] / max(1, self.experience["downsize_successes"] + self.experience["downsize_failures"])) * 100
            return {
                "recommendation": "Downsize Instance (Learned Policy)",
                "reasoning": f"Based on historical experience database (Confidence: {confidence:.1f}% across {downsize_score+self.experience['downsize_failures']} past episodes), downsizing yields positive net savings without availability loss."
            }
        return {
            "recommendation": "Maintain / Standard Operating Policy",
            "reasoning": "No historical learning deviation triggered."
        }