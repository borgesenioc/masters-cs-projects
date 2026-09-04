from bgpLikeSim import Router, Route

rtr = Router()

# Test adding new routes
print("=== Adding routes ===")
rtr.update(Route("1.1.1.1", "10.0.0.0", 24, [1, 2, 3]))
rtr.update(Route("2.2.2.2", "10.0.0.0", 24, [4, 5]))
rtr.update(Route("3.3.3.3", "10.0.0.0", 22, [6, 7, 8, 9]))
rtr.printRIB()

# Test updating an existing neighbor's route
print("\n=== Updating 1.1.1.1's route (should replace) ===")
rtr.update(Route("1.1.1.1", "10.0.0.0", 24, [10, 20, 30]))
rtr.printRIB()

# Test withdrawing
print("\n=== Withdrawing 1.1.1.1 ===")
rtr.withdraw(Route("1.1.1.1", "10.0.0.0", 24, [99]))
rtr.printRIB()

# Test withdrawing last route for prefix
print("\n=== Withdrawing 2.2.2.2 (last /24) ===")
rtr.withdraw(Route("2.2.2.2", "10.0.0.0", 24, [99]))
rtr.printRIB()

# Test withdrawing non-existent prefix
print("\n=== Withdrawing non-existent ===")
rtr.withdraw(Route("5.5.5.5", "99.99.99.99", 32, [1]))
rtr.printRIB()
