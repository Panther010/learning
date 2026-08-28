data1 = {'topic': 'OLTP vs OLAP', 'post': 'OLTP (Online Transaction Processing):\n- Is used for live transactional system where we need to access data in high concurrency low latency mode.\n- To achieve this Milliseconds latency and high concurrency operations. It is preferred to have data is highly normalised (3rd normal form)\n- Data remained stored in row-oriented format 8-16 KB to get entire results in one read\n- Fast read, write and update are required. Vertical scaling.\n- Priority remains low latency and write integrity. Build around strict ACID compliance\n\nOLAP (Online Analytical Processing)\n- It is used for complex analytical aggregations with historical data.\n- Read heavy: read huge amount of data with higher latency. It is expected to have denormalized(Star Schema/ Snowflake Schema/ Wide Tables)\n- Data remained in columnar format (Parquet or Delta), This columnar storage help high compression, High I/O savings.\n- Scanning huge amount of data latency remain seconds to minutes. Scale horizontally.\n- Priority remains high throughput read performance\n\nIn modern data word these 2 system communicate with each other using CDC Change Data Capture(CDC) and ETL/ELT', 'core_concept': 'OLTP prioritizes low-latency, high-concurrency row storage; OLAP prioritizes high-throughput, read-heavy columnar storage.', 'hook': 'OLTP (Online Transaction Processing):', 'angle': 'Informative', 'tags': ['OLTP', 'OLAP', 'CDC']}
data2 = {'oltp_vs_olap.txt': {'topic': 'OLTP vs OLAP', 'post': 'OLTP (Online Transaction Processing):\n- Is used for live transactional system where we need to access data in high concurrency low latency mode.\n- To achieve this Milliseconds latency and high concurrency operations. It is preferred to have data is highly normalised (3rd normal form)\n- Data remained stored in row-oriented format 8-16 KB to get entire results in one read\n- Fast read, write and update are required. Vertical scaling.\n- Priority remains low latency and write integrity. Build around strict ACID compliance\n\nOLAP (Online Analytical Processing)\n- It is used for complex analytical aggregations with historical data.\n- Read heavy: read huge amount of data with higher latency. It is expected to have denormalized(Star Schema/ Snowflake Schema/ Wide Tables)\n- Data remained in columnar format (Parquet or Delta), This columnar storage help high compression, High I/O savings.\n- Scanning huge amount of data latency remain seconds to minutes. Scale horizontally.\n- Priority remains high throughput read performance\n\nIn modern data word these 2 system communicate with each other using CDC Change Data Capture(CDC) and ETL/ELT', 'core_concept': 'OLTP prioritizes low-latency, high-concurrency row storage; OLAP prioritizes high-throughput, read-heavy columnar storage.', 'hook': 'OLTP (Online Transaction Processing):', 'angle': 'Informative', 'tags': ['OLTP', 'OLAP', 'CDC']}}


print("data1", type(data1))
print(data1)

print("data2", type(data2))
print(data2)

for key, value in data1.items():
    print(key)
print("++++++++++++++++++++")
for key, value in data2.items():
    print(key.replace("_", " ").replace(".txt", ""))

print(data2["oltp_vs_olap.txt"])