import streamlit as st

st.title("🏸 Badminton Expense Splitter")

total_cost = st.number_input("Enter total court cost", min_value=0.0)
num_players = st.number_input("Enter number of players", min_value=1, step=1)

players = {}
payments = {}

st.subheader("Enter hours played")

for i in range(int(num_players)):
    name = st.text_input(f"Player {i+1} name", key=f"name{i}")
    hours = st.number_input(f"Hours played by {name}", min_value=0.0, key=f"hours{i}")

    if name:
        players[name] = hours

st.subheader("Enter payments")

for name in players:
    payments[name] = st.number_input(f"Amount paid by {name}", min_value=0.0, key=f"pay_{name}")

if st.button("Calculate Split"):

    total_player_hours = sum(players.values())

    if total_player_hours == 0:
        st.error("Total player hours cannot be zero.")
    else:
        cost_per_hour = total_cost / total_player_hours

        balances = {}
        for person in players:
            fair_share = players[person] * cost_per_hour
            balances[person] = round(payments.get(person, 0) - fair_share, 2)

        st.subheader("Balances")

        for person, balance in balances.items():
            if balance > 0:
                st.write(f"{person} should receive ₹{balance:.2f}")
            elif balance < 0:
                st.write(f"{person} should pay ₹{-balance:.2f}")
            else:
                st.write(f"{person} is settled")

        st.subheader("Settlement")

        creditors = [(p, b) for p, b in balances.items() if b > 0]
        debtors = [(p, -b) for p, b in balances.items() if b < 0]

        i, j = 0, 0

        while i < len(debtors) and j < len(creditors):
            d_name, d_amt = debtors[i]
            c_name, c_amt = creditors[j]

            pay = min(d_amt, c_amt)

            st.write(f"{d_name} pays ₹{pay:.2f} to {c_name}")

            d_amt -= pay
            c_amt -= pay

            debtors[i] = (d_name, d_amt)
            creditors[j] = (c_name, c_amt)

            if d_amt <= 0.01:
                i += 1
            if c_amt <= 0.01:
                j += 1