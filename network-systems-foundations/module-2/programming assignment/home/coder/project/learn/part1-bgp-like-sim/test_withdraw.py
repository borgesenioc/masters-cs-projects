from bgpLikeSim import Router, Route

rtr = Router()

# Manually add routes to the RIB
rtr.rib["10.0.0.0/24"] = [
    Route("1.1.1.1", "10.0.0.0", 24, [1, 2, 3]),
    Route("2.2.2.2", "10.0.0.0", 24, [4, 5]),
]
rtr.rib["10.0.0.0/22"] = [
    Route("3.3.3.3", "10.0.0.0", 22, [6, 7, 8, 9]),
]

print("=== Before withdraw ===")
rtr.printRIB()

# Withdraw one route
print("\n--- Withdrawing route from 1.1.1.1 ---")
rtr.withdraw(Route("1.1.1.1", "10.0.0.0", 24, [99, 99]))

print("\n=== After withdraw (should still have 2.2.2.2/24 and 3.3.3.3/22) ===")
rtr.printRIB()

# Withdraw the last route for /24
print("\n--- Withdrawing route from 2.2.2.2 ---")
rtr.withdraw(Route("2.2.2.2", "10.0.0.0", 24, [99, 99]))

print("\n=== After second withdraw (should have no /24, only 3.3.3.3/22) ===")
rtr.printRIB()

# Withdraw from a prefix that doesn't exist
print("\n--- Withdrawing from non-existent prefix ---")
rtr.withdraw(Route("5.5.5.5", "99.99.99.99", 32, [1]))

print("\n=== After bad withdraw (unchanged) ===")
rtr.printRIB()
