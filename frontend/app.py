import streamlit as st
import requests

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Construction AI",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

body {
    background-color: #050816;
}

.main {
    background-color: #050816;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #1e1f2b;
    border-right: 1px solid #2f3242;
}

.sidebar-title {
    font-size: 32px;
    font-weight: bold;
    color: white;
}

.card {
    background: #0f172a;
    padding: 18px;
    border-radius: 14px;
    margin-bottom: 15px;
    border: 1px solid #1f2937;
}

.metric-card {
    background: #111827;
    padding: 20px;
    border-radius: 16px;
    text-align: center;
    border: 1px solid #374151;
}

.phase-title {
    font-size: 26px;
    font-weight: bold;
    margin-top: 25px;
    margin-bottom: 10px;
}

.step-box {
    background: #081226;
    padding: 14px;
    margin-bottom: 10px;
    border-radius: 12px;
    border-left: 4px solid #6366f1;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown(
        "<div class='sidebar-title'>🏗️ Construction AI</div>",
        unsafe_allow_html=True
    )

    st.write("Plan Smarter. Build Better.")
    st.divider()

    st.markdown("### Dashboard")
    st.markdown("### Projects")
    st.markdown("### Reports")

# =========================
# MAIN TITLE
# =========================
st.title("Build Your Construction Plan")
st.caption("AI-powered planning & reporting")

# =========================
# INPUT
# =========================
goal = st.text_input(
    "Enter Project Goal",
    placeholder="Build a Hospital with two floor parking and Garden"
)

# =========================
# DOCKER BACKEND URL
# =========================
API_URL = "http://backend:8000/generate"

# =========================
# GENERATE BUTTON
# =========================
if st.button("🚀 Generate Plan"):

    if not goal:
        st.warning("Please enter a project goal")

    else:
        try:
            response = requests.post(
                API_URL,
                json={"goal": goal}
            )

            data = response.json()

            plan = data.get("plan", "")
            report = data.get("report", "")
            metrics = data.get("metrics", {})

            # =========================
            # LAYOUT COLUMNS
            # =========================
            col1, col2 = st.columns([1.3, 1])

            # =========================
            # TASK PLAN
            # =========================
            with col1:

                st.markdown("## 📋 TASK PLAN")

                phases = plan.split("Phase")

                icons = ["📋", "🏗️", "⚙️", "🚀"]

                for i, phase in enumerate(phases):

                    phase = phase.strip()

                    if not phase:
                        continue

                    lines = phase.split("\n")

                    title = lines[0]

                    st.markdown(
                        f"""
                        <div class='phase-title'>
                            {icons[i % len(icons)]} Phase {title}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    for step in lines[1:]:

                        step = (
                            step
                            .replace("**", "")
                            .replace("*", "")
                        )

                        if step.strip():

                            st.markdown(
                                f"""
                                <div class='step-box'>
                                    {step}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                # DOWNLOAD BUTTON
                st.download_button(
                    "⬇ Download Task Plan",
                    plan,
                    file_name="task_plan.txt"
                )

            # =========================
            # SITE REPORT
            # =========================
            with col2:

                st.markdown("## 📄 SITE REPORT")

                clean_report = (
                    report
                    .replace("**", "")
                    .replace("*", "")
                )

                st.markdown(
                    f"""
                    <div class='card'>
                        <pre style='white-space: pre-wrap; color:white;'>
{clean_report}
                        </pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # DOWNLOAD REPORT
                st.download_button(
                    "⬇ Download Report",
                    clean_report,
                    file_name="construction_report.txt"
                )

            # =========================
            # METRICS SECTION
            # =========================
            st.markdown("<br>", unsafe_allow_html=True)

            m1, m2, m3 = st.columns(3)

            with m1:
                st.markdown(
                    f"""
                    <div class='metric-card'>
                        <h4>Total Steps</h4>
                        <h2>{metrics.get('steps', 'N/A')}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with m2:
                st.markdown(
                    f"""
                    <div class='metric-card'>
                        <h4>Estimated Duration</h4>
                        <h2>{metrics.get('duration', 'N/A')}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with m3:
                st.markdown(
                    f"""
                    <div class='metric-card'>
                        <h4>Estimated Budget</h4>
                        <h2>{metrics.get('budget', 'N/A')}</h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        except Exception as e:
            st.error(str(e))