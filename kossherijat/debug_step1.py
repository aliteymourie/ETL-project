echo from core.engine.base_etl import BaseETL > debug_step1.py
echo from sqlalchemy import text >> debug_step1.py
echo e = BaseETL() >> debug_step1.py
echo c = e.get_mssql_engine().connect() >> debug_step1.py
echo result = c.execute(text("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='DarkhastFaktor' ORDER BY ORDINAL_POSITION")).fetchall() >> debug_step1.py
echo for row in result: >> debug_step1.py
echo     print(row[0]) >> debug_step1.py