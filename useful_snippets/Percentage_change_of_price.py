# Importing libraries:
import pandas as pd

data = {
    "open": [80, 390, 500, 600, 800, 900],
    "high": [90, 400, 510, 610, 850, 901],
    "low": [75, 380, 480, 550, 750, 852],
    "close": [100, 400, 500, 650, 53, 50],
}

# load data into a DataFrame object:
df = pd.DataFrame(data)

first_row_df = df["close"].iloc[1]
# print(f"First row is: {first_row_df}")

penultimate_row_df = df["close"].iloc[-2]
print(f"Penultimate row is: {penultimate_row_df}")

last_row_df = df["close"].iloc[-1]
print(f"Last row is: {last_row_df}")

if penultimate_row_df >= last_row_df:
    # Percentage difference, round on 2 decimals
    percentage_difference = round(
        ((penultimate_row_df - last_row_df) / ((penultimate_row_df + last_row_df) / 2))
        * 100,
        2,
    )
    print(f"Percentage difference is: {percentage_difference}")

elif penultimate_row_df < last_row_df:
    # Percentage difference, round on 2 decimals
    percentage_difference = round(
        ((last_row_df - penultimate_row_df) / ((penultimate_row_df + last_row_df) / 2))
        * 100,
        2,
    )
    print(f"Percentage difference is: {percentage_difference}")


# Percentage trigger for signal:
# percentage_trigger = int(input("Insert percentage difference for signal trigger: (E.g. 4):"))

percentage_trigger = 4
# percentage_trigger = percentage_trigger / 100
print(f"Percentage trigger is: {percentage_trigger}%.")


if percentage_difference >= percentage_trigger:

    if penultimate_row_df >= last_row_df:
        print(
            f"[LRCUSDT] Price has dropped for -{percentage_difference}% in last hour. Try LONG! Visit: [link]"
        )
    elif penultimate_row_df < last_row_df:
        print(
            f"[LRCUSDT] Price has pumped for +{percentage_difference}% in last hour. Try SHORT! Visit: [link]"
        )
else:
    print("[LRCUSDT] passed without triggering condition.")
