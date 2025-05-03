import os
from dotenv import load_dotenv
from dbt.cli.main import dbtRunner

# 加載 .env
load_dotenv()

# 驗證 TIMEZONE
if not os.getenv("TIMEZONE"):
    print("Error: TIMEZONE not set in .env")
    exit(1)
print(f"TIMEZONE: {os.getenv('TIMEZONE')}")

# 初始化 DBT
dbt = dbtRunner()

# 運行 dbt clean
print("運行 dbt clean...")
dbt.invoke(["clean", "--profiles-dir", "."])

# 運行 dbt run
print("運行 dbt run...")
dbt.invoke(["run", "--profiles-dir", "."])

# 運行 dbt test
print("運行 dbt test...")
dbt.invoke(["test", "--profiles-dir", "."])