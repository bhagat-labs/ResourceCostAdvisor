import streamlit as st
import json
from tools.cloud_tools import SCENARIOS, get_cost_estimate
from agents.simple_reflex import SimpleReflexAgent
from agents.model_based import ModelBasedReflexAgent
from agents.goal_based import GoalBasedAgent
from agents.utility_based import UtilityBasedAgent
from agents.learning_agent import LearningAgent
from agents.llm_agent import LLMToolAgent

st.set_page_config(page_title="Cloud Workload Advisor AI Dashboard", layout="wide")

st.title("☁️ Multi-Agent Cloud Workload Resource Advisor")
st.markdown("Comparing Classical AI Agents and an Ollama LLM Agent for Cloud Cost & Performance Optimization.")

# Sidebar Scenario Selection
scenario_choice = st.sidebar.selectbox(
    "Select Test Scenario",
    options=["normal", "critical", "edge_case"],
    format_func=lambda x: f"Scenario: {x.upper()} - {SCENARIOS[x]['description']}"
)

current_scenario = SCENARIOS[scenario_choice]

st.subheader(f"📋 Scenario Profile: `{scenario_choice.upper()}`")
st.info(current_scenario["description"])

col1, col2, col3, col4 = st.columns(4)
col1.metric("CPU Utilization", f"{current_scenario['metrics']['cpu_utilization']}%")
col2.metric("Response Time", f"{current_scenario['metrics']['response_time_ms']} ms")
col3.metric("Availability", f"{current_scenario['metrics']['availability']}%")
col4.metric("Current Cost", f"${current_scenario['cost']['current_hourly_cost']}/hr")

st.markdown("---")
st.subheader("🤖 Agent Decision Comparison Matrix")

# Initialize Agents
sr_agent = SimpleReflexAgent()
mb_agent = ModelBasedReflexAgent()
gb_agent = GoalBasedAgent()
ub_agent = UtilityBasedAgent()
la_agent = LearningAgent()
llm_agent = LLMToolAgent(model_name="qwen2.5")

# Run Evaluations
sr_res = sr_agent.evaluate(current_scenario["metrics"], current_scenario["slos"])
mb_res = mb_agent.evaluate(current_scenario["metrics"], current_scenario["slos"])
gb_res = gb_agent.evaluate(current_scenario["metrics"], current_scenario["slos"])
ub_res = ub_agent.evaluate(current_scenario["metrics"], current_scenario["cost"], current_scenario["slos"])
la_res = la_agent.evaluate(current_scenario["metrics"], current_scenario["cost"])

# Display comparison table / cards
agent_data = [
    {"Agent": "Simple Reflex Agent", "Decision": sr_res["recommendation"], "Reasoning": sr_res["reasoning"]},
    {"Agent": "Model-Based Reflex Agent", "Decision": mb_res["recommendation"], "Reasoning": mb_res["reasoning"]},
    {"Agent": "Goal-Based Agent", "Decision": gb_res["recommendation"], "Reasoning": gb_res["reasoning"]},
    {"Agent": "Utility-Based Agent", "Decision": ub_res["recommendation"], "Reasoning": ub_res["reasoning"]},
    {"Agent": "Learning Agent", "Decision": la_res["recommendation"], "Reasoning": la_res["reasoning"]},
]

st.table(agent_data)

st.markdown("---")
st.subheader("🧠 Local LLM Agent Analysis (Ollama + Tool Calling)")

if st.button("Run LLM Tool-Calling Advisor"):
    with st.spinner("Calling local Ollama model and executing cloud metric tools..."):
        try:
            llm_output = llm_agent.run_analysis(scenario_choice)
            st.success("LLM Analysis Complete!")
            st.markdown("**LLM Recommendation & Reasoning:**")
            st.write(llm_output["decision"])
            with st.expander("View Tool Evidence & Grounding Logs"):
                for log in llm_output["evidence_used"]:
                    st.code(log)
        except Exception as e:
            st.error(f"Error connecting to Ollama: {e}. Ensure Ollama is running locally (`ollama serve`).")