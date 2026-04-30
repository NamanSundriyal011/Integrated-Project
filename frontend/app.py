import streamlit as st
import requests
import re

st.set_page_config(page_title="Construction AI", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title("🏗 Construction AI")
st.sidebar.markdown("Plan Smarter. Build Better.")
st.sidebar.markdown("---")

# ---------- HEADER ----------
st.title("Build Your Construction Plan")
st.caption("AI-powered planning & reporting")

goal = st.text_input("Enter Project Goal")

# ---------- CLEAN FUNCTION ----------
def clean_text(text):
    text = re.sub(r"\*\*", "", text)
    text = re.sub(r"\*", "", text)
    text = re.sub(r"- ", "", text)
    return text.strip()

# ---------- SAFE METRICS ----------
def extract_metrics(metrics_text):
    result = {
        "duration": "N/A",
        "budget": "N/A",
        "team": "N/A"
    }

    for line in metrics_text.split("\n"):
        parts = line.split(":", 1)

        if len(parts) < 2:
            continue

        key = parts[0].lower()
        value = parts[1].strip()

        if "duration" in key:
            result["duration"] = value
        elif "budget" in key:
            result["budget"] = value
        elif "team" in key:
            result["team"] = value

    return result   # ✅ returns dictionary (NO unpack issue)

# ---------- BUTTON ----------
if st.button("🚀 Generate Plan"):

    try:
        res = requests.post(
            "http://127.0.0.1:8000/generate",
            json={"goal": goal}
        ).json()

        if "error" in res:
            st.error(res["error"])
        else:

            plan_text = clean_text(res["plan"])
            report_text = clean_text(res["report"])
            metrics_text = res.get("metrics", "")

            # ✅ NO unpacking now
            metrics = extract_metrics(metrics_text)

            duration = metrics["duration"]
            budget = metrics["budget"]
            team = metrics["team"]

            # ---------- STEP COUNT ----------
            steps_list = [
                s for s in plan_text.split("\n")
                if s.strip() and len(s.strip()) < 150
            ]
            total_steps = len(steps_list)

            col1, col2 = st.columns(2)

            # ---------- TASK PLAN ----------
            with col1:
                st.subheader("📋 TASK PLAN")

                st.download_button(
                    "⬇ Download Task Plan",
                    data=plan_text,
                    file_name="task_plan.txt"
                )

                phases = plan_text.split("Phase")
                icons = ["📋", "🏗", "⚙️", "🚀"]

                for i, phase in enumerate(phases):
                    if phase.strip():

                        lines = [
                            clean_text(l)
                            for l in phase.strip().split("\n")
                            if l.strip()
                        ]

                        title = lines[0]

                        st.markdown(f"### {icons[i % len(icons)]} Phase {title}")

                        for step in lines[1:]:
                            st.markdown(f"""
                            <div style="
                                background:#0f172a;
                                padding:12px;
                                margin:8px 0;
                                border-radius:10px;
                                border-left:4px solid #6366f1;
                            ">
                                {step}
                            </div>
                            """, unsafe_allow_html=True)

            # ---------- REPORT ----------
            with col2:
                st.subheader("📄 SITE REPORT")

                st.download_button(
                    "⬇ Download Report",
                    data=report_text,
                    file_name="report.txt"
                )

                sections = report_text.split("\n\n")

                for sec in sections:
                    if sec.strip():
                        st.markdown(f"""
                        <div style="
                            background:#0f172a;
                            padding:16px;
                            margin-bottom:10px;
                            border-radius:12px;
                            border:1px solid rgba(255,255,255,0.08);
                        ">
                            {sec}
                        </div>
                        """, unsafe_allow_html=True)

            # ---------- CARDS ----------
            st.markdown("###")

            c1, c2, c3, c4 = st.columns(4)

            def card(title, value, color):
                return f"""
                <div style="
                    background: rgba(30,41,59,0.8);
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                    border:1px solid rgba(255,255,255,0.1);
                    box-shadow: 0 0 20px {color}33;
                ">
                    <div style="font-size:14px; color:#94a3b8;">{title}</div>
                    <div style="font-size:22px; font-weight:600; color:white;">{value}</div>
                </div>
                """

            with c1:
                st.markdown(card("Total Steps", total_steps, "#3b82f6"), unsafe_allow_html=True)

            with c2:
                st.markdown(card("Est. Duration", duration, "#22c55e"), unsafe_allow_html=True)

            with c3:
                st.markdown(card("Est. Budget", budget, "#f97316"), unsafe_allow_html=True)

            with c4:
                st.markdown(card("Team Members", team, "#a855f7"), unsafe_allow_html=True)

    except Exception as e:
        st.error(str(e))