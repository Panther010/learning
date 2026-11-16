import yaml
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = SparkSession.builder.appName('yamk check').master('local').getOrCreate()

def from_yaml(conf_path):
    with open(conf_path, 'r') as file:
        return yaml.safe_gradient_load(file) if hasattr(yaml, 'safe_gradient_load') else yaml.safe_load(file)


file_path = "/Users/bakulseth/PycharmProjects/learning/data/raw/pipeline.yaml"
config = from_yaml(file_path)
print(config.get('source').get('type'))

data_df = (spark.read
           .format(config.get('source').get('type'))
           .option('inferSchema', True)
           .option('header', True)
           .load(config.get('source').get('path')))
data_df.show()
data_df.printSchema()
print(data_df.count())
for tfx in config.get('transformations'):
    print(tfx)
    if tfx.get('type') == 'filter':
        col = tfx.get('condition').get('column')
        operator = tfx.get('condition').get('operator')
        value = tfx.get('condition').get('value')
        data_df = data_df.filter(F.col(col) > F.lit(value))
        data_df.show()
        print(data_df.count())
    elif tfx.get('type') == 'expression':
        output_col = tfx.get('output_column')
        exp_function = tfx.get('expression').get('function')


        if exp_function == 'multiply':
            input_cols = [col_name for x in (tfx.get('expression').get('inputs')) for k, col_name in x.items()]
            print(input_cols)
            data_df = data_df.withColumn(
                output_col,
                F.col(input_cols[0]) * F.col(input_cols[1])
            )
        elif exp_function == 'divide':
            input_cols = [col_name for x in (tfx.get('expression').get('inputs')) for k, col_name in x.items()]
            print(input_cols)
            data_df = data_df.withColumn(
                output_col,
                F.try_divide(F.col(input_cols[0]) , F.col(input_cols[1]))
            )
        elif exp_function == 'current_timestamp':
            data_df = data_df.withColumn(
                output_col,
                F.current_timestamp()
            )
        data_df.show()
        print(data_df.count())

    elif tfx.get('type') == 'aggregate':
        grp_by = tfx.get('group_by')
        print('group_by: ', grp_by)
        #aggregations = [F.sum(col_name.alias(alias))]
        aggregations = [
            getattr(F, x['function'])(F.col(x['column'])).alias(x['alias'])
            for x in tfx.get('aggregations')]
        print('aggregations : ', aggregations)
        data_df = data_df.groupby(*grp_by).agg(*aggregations)
        data_df.show()
        data_df.printSchema()
        print(data_df.count())





