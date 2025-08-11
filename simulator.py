import json, time, random, datetime, subprocess

# Temperature threshold
SAFE_TEMP_LIMIT = 85  # degrees Celsius

def get_status(temp):
    # return CSS-friendly status strings
    return "overheat" if temp >= SAFE_TEMP_LIMIT else "safe"

def run_simulation(entry_limit = 10):
    global running
    running = True
    print("Running simulation......")
    count = 0
    previous_status = "safe"

    while count < entry_limit and running:
        temp = random.randint(60, 100)  # Simulated temperature
        status = get_status(temp)
        data = {
            "temperature": temp,
            "status": status,
            "timestamp": datetime.datetime.now().isoformat()
        }

        try:
            with open("data.json","a") as f:
                json.dump(data, f)
                f.write("\n")
            print(f"Simulated: {data}")
        except Exception as e:
            print(f"Error writing to file: {e}")

        # run alert script only on first transition safe -> overheat
        if previous_status == "safe" and status == "overheat":
            print("Overheat detected. Running mail.js...")
            try:
                subprocess.run(["node", "mail.js"])
            except Exception as e:
                print("Failed to run mail.js:", e)

        previous_status = status
        count += 1
        time.sleep(5)

def stop_simulation():
    global running
    running = False
