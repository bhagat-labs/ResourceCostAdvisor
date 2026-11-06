class SimpleReflexAgent:
    def evaluate(self, metrics, slos):
        if metrics["cpu_utilization"] > 80.0 or metrics["response_time_ms"] > slos["max_response_time_ms"]:
            return {
                "recommendation": "Scale Up / Out Immediately",
                "reasoning": "Condition-action rule triggered: CPU or response time exceeds critical threshold."
            }
        elif metrics["cpu_utilization"] < 20.0:
            return {
                "recommendation": "Scale Down",
                "reasoning": "Condition-action rule triggered: CPU utilization is below off-peak minimum threshold."
            }
        return {
            "recommendation": "Maintain Current Configuration",
            "reasoning": "All metrics are within acceptable baseline conditions."
        }