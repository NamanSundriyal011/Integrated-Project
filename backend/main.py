from fastapi import FastAPI
from pydantic import BaseModel

from agent import generate_plan
from generator import generate_report, generate_metrics

app = FastAPI()

# =========================
# REQUEST MODEL
# =========================
class ProjectRequest(BaseModel):
    goal: str

# =========================
# GENERATE API
# =========================
@app.post("/generate")
def generate(data: ProjectRequest):

    plan = generate_plan(data.goal)

    report = generate_report(data.goal)

    metrics_text = generate_metrics(data.goal)

    # =========================
    # CONVERT METRICS STRING TO DICT
    # =========================
    metrics = {
        "duration": "N/A",
        "budget": "N/A",
        "team": "N/A",
        "steps": 0
    }

    lines = metrics_text.split("\n")

    for line in lines:

        line = line.strip()

        if "Duration:" in line:
            metrics["duration"] = line.replace("Duration:", "").strip()

        elif "Budget:" in line:
            metrics["budget"] = line.replace("Budget:", "").strip()

        elif "Team:" in line:
            metrics["team"] = line.replace("Team:", "").strip()

    # count total steps
    metrics["steps"] = plan.count("-")

    return {
        "plan": plan,
        "report": report,
        "metrics": metrics
    }