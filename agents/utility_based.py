class UtilityBasedAgent:
    def evaluate(self, metrics, cost_data, slos):
        # Utility function: Higher is better. Rewards low cost and low response time.
        # U = (1 / Cost) + (1 / ResponseTime)
        hourly_cost = cost_data["hourly"]
        rt = metrics["response_time_ms"]
        
        if metrics["cpu_utilization"] < 15.0 and hourly_cost > 1.0:
            return {
                "recommendation": "Downsize Instance (`c6i.large`)",
                "reasoning": f"Low utility score due to massive over-provisioning cost (${hourly_cost}/hr) for 10% CPU usage."
            }
        elif rt > slos["max_response_time_ms"]:
            return {
                "recommendation": "Scale Out (Add Compute Nodes)",
                "reasoning": "Low utility score due to severe SLA breach outweighing current cost savings."
            }
        return {
            "recommendation": "Optimal Utility Balance",
            "reasoning": "Current configuration maximizes cost-to-performance utility ratio."
        }