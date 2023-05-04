from pymilvus import connections, CollectionSchema, FieldSchema, DataType, Collection, utility

# 连接数据库
connections.connect(alias="default", user='minioadmin', password='minioadmin', host='localhost', port='19530')

# 创建集合
people_id = FieldSchema(
    name='id', dtype=DataType.INT64, is_primary=True
)
people_name = FieldSchema(
    name='name', dtype=DataType.VARCHAR, max_length=200
)
people_metrics = FieldSchema(
    name='metrics', dtype=DataType.FLOAT_VECTOR, dim=3
)
schema = CollectionSchema(fields=[people_id, people_name, people_metrics])
collection = Collection(name='people', schema=schema, using='default', shards_num=2)

# 插入数据
data = [
    [1, 2, 3, 4, 5, 6],
    ['小明','小月','小王','小李','小张','小赵'],
    [[1.8, 75, 25],[1.75, 70, 24],[1.8, 80, 28],[1.78, 78, 30],[1.75, 70, 23],[1.8, 76, 29]]
]
mr = collection.insert(data)
collection.flush()

# 创建索引
index_params = {
    "metric_type":"L2", # L2:欧式距离, IP:向量内积
    "index_type":"FLAT",
    "params":{ }
}
collection.create_index(
    field_name='metrics', 
    index_params=index_params
)

# 查询数据
collection.load()
search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
results = collection.search(
    data=[[1.75, 72, 24]],
    anns_field="metrics", 
    param=search_params,
    limit=10, 
    expr=None,
    output_fields=['id','name'],
    consistency_level="Strong"
)
print(results)
