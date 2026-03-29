import subprocess

process = subprocess.Popen(["./bub", "5", "7", "3"], stdout=subprocess.PIPE, text=True)

for line in process.stdout:
    print(f"Python caught this: {line.strip()}")
