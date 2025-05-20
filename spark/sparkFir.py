#coding:utf8

#导包
from pyspark.sql import SparkSession
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.types import StructType,StructField,IntegerType,StringType,FloatType


if __name__ == '__main__':
    #构建
    spark = SparkSession.builder.appName("sparkSQL").master("local[*]").\
        config("spark.sql.shuffle.partitions",2).\
        config("spark.sql.warehouse.dir","hdfs://node1:8020/user/hive/warehouse").\
        config("hive.metastore.uris","thrift://node1:9083").\
        enableHiveSupport().\
        getOrCreate()

    #
    sc = spark.sparkContext

    #构建df
    schema = StructType().add("type",StringType(),nullable=True). \
        add("title", StringType(), nullable=True). \
        add("companyTitle", StringType(), nullable=True). \
        add("minSalary", IntegerType(), nullable=True). \
        add("maxSalary", IntegerType(), nullable=True). \
        add("workExperience", StringType(), nullable=True). \
        add("education", StringType(), nullable=True). \
        add("totalTag", StringType(), nullable=True). \
        add("companyPeople", StringType(), nullable=True). \
        add("workTag", StringType(), nullable=True). \
        add("welfare", StringType(), nullable=True). \
        add("imgSrc", StringType(), nullable=True). \
        add("city", StringType(), nullable=True)

    #形成
    df = spark.read.format("csv").\
        option("sep",","). \
        option("quote", '"'). \
        option("escape", '"'). \
        option("header", True).\
        option("encoding", "utf-8").\
        schema(schema=schema).\
        load("./jobData.csv")

    #数据清洗
    df.drop_duplicates()

    df = df.withColumn("id",monotonically_increasing_id())


    df.show()

    #sql
    df.write.mode("overwrite").\
        format("jdbc").\
        option("url","jdbc:mysql://node1:3306/bigdata?useSSL=false&useUnicode=true&charset=utf8").\
        option("dbtable","jobData").\
        option("user","root").\
        option("password","root").\
        option("encoding","utf-8").\
        save()

    df.write.mode("overwrite").saveAsTable("jobData","parquet")
    spark.sql("select * from jobData").show()


