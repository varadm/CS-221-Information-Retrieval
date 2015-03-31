package edu.uci.ics.cs221.project3.conf

/**
 * @author varadmeru
 *
 */
object Config {
  // Spark configurations
  val SPARK_HOME = "/Users/varadmeru/research/spark-stuff/spark-training/spark";
  val MASTER = "local[20]";
  val APP_NAME = "SimpleApp";
  
  // Cassandra Configurations
  val CASSANDRA_HOST_VALUE = "127.0.0.1"
  val CASSANDRA_NATIVE_PORT_VALUE = "9042"
  val CASSANDRA_RPC_PORT_VALUE = "9160"
  val CASSANDRA_HOST = "spark.cassandra.connection.host"
  val CASSANDRA_RPC_PORT = "spark.cassandra.connection.rpc.port"
  val CASSANDRA_NATIVE_PORT = "spark.cassandra.connection.native.port"
  
  val CASSANDRA_KEYSPACE = "9160"
}