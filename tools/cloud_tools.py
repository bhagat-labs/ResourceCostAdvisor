import json

# Simulated Cloud Database / State
SCENARIOS = {
    "normal": {
        "scenario_id": "normal",
        "description": "Stable traffic with optimal resource usage.",
        "metrics": {"cpu_utilization": 45.0, "memory_utilization": 50.0, "response_time_ms": 180.0, "availability": 99.99},
        "cost": {"current_hourly_cost": 0.10, "instance_type": "c6i.large"},
        "slos": {"max_response_time_ms": 300.0, "min_availability": 99.9},
        "scaling_policy": {"min_instances": 2, "max_instances": 4, "target_cpu": 60.0}
    },
    "critical": {
        "scenario_id": "critical",
        "description": "High CPU utilization and response time breaches target.",
        "metrics": {"cpu_utilization": 92.5, "memory_utilization": 85.0, "response_time_ms": 850.0, "availability": 98.50},
        "cost": {"current_hourly_cost": 0.10, "instance_type": "c6i.large"},
        "slos": {"max_response_time_ms": 300.0, "min_availability": 99.9},
        "scaling_policy": {"min_instances": 1, "max_instances": 2, "target_cpu": 80.0}
    },
    "edge_case": {
        "scenario_id": "edge_case",
        "description": "Low utilization (CPU/Memory low) but instance type is expensive.",
        "metrics": {"cpu_utilization": 10.0, "memory_utilization": 18.0, "response_time_ms": 110.0, "availability": 99.99},
        "cost": {"current_hourly_cost": 1.70, "instance_type": "c6i.2xlarge"},
        "slos": {"max_response_time_ms": 300.0, "min_availability": 99.9},
        "scaling_policy": {"min_instances": 2, "max_instances": 10, "target_cpu": 70.0}
    }
}

def get_resource_metrics(scenario_id: str) -> str:
    """Returns CPU, memory, response time, and availability metrics for the given scenario."""
    data = SCENARIOS.get(scenario_id, SCENARIOS["normal"])
    return json.dumps(data["metrics"])

def get_cost_estimate(instance_type: str) -> str:
    """Returns the hourly and monthly cost estimate for a specific cloud instance type."""
    costs = {
        "c6i.large": {"hourly": 0.10, "monthly": 73.00},
        "c6i.xlarge": {"hourly": 0.20, "monthly": 146.00},
        "c6i.2xlarge": {"hourly": 1.70, "monthly": 1241.00},
        "t4g.small": {"hourly": 0.016, "monthly": 11.68}
    }
    return json.dumps(costs.get(instance_type, {"hourly": 0.50, "monthly": 365.00}))

def get_service_level_targets(scenario_id: str) -> str:
    """Retrieves defined SLAs/SLOs for response time and availability."""
    data = SCENARIOS.get(scenario_id, SCENARIOS["normal"])
    return json.dumps(data["slos"])

def get_scaling_policy(scenario_id: str) -> str:
    """Evaluates existing scaling rules and thresholds."""
    data = SCENARIOS.get(scenario_id, SCENARIOS["normal"])
    return json.dumps(data["scaling_policy"])