from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="CogniFix AI")

troubleshooting_data = {
    "wifi_issue": [
        "Check whether Wi-Fi is turned on.",
        "Restart your router.",
        "Forget the Wi-Fi network and reconnect.",
        "Restart your device.",
        "Contact ISP if issue continues."
    ],
    "slow_internet": [
        "Restart your router.",
        "Disconnect unused devices.",
        "Move closer to the router.",
        "Check internet speed.",
        "Contact ISP if speed is still low."
    ],
    "login_issue": [
        "Check username and password.",
        "Reset your password.",
        "Clear browser cache.",
        "Try another browser.",
        "Contact support if login still fails."
    ],
    "account_locked": [
        "Wait for some time before trying again.",
        "Reset your password.",
        "Check email verification.",
        "Avoid multiple wrong attempts.",
        "Contact support to unlock account."
    ],
    "app_crash": [
        "Close the app completely.",
        "Restart your device.",
        "Update the app.",
        "Clear app cache.",
        "Reinstall the app."
    ],
    "payment_failed": [
        "Check internet connection.",
        "Verify card or UPI details.",
        "Check bank balance.",
        "Try another payment method.",
        "Contact support if money was deducted."
    ],
    "refund_issue": [
        "Check refund status.",
        "Wait 3 to 5 business days.",
        "Verify payment details.",
        "Check email or SMS updates.",
        "Contact customer support."
    ],
    "battery_drain": [
        "Reduce screen brightness.",
        "Close background apps.",
        "Turn on battery saver.",
        "Check battery usage.",
        "Update system software."
    ],
    "bluetooth_issue": [
        "Turn Bluetooth off and on.",
        "Forget and reconnect the device.",
        "Check device compatibility.",
        "Restart your device.",
        "Update system software."
    ],
    "software_update_issue": [
        "Check internet connection.",
        "Ensure enough storage.",
        "Restart your device.",
        "Try update again.",
        "Contact support if update fails."
    ]
}


class IssueRequest(BaseModel):
    issue_type: str


def generate_solution(issue_type):
    steps = troubleshooting_data[issue_type]

    solution = []
    solution.append(f"AI Analysis: The selected issue is '{issue_type}'.")
    solution.append("The system retrieved deterministic steps from the knowledge base.")
    solution.append("")
    solution.append("Recommended Troubleshooting Steps:")

    for i, step in enumerate(steps, start=1):
        solution.append(f"Step {i}: {step}")

    solution.append("")
    solution.append("Final Advice: If the problem continues, contact customer support.")

    return solution


def create_html(solution=None):
    options = ""
    for issue in troubleshooting_data.keys():
        options += f'<option value="{issue}">{issue}</option>'

    result_html = ""
    if solution:
        result_html = "<div class='result'><h2>Generated Solution</h2>"
        result_html += "<pre>"
        for line in solution:
            result_html += line + "\n"
        result_html += "</pre></div>"

    return f"""
<!DOCTYPE html>
<html>
<head>
    <title>CogniFix AI</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #e0e7ff, #f8fafc);
            padding: 40px;
        }}

        .box {{
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 35px;
            border-radius: 18px;
            box-shadow: 0 0 20px rgba(0,0,0,0.25);
        }}

        h1 {{
            text-align: center;
            color: #1d4ed8;
            font-size: 40px;
            margin-bottom: 5px;
        }}

        h3 {{
            text-align: center;
            color: #333;
        }}

        label {{
            font-size: 18px;
            font-weight: bold;
        }}

        select, button {{
            width: 100%;
            padding: 14px;
            margin-top: 15px;
            font-size: 17px;
            border-radius: 8px;
        }}

        button {{
            background: #1d4ed8;
            color: white;
            border: none;
            cursor: pointer;
            font-weight: bold;
        }}

        button:hover {{
            background: #1e40af;
        }}

        .result {{
            margin-top: 25px;
            background: #f1f5f9;
            padding: 22px;
            border-radius: 12px;
            border-left: 6px solid #1d4ed8;
        }}

        pre {{
            white-space: pre-wrap;
            font-size: 16px;
            line-height: 1.6;
        }}
    </style>
</head>
<body>
    <div class="box">
        <h1>CogniFix AI</h1>
        <h3>LLM-Driven Intelligent Troubleshooting Agent</h3>

        <form action="/solve" method="post">
            <label>Select Issue Type:</label>
            <select name="issue_type">
                {options}
            </select>

            <button type="submit">Generate Solution</button>
        </form>

        {result_html}
    </div>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def home():
    return create_html()


@app.post("/solve", response_class=HTMLResponse)
def solve(issue_type: str = Form(...)):
    solution = generate_solution(issue_type)
    return create_html(solution)


@app.get("/fix/{issue_type}")
def fix_issue(issue_type: str):
    if issue_type not in troubleshooting_data:
        return {
            "error": "Issue not found",
            "available_issues": list(troubleshooting_data.keys())
        }

    return {
        "project": "CogniFix AI",
        "issue_type": issue_type,
        "solution": generate_solution(issue_type)
    }


@app.post("/troubleshoot")
def troubleshoot(request: IssueRequest):
    issue_type = request.issue_type

    if issue_type not in troubleshooting_data:
        return {
            "error": "Issue not found",
            "available_issues": list(troubleshooting_data.keys())
        }

    return {
        "project": "CogniFix AI",
        "issue_type": issue_type,
        "retrieved_steps": troubleshooting_data[issue_type],
        "generated_solution": generate_solution(issue_type)
    }