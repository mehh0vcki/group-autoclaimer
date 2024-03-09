print("\n\n")
from format import generate_logo, generate_text

generate_logo()
generate_text("======================", 0)

generate_text("this color is default color, this color is using to send messages on start, and about claim status", 0)
generate_text("this color is account color, this color is using to show details of account switch", 1)
generate_text("this color is debug color, this color is using to print out data if showAccountSwitchData or showClaimData enabled.", 3)