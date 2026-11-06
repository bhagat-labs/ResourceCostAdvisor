"""
test_scenarios.py
Defines the test scenarios (Normal, Critical/Failure, Edge/Ambiguous Case) 
for comparing cloud workload advisor agents.
"""

TEST_SCENARIOS = {
    "normal": {
        "scenario_id": "normal",
        "description": "Stable traffic with optimal resource usage and balanced performance.",
        "metrics": {
            "cpu_utilization": 45.0,
            "memory_utilization": 50.0,
            "response_time_ms": 180.0,
            "availability": 99.99
        },
        "cost": {
            "current_hourly_cost": 0.10,
            "instance_type": "c6i.large"
        },
        "slos": {
            "max_response_time_ms": 300.0,
            "min_availability": 99.9
        },
        "scaling_policy": {
            "min_instances": 2,
            "max_instances": 4,
            "target_cpu": 60.0
        }
    },
    "critical": {
        "scenario_id": "critical",
        "description": "CPU utilization is consistently high and response time exceeds target SLOs.",
        "metrics": {
            "cpu_utilization": 92.5,
            "memory_utilization": 85.0,
            "response_time_ms": 850.0,
            "availability": 98.50
        },
        "cost": {
            "current_hourly_cost": 0.10,
            "instance_type": "c6i.large"
        },
        "slos": {
            "max_response_time_ms": 300.0,
            "min_availability": 99.9
        },
        "scaling_policy": {
            "min_instances": 1,
            "max_instances": 2,
            "target_cpu": 80.0
        }
    },
    "edge_case": {
        "scenario_id": "edge_case",
        "description": "CPU and memory utilization are low, but the provisioned instance is expensive.",
        "metrics": {
            "cpu_utilization": 10.0,
            "memory_utilization": 18.0,
            "response_time_ms": 110.0,
            "availability": 99.99
        },
        "cost": {
            "current_hourly_cost": 1.70,
            "instance_type": "c6i.2xlarge"
        },
        "slos": {
            "max_response_time_ms": 300.0,
            "min_availability": 99.9
        },
        "scaling_policy": {
            "min_instances": 2,
            "max_instances": 10,
            "target_cpu": 70.0
        }
    }
}

def get_scenario(scenario_id: str) -> dict:
    """Retrieves a specific test scenario by its identifier."""
    return TEST_SCENARIOS.get(scenario_id, TEST_SCENARIOS["normal"])

def list_scenario_ids() -> list:
    """Returns all available test scenario IDs."""
    return list(TEST_SCENARIOS.keys())