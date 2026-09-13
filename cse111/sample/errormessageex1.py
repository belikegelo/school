# # Example 1
# def main():
#     print("Are you surprised, Clark?")
# # Start this program by
# # calling the main function.
# if __name__ == "__main__":
#     main()




# Example 2
def main():
  print("This program computes and prints the remaining")
  print("balance for a loan with a fixed annual percentage")
  print("rate and a fixed number of payments per year.")
  print()
  print("Please enter the following five values.")
  principal = float(input("Principal amount: "))
  annual_rate = float(input("Annual percentage rate: "))
  years = int(input("Number of years in the life of the loan: "))
  payments_per_year = int(input("Number of payments per year: "))
  number_paid = int(input("Number of payments already paid: "))
  balance = compute_balance(principal, annual_rate, years,
          payments_per_year, number_paid)
  print()
  print(f"Balance remaining: {balance}")
def compute_balance(princ, ar, years, ppy, ptd):
  """Compute and return the balance remaining for a loan."""
  payment = compute_payment(princ, ar, years, ppy)
  #Show variable values for debugging
  print()
  print(f"compute_balance({princ}, {ar}, {years}, {ppy}, {ptd})")
  rate = ar / ppy
  power = (1 + rate) ** ptd
  #Show variable values for debugging
  print(f"    payment: {payment}  rate: {rate}  power: {power}")
  balance = princ * power - payment * (power - 1) / rate
  #Show variable values for debugging
  print(f"    balance: {balance:.2f}")
  return round(balance, 2)
def compute_payment(princ, ar, years, ppy):
  """Compute and return the payment per period for a loan."""
  #Show variable values for debugging
  print()
  print(f"compute_payment({princ}, {ar}, {years}, {ppy})")
  rate = ar / ppy
  n = years * ppy
  #Show variable values for debugging
  print(f"    rate: {rate}  n: {n}")
  payment = princ * rate / (1 - (1 + rate) ** -n)
  #Show variable values for debugging
  print(f"    payment: {payment:.2f}")
  return round(payment, 2)
# Start this program by
# calling the main function.
if __name__ == "__main__":
    main()