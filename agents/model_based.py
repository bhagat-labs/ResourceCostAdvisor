class ModelBasedReflexAgent:
    def __init__(self):
        self.state_history = []

    def evaluate(self, metrics, slos):
        self.state_history.append(metrics["cpu_utilization"])
        if len(self.state_history) > 3:
            self.state_history.pop(0)
            
        trend = "increasing" if len(self.state_history) == 3 and self.state_history[-1] > self.state_history[0] else "stable"
        
        if metrics["cpu_utilization"] > 75.0 and trend == "increasing":
            return {
                "recommendation": "Proactive Horizontal Scale-Out",
                "reasoning": f"Model state detects high CPU ({metrics['cpu_utilization']}%) with an upward trend. Preempting breach."
            }
        return {
            "recommendation": "No Action Required",
            "reasoning": f"Internal state trend is {trend}; no imminent risk detected."
        }