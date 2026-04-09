import os
import sys
import json
from openai import OpenAI

# Insert root to sys path so we can import our backend natively
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backend.env import SatelliteSchedulingEnv
from backend.graders import grade

SYSTEM_PROMPT = """You are an expert satellite fleet coordinator AI.
You manage a fleet of satellites to complete tasks under resource constraints.

You receive a JSON observation each turn and must respond with ONE action in JSON format.

Available actions:
- {"type": "assign_task", "satellite_id": "SAT-001", "task_id": "TASK-001"}  
  → Assign a task to an executor satellite. Only use active satellites with sufficient battery.
- {"type": "change_role", "satellite_id": "SAT-001"}
  → Switch satellite between planner and executor roles.
- {"type": "skip"}
  → Skip this step (small penalty).

Rules:
1. Only EXECUTOR satellites can be assigned tasks.
2. Satellite battery must be >= task battery_cost.
3. Satellite storage_used + task storage_cost must be <= 100.
4. Prioritize CRITICAL tasks, especially disaster_related ones.
5. Monitor battery — satellites with battery < 10 should not be assigned tasks.

Respond with ONLY valid JSON. No explanation, no markdown. Just the action JSON.
"""

def llm_agent_action(client: OpenAI, model: str, observation: dict) -> dict:
    obs_summary = {
        "step": observation["step"],
        "max_steps": observation["max_steps"],
        "satellites": [
            {"id": s["id"], "battery": round(s["battery"], 1), "role": s["role"], "active": s["active"]}
            for s in observation["satellites"] if s["active"]
        ],
        "pending_tasks": [
            {"id": t["id"], "priority": t["priority"], "battery_cost": t["battery_cost"]}
            for t in observation["tasks"] if not t["completed"] and not t["assigned_to"]
        ][:10]
    }
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Current state:\n{json.dumps(obs_summary)}\n\nWhat action should the agent take?"},
            ],
            temperature=0.1,
            max_tokens=150,
        )
        action_text = response.choices[0].message.content.strip()
        if action_text.startswith("```"):
            action_text = action_text.split("```")[1]
            if action_text.startswith("json"):
                action_text = action_text[4:]
        return json.loads(action_text)
    except Exception:
        return {"type": "skip"}

def main():
    # 1. Strictly extract the injected OpenEnv credentials
    try:
        API_BASE_URL = os.environ["API_BASE_URL"]
        API_KEY = os.environ["API_KEY"]
    except KeyError as e:
        print(f"ERROR: Missing injected OpenEnv variable: {e}", file=sys.stderr)
        sys.exit(1)
        
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
    
    # 2. Instantiate OpenAI client with proxy
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    # 3. Process all 3 difficulties to get full Phase 2 coverage
    for difficulty in ["easy", "medium", "hard"]:
        env = SatelliteSchedulingEnv(difficulty=difficulty, seed=42)
        obs = env.reset()
        done = False
        steps = 0
        total_reward = 0.0

        print(f"[START] task={difficulty}", flush=True)

        while not done:
            action = llm_agent_action(client, MODEL_NAME, obs)
            obs, reward, done, _ = env.step(action)
            total_reward += reward
            steps += 1
            print(f"[STEP] step={steps} reward={reward}", flush=True)
            
            # Limit the number of API calls during Hackathon proxy phase to avoid rate limits
            if steps >= 10 and not done:
                print("Early stopping due to proxy limits.", file=sys.stderr)
                break
                
        final_state = env.get_state()
        result = grade(difficulty, final_state)
        # OpenEnv strict formatting requires actual score calculation
        print(f"[END] task={difficulty} score={result['score']} steps={steps}", flush=True)

if __name__ == "__main__":
    main()
