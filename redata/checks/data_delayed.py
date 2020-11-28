from redata.db_operations import metrics_db, source_db, metadata

def check_data_delayed(table, time_column, time_type):
    result = source_db.execute(f"""
        SELECT 
            EXTRACT (epoch from now() - max({time_column}))
        FROM {table}
    """).fetchall()[0]

    metrics_data_delay = metadata.tables['metrics_data_delay']

    stmt = metrics_data_delay.insert().values(
        table_name=table,
        value=result[0]
    )
    metrics_db.execute(stmt)
