from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
import logging
from pyspark.sql.types import *
from pyspark.sql.window import Window


class WordBankIngest:

    def __init__(self) -> None:

        self.spark = SparkSession.builder.appName('').master('local').getOrCreate()

        self.input_file = '../../../input_data/raw/world_bank_countries.json'
        self.output_file = '../../../input_data/silver/world_bank_countries'

        self.gdp_data = '../../../input_data/raw/GEPCSV.csv'
        self.invoice_data = '../../../input_data/raw/invoices.json'
        self.game_file = '../../../input_data/raw/keystrokes-for-tech-test.csv'

        formatter = '%(levelname)s : %(filename)s : %(lineno)d : %(message)s'
        logging.basicConfig(level=logging.INFO, format=formatter)
        self.log = logging.getLogger('logger')
        

    def get_schema(self) -> str:
        self.log.info(f'returning word bank json schema')
        return """id string, iso2Code string, name string, 
        region struct<id string, iso2code string, value string>, 
        adminregion struct<id string, iso2code string, value string>, 
        incomeLevel struct<id string, iso2code string, value string>,
        lendingType struct<id string, iso2code string, value string>, 
        capitalCity string, longitude string, latitude string"""

    def get_invoice_schema(self) -> str:
        return """
        InvoiceNumber string,CreatedTime bigint,StoreID string,PosID string,CashierID string,CustomerType string,
        CustomerCardNo string,TotalAmount double,NumberOfItems bigint,PaymentMethod string,TaxableAmount double,
        CGST double,SGST double,CESS double,DeliveryType string,
        DeliveryAddress struct<AddressLine string,City string,State string,PinCode string,ContactNumber string>,
        InvoiceLineItems array<struct<ItemCode string,ItemDescription string,ItemPrice double,ItemQty bigint,TotalValue double>>
        """

    def get_json_schema(self) -> StructType:
        return StructType([
            StructField("seqNum", StringType(), True),
            StructField("matchTime", StringType(), True),
            StructField("timestamp", StringType(), True),
            StructField("server", StructType([StructField("team", StringType())])),
            StructField("nextServer", StructType([StructField("team", StringType())])),
            StructField("score",  StructType([
                StructField("currentSetScore", StructType([
                    StructField("gamesA", IntegerType(), True),
                    StructField("gamesB", IntegerType(), True),
                ])),
                StructField("currentGameScore", StructType([
                    StructField("pointsA", StringType(), True),
                    StructField("pointsB", StringType(), True),
                    StructField("gameType", StringType(), True),
                ])),
                StructField("previousSetsScore", StructType([])),
                StructField("details", StructType([
                    StructField("scoredBy", StringType(), True),
                    StructField("pointType", StringType(), True),
                ])),
            ])),

            StructField("matchStatus", StructType([
                StructField("umpire", StringType(), True),
                StructField("numSets", IntegerType(), True),
                StructField("courtNum", IntegerType(), True),
                StructField("matchState", StructType([
                    StructField("state", StringType(), True),
                    StructField("locationTimestamp", StringType(), True)
                ])),
                StructField("tossWinner", StringType(), True),
                StructField("umpireCode", StringType(), True),
                StructField("firstServer", StringType(), True),
                StructField("scoringType", StringType(), True),
                StructField("tossChooser", StringType(), True),
                StructField("teamAPlayer1", StringType(), True),
                StructField("teamBPlayer1", StringType(), True),
                StructField("tieBreakType", StringType(), True),
                StructField("umpireCountry", StringType(), True),
                StructField("teamAPlayersDetails", StructType([
                    StructField("player1Id", StringType(), True),
                    StructField("player1Country", StringType(), True)
                ])),
                StructField("teamBPlayersDetails", StructType([
                    StructField("player1Id", StringType(), True),
                    StructField("player1Country", StringType(), True)
                ]))
            ])),
            StructField("eventElementType", StringType(), True)
        ])

    def read_data(self) -> DataFrame:
        data = self.spark.read.format("json").schema(self.get_schema()).load(self.input_file)
        data.printSchema()
        data1 = data.select(f.col("id").alias('country_id'),
                            f.col("iso2Code").alias('iso2_code'),
                            f.col("name").alias('country_name'),
                            f.col("region.id").alias("region_id"),
                            f.col("region.iso2code").alias("region_iso2_code"),
                            f.col("region.value").alias("region_value"),
                            f.col("adminregion.id").alias("admin_region_id"),
                            f.col("adminregion.iso2code").alias("admin_region_iso2code"),
                            f.col("adminregion.value").alias("admin_region_value"),
                            f.col("incomeLevel.id").alias("income_level_id"),
                            f.col("incomeLevel.iso2code").alias("income_level_iso2code"),
                            f.col("incomeLevel.value").alias("income_level_value"),
                            f.col("lendingType.id").alias("lending_type_id"),
                            f.col("lendingType.iso2code").alias("lending_type_iso2code"),
                            f.col("lendingType.value").alias("lending_type_value"),
                            f.col("capitalCity").alias('capital_city'),
                            f.col("longitude"),
                            f.col("latitude"))
        data1.printSchema()
        data1.show()

        country_data = data1.select(f.col('country_id'),
                            f.col('iso2_code'),
                            f.col('country_name'),
                            f.col("region_id"),
                            f.col("admin_region_id"),
                            f.col("income_level_id"),
                            f.col("lending_type_id"),
                            f.col('capital_city'),
                            f.col("longitude"),
                            f.col("latitude")).drop_duplicates()
        region_data = data1.select(f.col("region_id"), f.col("region_iso2_code"), f.col("region_value")).drop_duplicates()
        admin_data = data1.select(f.col("admin_region_id"), f.col("admin_region_iso2code"),
                                  f.col("admin_region_value")).drop_duplicates()
        income_data = data1.select(f.col("income_level_id"), f.col("income_level_iso2code"),
                                  f.col("income_level_value")).drop_duplicates()
        lending_data = data1.select(f.col("lending_type_id"), f.col("lending_type_iso2code"),
                                   f.col("lending_type_value")).drop_duplicates()

        region_data.show()
        admin_data.show()
        income_data.show()
        lending_data.show()
        country_data.show()
        return data1

    def read_csv_data(self) -> DataFrame:
        gdp_data = self.spark.read.csv(self.gdp_data, header=True, inferSchema=True)
        gdp_data.printSchema()
        gdp_data.show()

        gdp_data1 = gdp_data.withColumn("year_gdp_map",
            f.create_map(f.lit("2021"), f.col("2021"), f.lit("2022"), f.col("2022"), f.lit("2023"), f.col("2023"),
                         f.lit("2024"), f.col("2024"), f.lit("2025"), f.col("2025"), f.lit("2026"), f.col("2026"))
        )
        gdp_data1.show()
        gdp_data2 = gdp_data1.select(
            f.col('Country Name'), f.col('Country Code'), f.col('Indicator Name'), f.col('Indicator Code'),
            f.explode(f.col('year_gdp_map')).alias('year', 'gdp'))
        gdp_data2.show()
        return gdp_data

    def camel_to_snake(self, col_name):
        return "".join(['_' + char if char.isupper() else char for char in col_name]).lstrip('_').lower()

    def read_invoice_data(self) -> DataFrame:
        invoice = self.spark.read.format("json").schema(self.get_invoice_schema()).load(self.invoice_data)

        invoice = invoice.toDF(*[self.camel_to_snake(col) for col in invoice.columns])

        invoice.printSchema()
        invoice.show()

        invoice1 = invoice.select(f.col('invoice_number'),
                                  f.col('created_time'),
                                  f.col('store_i_d').alias('store_id'),
                                  f.col('pos_i_d').alias('pos_id'),
                                  f.col('cashier_i_d').alias('cashier_id'),
                                  f.col('customer_type'), f.col('customer_card_no'),
                                  f.col('total_amount'), f.col('number_of_items'), f.col('payment_method'),
                                  f.col('taxable_amount'),
                                  f.col('c_g_s_t').alias('cgst'),
                                  f.col('s_g_s_t').alias('sgst'),
                                  f.col('c_e_s_s').alias('cess'),
                                  f.col('delivery_type'),
                                  f.col('delivery_address.AddressLine').alias('addressline'),
                                  f.col('delivery_address.City').alias('city'),
                                  f.col('delivery_address.State').alias('state'),
                                  f.col('delivery_address.PinCode').alias('pincode'),
                                  f.col('delivery_address.ContactNumber').alias('contactnumber'),
                                  f.explode(f.col('invoice_line_items')).alias('line_item')
                                  ) \
            .withColumn('item_code', f.col('line_item.ItemCode')) \
            .withColumn('item_description',f.col('line_item.ItemPrice')) \
            .withColumn('item_price', f.col('line_item.ItemPrice')) \
            .withColumn('item_qty', f.col('line_item.ItemQty')) \
            .withColumn('total_value', f.col('line_item.TotalValue')) \
            .drop('line_item')
        invoice1.printSchema()
        invoice1.show()

        # Define time window
        time_window = Window.orderBy(f.col("created_time")).rangeBetween(-60000,
                                                                         0)  # 1-hour window ending at the current row

        # Aggregation using window function
        aggregated_df = invoice1.withColumn("window_total_amount", f.sum("total_value").over(time_window)) \
            .withColumn("window_invoice_count", f.count("invoice_number").over(time_window)) \
            .withColumn("time_value", f.from_unixtime(f.col("created_time")/f.lit(1000)))

        aggregated_df.show(100)
        aggregated_df.select(f.max('time_value'), f.min('time_value')).show()

        # Perform aggregation over a sliding window
        windowed_df = aggregated_df.groupBy(f.window("time_value", "2 minutes", "1 minutes")) \
            .agg(
            f.sum("total_value").alias("total_sales"),
            f.count("invoice_number").alias("invoice_count")
        ).orderBy(f.col('window'))

        windowed_df.show(100, truncate=False)

        return invoice

    def read_game_data(self) -> DataFrame:
        game = self.spark.read.csv(self.game_file, inferSchema=True, header=True)
        game.printSchema()
        print(game.columns)
        parsed_df = game.withColumn("parsed_json", f.from_json(f.col("match_element"), self.get_json_schema()))
        parsed_df.printSchema()
        print(parsed_df.columns)
        parsed_df.show()
        flattened_df = parsed_df.select(
            f.col("row_num"),
            f.col("match_id"),
            f.col("message_id"),
            f.col("parsed_json.seqNum").alias("seq_num"),
            f.col("parsed_json.matchTime").alias("match_time"),
            f.col("parsed_json.timestamp").alias("timestamp"),
            f.col("parsed_json.matchStatus.umpire").alias("umpire"),
            f.col("parsed_json.matchStatus.numSets").alias("num_sets"),
            f.col("parsed_json.matchStatus.courtNum").alias("court_num"),
            f.col("parsed_json.matchStatus.matchState.state").alias("match_state"),
            f.col("parsed_json.matchStatus.matchState.locationTimestamp").alias("location_timestamp"),
            f.col("parsed_json.matchStatus.teamAPlayersDetails.player1Id").alias("team_a_player1_id"),
            f.col("parsed_json.matchStatus.teamBPlayersDetails.player1Id").alias("team_b_player1_id"),
            f.col("parsed_json.eventElementType"),
            f.col("parsed_json.server.team").alias('server_team'),
            f.col("parsed_json.score.currentSetScore.gamesA").alias('current_score_game_a'),
            f.col("parsed_json.score.currentSetScore.gamesB").alias('current_score_game_b'),
            f.col("parsed_json.score.currentGameScore.pointsA").alias('current_score_point_a'),
            f.col("parsed_json.score.currentGameScore.pointsB").alias('current_score_point_b'),
            f.col("parsed_json.score.currentGameScore.gameType").alias('current_score_game_type'),
            f.col("parsed_json.score.details.scoredBy").alias('details_scored_by'),
            f.col("parsed_json.score.details.pointType").alias('details_point_by'),
        )
        flattened_df.printSchema()
        print(flattened_df.columns)
        flattened_df.show(100)
        new_data = flattened_df.select(f.col('umpire'), f.col('num_sets'), f.col('court_num'), f.col('match_state'),
                            f.col('team_a_player1_id'), f.col('team_b_player1_id')).drop_duplicates()

        # new_data.show(50)
        # flattened_df.describe().show()
        flattened_df.select('eventElementType').drop_duplicates().show()
        flattened_df.select('current_score_game_type').drop_duplicates().show()

        match_data = flattened_df.select(f.col('match_id'), f.col('eventElementType'), f.col('server_team'),
                                         f.col('current_score_game_type'), f.col('match_time'), f.col('current_score_game_a'),
                                         f.col('current_score_game_b'), f.col('current_score_point_a'),
                                         f.col('current_score_point_b')) \
            .filter((f.col('eventElementType') == f.lit('PointScored')) & (f.col('match_id') == f.lit(29304)))
        match_data.drop_duplicates().orderBy(f.col('match_time')).show(100)

        flattened_df.filter((f.col('match_id') == f.lit(29304)) &
                            (f.col('match_time') >= f.lit('00:31:27')) &
                            (f.col('match_time') <= f.lit('00:34:56'))).show(truncate=False)

        return game

    def main(self):
        # country_d = self.read_data()
        # gdp_df = self.read_csv_data()
        invoice_df = self.read_invoice_data()
        # game_df = self.read_game_data()


if __name__ == '__main__':
    wbi = WordBankIngest()
    wbi.main()