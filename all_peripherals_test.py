from Controller.peripheral_class import debug_peripheral

print("starting test")
# debug_peripheral('Peripheral_path', "fan", 1)
print("Starting fan")
# debug_peripheral('Ignore', "heat", 1)
print("light test")
# debug_peripheral('Ignore', "light", 1)
print("Water test")
debug_peripheral('Ignore', "water", 1)
print("End test")
