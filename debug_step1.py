from core.engine.base_etl import BaseETL
from sqlalchemy import text

e = BaseETL()
c = e.get_mssql_engine().connect()

# ستون‌های DarkhastFaktor
result = c.execute(text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'DarkhastFaktor' ORDER BY ORDINAL_POSITION")).fetchall()
print('=== DarkhastFaktor ===')
for row in result:
    print(row[0])

print()

# ستون‌های DarkhastFaktorSatr
result2 = c.execute(text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'DarkhastFaktorSatr' ORDER BY ORDINAL_POSITION")).fetchall()
print('=== DarkhastFaktorSatr ===')
for row in result2:
    print(row[0])