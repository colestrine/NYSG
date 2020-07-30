from Controller.peripheral_class import debug_peripheral

print("Fan cycle")
debug_peripheral('Peripheral_path', "fan", 1)
print("Heat cycle")
debug_peripheral('Ignore', "heat", 1)
print("LED cycle")
debug_peripheral('Ignore', "light", 1)
print("Valve cycle")
debug_peripheral('Ignore', "water", 1)
print("End test")
