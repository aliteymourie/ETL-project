import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / 'mother data base guide'
OUT_DIR = ROOT / 'warehouse_tables' / 'generated'

TYPE_MAP = {
    'int': 'INTEGER',
    'bigint': 'BIGINT',
    'decimal': 'NUMERIC',
    'numeric': 'NUMERIC',
    'float': 'DOUBLE PRECISION',
    'datetime': 'TIMESTAMP',
    'date': 'DATE',
    'text': 'TEXT',
}


def map_column_type(col_meta: dict) -> str:
    # try several reasonable keys
    if not isinstance(col_meta, dict):
        return 'TEXT'
    max_len = col_meta.get('max_length') or col_meta.get('length')
    dtype = col_meta.get('data_type') or col_meta.get('type') or col_meta.get('sql_type')
    if max_len:
        try:
            ml = int(max_len)
            return f'VARCHAR({ml})'
        except Exception:
            pass
    if dtype:
        d = str(dtype).lower()
        for k, v in TYPE_MAP.items():
            if k in d:
                return v
    return 'TEXT'


def generate_create_table(table_name: str, table_meta: dict) -> str:
    cols = table_meta.get('columns', {}) or {}
    pks = table_meta.get('primary_keys', []) or []

    col_lines = []
    if not cols:
        # fallback: create an id and raw JSON column
        col_lines.append('id SERIAL PRIMARY KEY')
        col_lines.append("raw JSONB")
    else:
        for col_name, meta in cols.items():
            sql_type = map_column_type(meta)
            col_lines.append(f'"{col_name}" {sql_type}')
    pk_clause = ''
    if pks:
        pk_cols = ', '.join([f'"{c}"' for c in pks])
        pk_clause = f', PRIMARY KEY ({pk_cols})'

    cols_sql = ',\n    '.join(col_lines)
    ddl = f'CREATE TABLE IF NOT EXISTS public."{table_name}" (\n    {cols_sql}{pk_clause}\n);'
    return ddl


def process_schema_file(path: Path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f'Failed to parse {path}: {e}')
        return

    statements = []
    # support top-level dict (usual) or list of dicts
    if isinstance(data, dict):
        items = list(data.items())
    elif isinstance(data, list):
        items = []
        for elem in data:
            if isinstance(elem, dict):
                # merge dict entries
                for k, v in elem.items():
                    items.append((k, v))
    else:
        print(f'Unsupported JSON structure in {path}, skipping.')
        return

    for table_name, table_meta in items:
        try:
            ddl = generate_create_table(table_name, table_meta)
            statements.append(ddl)
        except Exception as e:
            print(f'Failed to generate DDL for {table_name} in {path}: {e}')
            continue

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUT_DIR / f'{path.stem}_create.sql'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(statements))
    print(f'Wrote {out_file}')


def main():
    json_files = [p for p in SCHEMA_DIR.glob('*.json')]
    if not json_files:
        print('No schema JSON files found in', SCHEMA_DIR)
        return
    for jf in json_files:
        process_schema_file(jf)


if __name__ == '__main__':
    main()
