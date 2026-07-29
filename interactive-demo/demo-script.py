import os
import json
import random
import requests
from datetime import datetime

API_KEY = os.environ.get("DEEPSEEK_API_KEY")
if not API_KEY:
    print("No API key found")
    exit(1)

# 模拟角色和任务
demos = [
    {"role": "Market Analyst", "task": "Analyze the potential of exporting Brazilian sugar to the Middle East."},
    {"role": "Legal Advisor", "task": "Draft a compliance checklist for cross-border e-commerce in Southeast Asia."},
    {"role": "Content Creator", "task": "Write a social media post introducing AI-driven trade solutions."},
    {"role": "Logistics Coordinator", "task": "Outline a shipping route from Shanghai to Dubai for consumer electronics."},
    {"role": "Financial Analyst", "task": "Create a cost-benefit analysis template for importing coffee from Ethiopia."}
]

selected = random.choice(demos)

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": f"You are the {selected['role']} at Global AI Media Group. Respond professionally."},
        {"role": "user", "content": selected['task']}
    ],
    "temperature": 0.7,
    "max_tokens": 300
}

try:
    resp = requests.post("https://api.deepseek.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
    output = resp.json()["choices"][0]["message"]["content"]
except Exception as e:
    output = f"Error: {e}"

filename = f"interactive-demo/daily-output/{datetime.now().strftime('%Y-%m-%d')}.md"
content = f"## {selected['role']}\n**Task:** {selected['task']}\n\n{output}"
with open(filename, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Demo saved to {filename}")
