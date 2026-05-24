from core.engine.base_etl import BaseETL
from sqlalchemy import text

etl = BaseETL()
engine = etl.get_mssql_engine()

with engine.connect() as conn:
    print('ستون‌های DarkhastFaktor:')
    cols = conn.execute(text(\"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='DarkhastFaktor' ORDER BY ORDINAL_POSITION\")).fetchall()
    for i, col in enumerate(cols, 1):
        print(f'  {i}. {col[0]}')
    
    print()
    print('ستون‌های DarkhastFaktorSatr:')
    cols2 = conn.execute(text(\"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='DarkhastFaktorSatr' ORDER BY ORDINAL_POSITION\")).fetchall()
    for i, col in enumerate(cols2, 1):
        print(f'  {i}. {col[0]}')
