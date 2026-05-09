import streamlit as st
import pandas as pd
import os
from datetime import datetime

# ---------- HISTORY FILE SETUP ----------
HISTORY_FILE = "history.csv"

if not os.path.exists(HISTORY_FILE):
    df = pd.DataFrame(columns=[
        "Date",
        "Player",
        "Hours Played",
        "Amount Paid",
        "Balance"
    ])
    df.to_csv(HISTORY_FILE, index=False)

# ---------- APP TITLE ----------
st.title("🏸 Badminton Expense Splitter")

# ---------- INPUTS ----------
total_cost = st.number_input(
    "Enter total court cost",
    min_value=0.0
)

num_players = st.number_input(
    "Enter number of players",
    min_value=1,
    step=1
)

players = {}
payments = {}

# ---------- HOURS INPUT ----------
st.subheader("Enter hours played")

for i in range(int(num_players)):

    name = st.text_input(
        f"Player {i+1} name",
        key=f"name{i}"
    )

    hours = st.number_input(
        f"Hours played by {name}",
        min_value=0.0,
        key=f"hours{i}"
    )

    if name:
        players[name] = hours

# ---------- PAYMENT INPUT ----------
st.subheader("Enter payments")

for name in players:
    payments[name] = st.number_input(
        f"Amount paid by {name}",
        min_value=0.0,
        key=f"pay_{name}"
    )

# ---------- CALCULATE BUTTON ----------
if st.button("Calculate Split"):

    total_player_hours = sum(players.values())

    if total_player_hours == 0:
        st.error("Total player hours cannot be zero.")

    else:

        # ---------- COST CALCULATION ----------
        cost_per_hour = total_cost / total_player_hours

        balances = {}

        for person in players:

            fair_share = players[person] * cost_per_hour

            balances[person] = round(
                payments.get(person, 0) - fair_share,
                2
            )

        # ---------- BALANCES ----------
        st.subheader("Balances")

        for person, balance in balances.items():

            if balance > 0:
                st.write(f"{person} should receive ₹{balance:.2f}")

            elif balance < 0:
                st.write(f"{person} should pay ₹{-balance:.2f}")

            else:
                st.write(f"{person} is settled")

        # ---------- SAVE HISTORY ----------
        history_rows = []

        current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

        for person in players:

            history_rows.append({
                "Date": current_date,
                "Player": person,
                "Hours Played": players[person],
                "Amount Paid": payments[person],
                "Balance": balances[person]
            })

        new_data = pd.DataFrame(history_rows)

        existing_data = pd.read_csv(HISTORY_FILE)

        updated_data = pd.concat(
            [existing_data, new_data],
            ignore_index=True
        )

        updated_data.to_csv(HISTORY_FILE, index=False)

        # ---------- SETTLEMENT ----------
        st.subheader("Settlement")

        creditors = [
            (p, b)
            for p, b in balances.items()
            if b > 0
        ]

        debtors = [
            (p, -b)
            for p, b in balances.items()
            if b < 0
        ]

        i, j = 0, 0

        while i < len(debtors) and j < len(creditors):

            d_name, d_amt = debtors[i]
            c_name, c_amt = creditors[j]

            pay = min(d_amt, c_amt)

            st.write(f"👉 {d_name} pays ₹{pay:.2f} to {c_name}")

            d_amt -= pay
            c_amt -= pay

            debtors[i] = (d_name, d_amt)
            creditors[j] = (c_name, c_amt)

            if d_amt <= 0.01:
                i += 1

            if c_amt <= 0.01:
                j += 1

# ---------- MATCH HISTORY ----------
st.subheader("📜 Match History")

history_df = pd.read_csv(HISTORY_FILE)

if len(history_df) > 0:
    st.dataframe(history_df)

else:
    st.info("No history available yet.")
