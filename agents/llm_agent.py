import ollama
import json
from tools.cloud_tools import get_resource_metrics, get_cost_estimate, get_service_level_targets, get_scaling_policy

class LLMToolAgent:
    def __init__(self, model_name="qwen2.5"):
        self.model_name = model_name

    def run_analysis(self, scenario_id: str):
        prompt = f"""
        Analyze cloud workload scenario '{scenario_id}'. 
        You MUST call at least two relevant tools (such as get_resource_metrics, get_cost_estimate, get_service_level_targets, or get_scaling_policy) to fetch live data.
        Ground your recommendation strictly in the tool outputs, balancing response time, availability, and cost.
        """
        
        available_tools = {
            "get_resource_metrics": get_resource_metrics,
            "get_cost_estimate": get_cost_estimate,
            "get_service_level_targets": get_service_level_targets,
            "get_scaling_policy": get_scaling_policy
        }

        messages = [{'role': 'user', 'content': prompt}]
        
        # First call with tool definitions
        response = ollama.chat(
            model=self.model_name,
            messages=messages,
            tools=[get_resource_metrics, get_cost_estimate, get_service_level_targets, get_scaling_policy]
        )

        tool_outputs = []
        if response.get('message', {}).get('tool_calls'):
            for tool in response['message']['tool_calls']:
                func_name = tool['function']['name']
                func_args = tool['function']['arguments']
                if func_name in available_tools:
                    result = available_tools[func_name](**func_args)
                    tool_outputs.append(f"Tool {func_name}({func_args}) returned: {result}")
            
            # Follow-up chat incorporating tool evidence
            messages.append(response['message'])
            messages.append({'role': 'tool', 'content': "\n".join(tool_outputs)})
            
            final_response = ollama.chat(model=self.model_name, messages=messages)
            return {
                "decision": final_response['message']['content'],
                "evidence_used": tool_outputs
            }
        
        return {
            "decision": response['message']['content'],
            "evidence_used": ["No tools were called directly by the model."]
        }