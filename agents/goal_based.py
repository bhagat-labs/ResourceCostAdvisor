class GoalBasedAgent:
    def evaluate(self, metrics, slos):
        goal_response_time = slos["max_response_time_ms"]
        goal_availability = slos["min_availability"]
        
        rt_met = metrics["response_time_ms"] <= goal_response_time
        av_met = metrics["availability"] >= goal_availability
        
        if not rt_met or not av_met:
            return {
                "recommendation": "Add Instance to ASG",
                "reasoning": f"Current state fails goals: Response Time {metrics['response_time_ms']}ms (Goal <= {goal_response_time}ms)."
            }
        return {
            "recommendation": "Goals Successfully Met",
            "reasoning": "All performance goals and availability targets are fully satisfied."
        }