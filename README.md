# ETL Warehouse — Quick Start

این مخزن یک فریم‌ورک ETL سبک برای بارگذاری داده‌ها از دیتابیس مادر به یک DW بر پایه PostgreSQL و اورکستراسیون با Airflow فراهم می‌کند.

هر آنچه اینجا می‌سازیم قابل اجرا به‌صورت محلی با `docker-compose` است.

Prerequisites
- Docker & Docker Compose
- Python 3.10+

تنظیمات اتصال (نمونه)
- فایل‌های پیکربندی نمونه در `config/*.example` قرار دارند. قبل از اجرا، یک کپی ایجاد کنید و مقادیر را پر کنید:

```bash
cp config/databases.yaml.example config/databases.yaml
cp config/settings.yaml.example config/settings.yaml
```

یا متغیرهای محیطی لازم را در `.env` قرار دهید (موجود در ریشه در صورت نیاز).

مهم‌ترین متغیرهای اتصال (مثال):
- `SRC_DB_USER`, `SRC_DB_PASSWORD`, `SRC_DB_HOST`, `SRC_DB_PORT`, `SRC_DB_DATABASE`
- `TGT_DB_USER`, `TGT_DB_PASSWORD`, `TGT_DB_HOST`, `TGT_DB_PORT`, `TGT_DB_DATABASE`

تولید DDL از شِماها
- فایل‌های JSON شِما در `mother data base guide/` قرار دارند.
- برای تولید DDL کلی برای انبار داده اجرا کنید:

```bash
python scripts/generate_ddl.py
python scripts/generate_dw_sales_ddl.py
```

این اسکریپت‌ها SQLهای تولیدشده را در `warehouse_tables/generated` و `warehouse_tables/final` می‌نویسند.

اجرای Airflow محلی (با docker-compose)

```bash
# ساخت و اجرای سرویس‌ها (شامل Airflow)
docker-compose up -d

# لاگ‌ها
docker-compose logs -f
```

پس از بالا آمدن Airflow، DAG نمونه `sales_incremental_and_agg` در پوشه `dags/` قابل مشاهده و فعال‌سازی است.

Metabase (BI)
----------------
We include a Metabase service in `docker-compose.yml` exposed on port `3000`.
To connect Metabase to the DW (Postgres):

1. Start services:

```bash
docker-compose up -d
```

2. Open Metabase at http://localhost:3000 and follow the setup flow. For the database connection use:

- Database type: PostgreSQL
- Host: `postgres` (or `localhost` if connecting externally)
- Port: value from `.env` `TGT_DB_PORT` (default 5432)
- Database name: `TGT_DB_DATABASE`
- Username/password: from `.env` `TGT_DB_USER` / `TGT_DB_PASSWORD`

3. After adding the DW, enable scanning of the schemas and sync the data model. Create dashboards based on `agg_daily_sales`, `agg_weekly_sales`, and fact tables.

اجرای تست‌های پایتون

```bash
pip install -r requirements.txt  # اگر فایلی موجود است
pytest -q
```

نکات عملیاتی
- فعلاً فایل‌های پیکربندی پیش‌فرض در پوشه `confing/` قرار دارند؛ `BaseETL` به دنبال `config/` می‌گردد. لطفاً فایل‌های نمونه را به `config/` کپی و مقادیر را تکمیل کنید.
- اگر اتصال به دیتابیس ندارید، می‌توانید اسکریپت‌های تولید DDL و DAGها را محلی بررسی کنید بدون نیاز به دیتابیس.

در صورت تمایل من می‌توانم:
- فایل `config/databases.yaml` را با مقادیر شما تولید کنم (در صورت ارائه مقادیر).
- `docker-compose.yml` را برای اجرای Airflow محلی بررسی و در صورت نیاز اصلاح کنم.
