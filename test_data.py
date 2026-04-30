from samachar_input_adapter import load_data, convert_to_signals

weather, aqi = load_data()

print("\n--- WEATHER DATA ---")
print(weather.head())

print("\n--- AQI DATA ---")
print(aqi.head())

# 🔥 TEST SIGNAL GENERATION
signals = convert_to_signals(weather, aqi)

print("\n--- GENERATED SIGNALS ---")
for s in signals[:5]:
    print(s)
    