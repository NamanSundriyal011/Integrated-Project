from fastapi import FastAPI
from pydantic import BaseModel

from agent import generate_plan
from generator import generate_report, generate_metrics

app = FastAPI()

class Request(BaseModel):
    goal: str


@app.get("/")
def home():
    return {"message": "Backend is working 🚀"}


@app.post("/generate")
def generate(req: Request):

    try:
        plan = generate_plan(req.goal)
        report = generate_report(req.goal)
        metrics = generate_metrics(req.goal)

        return {
            "goal": req.goal,
            "plan": plan,
            "report": report,
            "metrics": metrics
        }

    except Exception as e:
        return {
            "error": str(e)
        }


print("🔥 Backend starting...")