import os
import subprocess

def run_command(command):
    process = subprocess.run(command, shell=True)
    if process.returncode != 0:
        raise Exception(f"Command failed: {command}")

# Run pipeline
commands = [
        "python 0_api_dlt_load.py",
        "python 1_spark_process.py",
        "cd deals_dbt && python run_dbt.py"
    ]

for cmd in commands:
    run_command(cmd)