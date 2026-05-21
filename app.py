import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
import requests

# ==============================
# LOAD ENV VARIABLES
# ==============================

load_dotenv()

# ==============================
# STREAMLIT CONFIG
# ==============================

st.set_page_config(
    page_title="VertexBridge ERP AI Command Center",
    layout="wide"
)

# ==============================
# SIDEBAR
# ==============================

st.sidebar.title("ERP AI Control Panel")

st.sidebar.info("""
Features:
- ERP Risk Analysis
- Workstream Intelligence
- Go-Live Readiness Tracking
- Executive AI Insights
- RAID Log Analytics
""")

# ==============================
# TITLE
# ==============================

st.title("VertexBridge ERP AI Command Center")

st.caption(
    "AI-Powered ERP Transformation Intelligence Platform"
)

# ==============================
# FILE UPLOAD
# ==============================

uploaded_file = st.file_uploader(
    "Upload ERP Tracker Excel File",
    type=["xlsx"]
)

# ==============================
# MAIN APP
# ==============================

if uploaded_file:

    # ==============================
    # READ EXCEL SHEETS
    # ==============================

    project_status = pd.read_excel(
        uploaded_file,
        sheet_name="Project_Status",
        header=1
    )

    raid_log = pd.read_excel(
        uploaded_file,
        sheet_name="RAID_Log",
        header=1
    )

    go_green = pd.read_excel(
        uploaded_file,
        sheet_name="Go_to_Green_Plans",
        header=1
    )

    # ==============================
    # SUCCESS MESSAGE
    # ==============================

    st.success("Excel file uploaded successfully!")

    # ==============================
    # KPI DASHBOARD
    # ==============================

    st.markdown("## ERP Program KPIs")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric(
        "RAID Items",
        len(raid_log)
    )

    kpi2.metric(
        "Project Tasks",
        len(project_status)
    )

    kpi3.metric(
        "Go-Live Actions",
        len(go_green)
    )

    kpi4.metric(
        "Total Sheets",
        3
    )

    # VISUAL ANALYTICS

    st.markdown("## ERP Program Insights")

    insight1, insight2 = st.columns(2)

    with insight1:

        st.info(f"""
        Total RAID items identified: {len(raid_log)}

        Active ERP transformation tracking is in progress
        across multiple operational areas.
        """)

    with insight2:

        st.info(f"""
        Go-live readiness activities tracked:
        {len(go_green)}

        Project governance and mitigation planning
        workflows are active.
        """)

    # ==============================
    # PREVIEW DATA
    # ==============================

    with st.expander("Preview ERP Data"):

        st.subheader("Project Status")
        st.dataframe(project_status.head())

        st.subheader("RAID Log")
        st.dataframe(raid_log.head())

        st.subheader("Go To Green Plans")
        st.dataframe(go_green.head())

    # ==============================
    # CHAT SECTION
    # ==============================

    st.subheader("Ask ERP AI Agent")

    st.markdown("### Suggested Questions")

    col1, col2, col3 = st.columns(3)

    # Suggested Buttons

    with col1:

        if st.button("Financial Risks"):

            st.session_state.query = (
                "Summarise all risks with financial exposure"
            )

    with col2:

        if st.button("Workstream Issues"):

            st.session_state.query = (
                "Which workstream has had the most issues and what is the pattern?"
            )

    with col3:

        if st.button("Go-Live Readiness"):

            st.session_state.query = (
                "What needs to happen before go-live?"
            )

    # ==============================
    # USER INPUT
    # ==============================

    user_query = st.text_input(
        "Ask your question:",
        value=st.session_state.get("query", "")
    )

    # ==============================
    # PROCESS QUERY
    # ==============================

    if user_query:

        with st.spinner(
            "Running enterprise intelligence analysis..."
        ):

            query_lower = user_query.lower()

            analysis_result = ""

            # ==========================================
            # WORKSTREAM ANALYSIS
            # ==========================================

            if (
                "workstream" in query_lower
                or "issues" in query_lower
            ):

                try:

                    workstream_column = raid_log.columns[0]

                    workstream_counts = (
                        raid_log.groupby(
                            workstream_column
                        )
                        .size()
                        .sort_values(
                            ascending=False
                        )
                    )

                    top_workstreams = (
                        workstream_counts
                        .head(10)
                        .to_string()
                    )

                    analysis_result = f"""
                    Workstream Issue Distribution:

                    {top_workstreams}

                    Higher counts indicate
                    recurring issue concentration.
                    """

                except Exception as e:

                    analysis_result = (
                        f"Workstream analysis failed: {e}"
                    )

            # ==========================================
            # FINANCIAL RISK ANALYSIS
            # ==========================================

            elif (
                "financial" in query_lower
                or "risk" in query_lower
            ):

                try:

                    financial_rows = raid_log[
                        raid_log.astype(str)
                        .apply(
                            lambda row:
                            row.str.contains(
                                "financial",
                                case=False
                            ).any(),
                            axis=1
                        )
                    ]

                    analysis_result = (
                        financial_rows
                        .head(10)
                        .to_string()
                    )

                except Exception as e:

                    analysis_result = (
                        f"Financial analysis failed: {e}"
                    )

            # ==========================================
            # GO-LIVE ANALYSIS
            # ==========================================

            elif (
                "go-live" in query_lower
                or "readiness" in query_lower
            ):

                try:

                    analysis_result = (
                        go_green
                        .head(15)
                        .to_string()
                    )

                except Exception as e:

                    analysis_result = (
                        f"Go-live analysis failed: {e}"
                    )

            # ==========================================
            # GENERAL ANALYSIS
            # ==========================================

            else:

                analysis_result = f"""
                ERP Program Summary

                Project Status Rows:
                {len(project_status)}

                RAID Log Rows:
                {len(raid_log)}

                Go-To-Green Rows:
                {len(go_green)}

                Available Modules:
                - Project Status
                - RAID Log
                - Go-To-Green Plans
                """

            # ==========================================
            # FINAL PROMPT
            # ==========================================

            final_prompt = f"""
            You are a senior ERP Transformation
            Intelligence Advisor.

            Analyze enterprise ERP transformation
            data and provide concise
            executive-level insights.

            Your responsibilities:
            - Identify high-risk workstreams
            - Detect escalation patterns
            - Highlight delivery blockers
            - Analyze financial exposure
            - Assess go-live readiness
            - Recommend mitigation priorities

            Rules:
            - Be concise
            - Use bullet points where useful
            - Focus on business impact
            - Sound like an enterprise consultant
            - Use consulting-style language

            ANALYSIS RESULT:
            {analysis_result}

            USER QUESTION:
            {user_query}
            """

            # ==========================================
            # OPENROUTER API CALL
            # ==========================================

            headers = {
                "Authorization":
                f"Bearer {os.getenv('OPENROUTER_API_KEY')}",

                "Content-Type":
                "application/json"
            }

            payload = {
                "model": "openai/gpt-3.5-turbo",

                "messages": [
                    {
                        "role": "user",
                        "content": final_prompt
                    }
                ]
            }

            try:

                api_response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload
                )

                result = api_response.json()

                # ==========================================
                # HANDLE RESPONSE
                # ==========================================

                if "choices" in result:

                    answer = (
                        result["choices"][0]
                        ["message"]["content"]
                    )

                elif "error" in result:

                    answer = f"""
                    API Error:
                    {result['error']['message']}
                    """

                else:

                    answer = (
                        "Unexpected API response."
                    )

            except Exception as e:

                answer = f"""
                System Error:
                {e}
                """

            # ==========================================
            # DISPLAY RESPONSE
            # ==========================================

            st.markdown("## AI Agent Response")

            st.write(answer)

            st.markdown("---")

            st.caption(
                "VertexBridge ERP AI Command Center | "
                "Powered by LLM Analytics & Enterprise Intelligence"
            )