import matplotlib.pyplot as plt
import math


# ------------------------------------------------
# 1. READ DATA FROM TEXT FILE
# ------------------------------------------------

numbers = []

with open("data.txt", "r") as file:

    for line in file:

        # Remove spaces/new-line characters
        line = line.strip()

        # Ignore empty lines
        if line == "":
            continue

        number = float(line)

        # Benford analysis does not use zero
        if number != 0:
            numbers.append(abs(number))


# ------------------------------------------------
# 2. COUNT FIRST DIGITS
# ------------------------------------------------

# Create counters for digits 1 to 9
digit_counts = {
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 0
}


for number in numbers:

    # Convert number to text
    number_text = str(number)

    # Remove decimal point and leading zeros
    number_text = number_text.replace(".", "").lstrip("0")

    # Get first digit
    first_digit = int(number_text[0])

    # Increase counter
    digit_counts[first_digit] += 1


# ------------------------------------------------
# 3. CALCULATE ACTUAL PERCENTAGES
# ------------------------------------------------

total_numbers = len(numbers)

actual_percentage = []

for digit in range(1, 10):

    percentage = (
        digit_counts[digit] / total_numbers
    ) * 100

    actual_percentage.append(percentage)


# ------------------------------------------------
# 4. CALCULATE BENFORD EXPECTED PERCENTAGES
#
# Formula:
# P(d) = log10(1 + 1/d)
# ------------------------------------------------

benford_percentage = []

for digit in range(1, 10):

    percentage = math.log10(
        1 + (1 / digit)
    ) * 100

    benford_percentage.append(percentage)


# ------------------------------------------------
# 5. COMPARE DATASET WITH BENFORD'S LAW
# ------------------------------------------------

differences = []

for i in range(9):

    difference = abs(
        actual_percentage[i] - benford_percentage[i]
    )

    differences.append(difference)


# Mean Absolute Deviation
mad = sum(differences) / 9


# Simple demonstration threshold
if mad < 5:

    conclusion = "Dataset broadly follows Benford's Law"

    # Green analysis box
    box_color = "lightgreen"

else:

    conclusion = "Dataset does NOT closely follow Benford's Law"

    # Red analysis box
    box_color = "lightcoral"


# ------------------------------------------------
# 6. CREATE GRAPH
# ------------------------------------------------

digits = list(range(1, 10))


# Give each histogram bar a different color
colors = [
    "royalblue",
    "seagreen",
    "orange",
    "mediumpurple",
    "tomato",
    "deepskyblue",
    "hotpink",
    "sienna",
    "gray"
]


plt.figure(figsize=(11, 7))


# ------------------------------------------------
# Draw actual dataset
# ------------------------------------------------

plt.bar(
    digits,
    actual_percentage,
    color=colors,
    edgecolor="black",
    label="Actual Dataset"
)


# ------------------------------------------------
# Draw expected Benford distribution
# ------------------------------------------------

plt.plot(
    digits,
    benford_percentage,
    color="red",
    marker="o",
    linewidth=2,
    label="Benford's Law"
)


# ------------------------------------------------
# Graph labels
# ------------------------------------------------

plt.xlabel("First Digit")
plt.ylabel("Percentage (%)")

plt.title("Benford's Law Analysis")

plt.xticks(digits)

plt.legend()

plt.grid(
    axis="y",
    alpha=0.3
)


# ------------------------------------------------
# 7. ADD ANALYSIS INSIDE GRAPH
# ------------------------------------------------

analysis_text = (
    "ANALYSIS\n"
    + conclusion
    + "\n"
    + "MAD: "
    + str(round(mad, 2))
    + "%"
)


plt.text(
    5,
    25,
    analysis_text,
    fontsize=11,
    bbox=dict(
        facecolor=box_color,
        edgecolor="black",
        alpha=0.9
    )
)


# ------------------------------------------------
# 8. SAVE GRAPH AS PNG
# ------------------------------------------------

plt.savefig(
    "benford_result.png",
    dpi=150,
    bbox_inches="tight"
)


# ------------------------------------------------
# 9. PRINT RESULTS IN COMMAND PROMPT
# ------------------------------------------------

print()
print("--------------------------------------")
print("BENFORD'S LAW ANALYSIS")
print("--------------------------------------")
print("Number of records:", total_numbers)
print("MAD:", round(mad, 2), "%")
print("Result:", conclusion)
print("--------------------------------------")
print()
print("Graph saved as: benford_result.png")
print()


# ------------------------------------------------
# 10. SHOW GRAPH
# ------------------------------------------------

plt.show()