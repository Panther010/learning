from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import *
from pyspark.sql.window import Window

def main():
    spark = SparkSession.builder.appName("test_prep").master("local").getOrCreate()

    flight = spark.read.option("header", True).option("inferSchema", True).csv("/Users/bakulseth/PycharmProjects/learning/data/raw/flight/flightData.csv")
    passengers = spark.read.option("header", True).option("inferSchema", True).csv("/Users/bakulseth/PycharmProjects/learning/data/raw/flight/passengers.csv")

    flight.printSchema()
    passengers.printSchema()


    result1 = flight.alias("f").groupby(
        F.col("f.passengerId")
    ).agg(
        F.count(F.col("f.flightId")).alias("flight_count")
    ).join(
        passengers.alias("p"),
        F.col("f.passengerId") == F.col("p.passengerId"),
        "left"
    ).orderBy(
        F.col("flight_count").desc()
    )

    # result1.show(5)

    result2 = passengers.alias("p").join(
        flight.alias("f"),
        F.col("p.passengerId") == F.col("f.passengerId"),
        "left"
    ).filter(
        F.col("f.passengerId").isNull()
    )

    # result2.show()

    result3 = flight.groupby(
        F.col("from"),
        F.col("to")
    ).agg(
        F.count(F.col("passengerId")).alias("passenger_count")
    ).orderBy(
        F.col("passenger_count").desc()
    )

    # result3.show()

    result_check = flight.groupBy(
        F.col("from"),
        F.col("to"),
        F.col("passengerId")
    ).agg(
        F.count("flightId").alias("flight_count")
    ).orderBy(
        F.col("flight_count").desc()
    )

    # result_check.show()

    window_spec = Window.partitionBy(F.col("from"), F.col("to")).orderBy(F.col("flight_count").desc())

    result4 = result_check.select(
        F.col("*"),
        F.rank().over(window_spec).alias("rn")
    )

    # result4.show()

    invoice_df = spark.read.json("/Users/bakulseth/PycharmProjects/learning/data/raw/invoices.json")
    invoice_df.printSchema()
    invoice_df.show(truncate=False)

    address_schema = StructType([
        StructField("AddressLine", StringType()),
        StructField("City", StringType()),
        StructField("State", StringType()),
        StructField("PinCode", StringType()),
        StructField("ContactNumber", StringType())
    ])

    invoice_line_schema = StructType([
        StructField("ItemCode", StringType()),
        StructField("ItemDescription", StringType()),
        StructField("ItemPrice", DoubleType()),
        StructField("ItemQty", LongType()),
        StructField("TotalValue", DoubleType()),
    ])
    invoice_schema = StructType([
        StructField("InvoiceNumber", StringType()),
        StructField("CreatedTime", LongType()),
        StructField("StoreID", StringType()),
        StructField("PosID", StringType()),
        StructField("CashierID", StringType()),
        StructField("CustomerType", StringType()),
        StructField("CustomerCardNo", StringType()),
        StructField("TotalAmount", DoubleType()),
        StructField("NumberOfItems", LongType()),
        StructField("PaymentMethod", StringType()),
        StructField("TaxableAmount", DoubleType()),
        StructField("CGST", DoubleType()),
        StructField("SGST", DoubleType()),
        StructField("CESS", DoubleType()),
        StructField("DeliveryType", StringType()),
        StructField("DeliveryAddress", address_schema),
        StructField("InvoiceLineItems", ArrayType(invoice_line_schema))
    ])

    invoice_df = spark.read.schema(invoice_schema).json("/Users/bakulseth/PycharmProjects/learning/data/raw/invoices.json")
    invoice_df.printSchema()

    invoice_result1 = invoice_df.groupBy(
        F.col("StoreID")
    ).agg(
        F.sum("TotalAmount").alias("total_revenue")
    ).filter(
        F.col("total_revenue") > F.lit(50000)
    )

    # print(invoice_result1.count())

    invoice_result4 = invoice_df.select(
        F.col("*"),
        F.col("DeliveryAddress.AddressLine"),
        F.col("DeliveryAddress.City"),
        F.col("DeliveryAddress.State"),
        F.col("DeliveryAddress.PinCode"),
        F.col("DeliveryAddress.ContactNumber")
    )

    # invoice_result4.show()

    invoice_result2 = invoice_df.select(
        F.col("*"),
        F.explode(F.col("InvoiceLineItems")).alias("invoice_line_item")
    ).drop(
        F.col("InvoiceLineItems")
    ).select(
        F.col("*"),
        F.col("invoice_line_item.ItemCode"),
        F.col("invoice_line_item.ItemDescription"),
        F.col("invoice_line_item.ItemQty")
    ).groupby(
        F.col("ItemCode"),
        F.col("ItemDescription")
    ).agg(
        F.count("ItemQty").alias("sold_count")
    ).orderBy(
        F.col("sold_count").desc()
    )

    # invoice_result2.show(truncate=False)

    win_spec2 = Window.partitionBy(F.col("CustomerCardNo")).orderBy(F.col("event_time").desc())

    invoice_result3 = invoice_df.withColumn(
        "event_time",
        (F.col("CreatedTime")/1000).cast(TimestampType())
    ).select(
        F.col("*"),
        F.rank().over(win_spec2).alias("rn")
    ).filter(
        F.col("rn") != F.lit(1)
    )
    invoice_result3.show()


if __name__ == "__main__":
    main()