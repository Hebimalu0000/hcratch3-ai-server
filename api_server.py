import streamlit as st
from model import generate_response
from save_to_github import save_to_github
import json
from datetime import datetime
import os

LOG_FILE = "api_usage.json"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump({"requests": 0, "success": 0, "failures": 0, "logs": []}, f)

st.title("AI API Server")

if "api" in st.query_params:
    st.write("### AI API Endpoint")
    query_params = st.query_params
    prompt = query_params.get("prompt", [""])[0]

    if prompt:
        try:
            response = generate_response(prompt)
            st.json({"status": "success", "response": response})

            conversation_data = {"prompt": prompt, "response": response}
            save_to_github(conversation_data)

            with open(LOG_FILE, "r+") as f:
                data = json.load(f)
                data["requests"] += 1
                data["success"] += 1
                data["logs"].append({"timestamp": datetime.now().isoformat(), "prompt": prompt, "response": response})
                f.seek(0)
                json.dump(data, f, indent=4)
        except Exception as e:
            st.json({"status": "failure", "error": str(e)})

            with open(LOG_FILE, "r+") as f:
                data = json.load(f)
                data["requests"] += 1
                data["failures"] += 1
                f.seek(0)
                json.dump(data, f, indent=4)
    else:
        st.json({"status": "failure", "error": "No prompt provided."})

else:
    st.write("### API Usage Dashboard")
    with open(LOG_FILE, "r") as f:
        data = json.load(f)

    st.write("#### API Request Statistics")
    st.bar_chart({"Requests": [data["requests"]], "Success": [data["success"]], "Failures": [data["failures"]]})

    st.write("#### Recent Logs")
    st.json(data["logs"][-5:])
