import os, sqlite3

from flask import Flask, redirect, render_template, request, url_for
from openai import OpenAI
client = OpenAI(
    api_key=os.environ.get(".env"),
)

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        lead_diver_name = request.form["name"]
        lead_diver_email = request.form["email"]
        dive_certification = request.form.get("dive_cert")
        if dive_certification == "cavern":
            prompt = "You have selected Cavern as your highlest level of cave diving certification."
        elif dive_certification == "intro_to_cave":
            prompt = "You have selected Intro to Cave/Cave Diver 1 as your highlest level of cave diving certification."
        elif dive_certification == "full_cave":
            prompt = "You have selected Full Cave/Cave Diver 2 as your highlest level of cave diving certification."
        else:
            prompt = "You have not selected a dive certification level."
        plan_content = request.form["plan"]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.6,
            messages=[
                {"role": "system","content": "You will receive submissions of dive plans provided by technical cave divers. Your job is to provide feedback to the user about ways that they could improve their cave dive plan based on the expectations of the National Speleological Society Cave Diving Section (NSS-CDS). Some common errors that should be highlighted, if they are not present on the submitted dive plan, are provided as follows: - If the divers plan to dive deeper than 40 metres, the dive plan should outline how they plan to use an alternate gas supply, other than air, to avoid the effects of nitrogen narcosis - Dive plans often do not outline how equipment redundancy will be handled - Dive plans often do not outline emergency procedures clearly - Dive plans often do not outline how divers will handle a silt-out in the cave - Dive plans often do not outline how dive buddies with different set-ups, such as backmount versus sidemount, will work together as a team"},
                {"role": "user", "content": plan_content}
            ]
        )

        msg = response.choices[0].message.content if response.choices else None
        conn = get_db_connection()
        conn.execute("INSERT INTO diver (LeadDiverName, LeadDiverEmail) VALUES (?, ?)",
                     (lead_diver_name, lead_diver_email))
        conn.execute("INSERT INTO prompts (DivePlan, Msg) VALUES (?, ?)",
                     (plan_content, msg))
        conn.commit()
        conn.close()
        return redirect(url_for("index", result=response.choices[0].message.content))

    result = request.args.get("result")
    return render_template("index.html", result=result)