import sys, os
sys.path.insert(0, '.')

# حذف checkpoint تا کل داده دوباره لود شود
from core.engine.loader import DataLoader
from sqlalchemy import text

loader = DataLoader()
with loader.tgt_engine.begin() as conn:
    conn.execute(text(\"DELETE FROM etl_metadata.etl_checkpoint WHERE pipeline_name = 'fact_treasury'\"))
    conn.execute(text('TRUNCATE TABLE fact_treasury'))

print('✅ Checkpoint پاک شد. حالا fact_treasury را دوباره اجرا کن:')
print('   python -m pipelines.facts.load_fact_treasury')