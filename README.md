# Amazon Deals DE Pipeline

## 1. 本專案在幹嘛？

本專案是一個自動化數據管道，從 Rainforest API 擷取 Amazon.de 的優惠商品資料，經過資料清洗、統計分析，最終將結果存入 Google BigQuery，並透過 dbt 進行進一步的數據建模與報表產出。整個流程可部署於 GCP（Google Cloud Platform），並支援自動化排程。

---

## 2. 可以學習到的內容

- 如何串接第三方 API 並自動化資料擷取
- 使用 dlt 進行 ETL 管道建構與 BigQuery 整合
- PySpark 進行大數據處理與統計分析
- dbt 進行數據建模、資料清洗與自動化測試
- GCP BigQuery、Cloud Run、Cloud Scheduler、GCS 等雲端服務的整合與自動化部署（含 Terraform 基礎）
- Docker 化數據管道專案
- .env 與 GCP 金鑰等敏感資訊管理

---

## 3. 使用者先行設置

1. **GCP 金鑰與專案設定**
   - 申請 GCP 專案，啟用 BigQuery、Cloud Run、Cloud Storage 等服務
   - 建立 Service Account，下載金鑰檔（gcp-key.json），放置於專案根目錄
   - 設定 BigQuery Dataset 與 GCS Bucket（可用 `terraform-bigquery/` 自動化建立）

2. **.env 檔案設置**
   - 於專案根目錄建立 `.env`，內容範例如下：
     ```
     RAINFOREST_API_KEY=你的RainforestAPI金鑰
     GCP_PROJECT_ID=你的GCP專案ID
     DLT_DESTINATION_BIGQUERY_LOCATION=US
     DLT_PIPELINE_NAME=deals_pipeline
     DLT_DATASET_NAME=deals_dataset
     AMAZON_DOMAIN=amazon.de
     TIMEZONE=Europe/Berlin
     GCP_CREDENTIALS_PATH=./gcp-key.json
     TEMP_GCS_BUCKET=你的GCS暫存桶名稱
     SPARK_JARS=./spark-3.5-bigquery-0.42.1.jar,./gcs-connector-hadoop3-latest.jar
     HADOOP_HOME=（如需在Windows執行，請指定Hadoop路徑）
     ```

3. **安裝依賴**
   - `pip install -r requirements.txt`
   - 需安裝 Java（PySpark 需要）

4. **Docker 部署（可選）**
   - `docker build -t amazon-deals-pipeline .`
   - `docker run --env-file .env -v $(pwd)/gcp-key.json:/app/gcp-key.json amazon-deals-pipeline`

5. **Terraform 部署（可選）**
   - 於 `terraform-bigquery/`、`terraform-cloud-run/` 依序 `terraform init`、`terraform apply`，自動建立 GCP 資源

---

## 4. 個別檔案中值得特別留意學習的部分

- `0_api_dlt_load.py`：  
  - dlt 管道設計，動態表名、API 資料擷取與欄位結構設計
  - 品牌名稱自動萃取（`extract_brands.py`）

- `1_spark_process.py`：  
  - PySpark 與 BigQuery 整合
  - 多種統計指標一次性計算與寫入
  - 動態表名與時區處理

- `deals_dbt/`：  
  - dbt 專案結構、資料清洗（去重、欄位轉換）、品牌與每日統計模型
  - `schema.yml`：欄位測試設計，資料品質控管
  - `run_dbt.py`：自動化 dbt clean/run/test

- `terraform-bigquery/`、`terraform-cloud-run/`：  
  - GCP BigQuery、GCS、Cloud Run、Cloud Scheduler 的自動化部署腳本

- `dockerfile`：  
  - 如何將 ETL 管道與 Spark、dbt、GCP 整合於單一容器

---

## 5. 最後的成果

- **自動化數據管道**：一鍵執行即可完成 Amazon.de 優惠資料的擷取、清洗、統計與報表產出
- **BigQuery 數據集**：包含原始優惠資料、清洗後資料、品牌統計、每日統計等多張表
- **dbt 報表**：可直接用於 BI 工具分析
- **可雲端自動排程**：支援 GCP Cloud Run + Cloud Scheduler，每日自動執行
- **可擴展性**：可輕鬆調整 API 來源、分析指標、資料模型，並支援多國 Amazon

---

如需更詳細的操作說明，請參考各資料夾內的註解與程式碼說明。
