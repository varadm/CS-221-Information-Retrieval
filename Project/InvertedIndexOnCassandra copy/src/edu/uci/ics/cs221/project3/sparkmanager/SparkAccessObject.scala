package edu.uci.ics.cs221.project3.sparkmanager

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.rdd.PairRDDFunctions
import com.datastax.spark.connector._

import edu.uci.ics.cs221.project3.conf.Config

object SparkAccessObject {
  val conf = new SparkConf(true)
    .setSparkHome(Config.SPARK_HOME)
    .setMaster(Config.MASTER)
    .setAppName(Config.APP_NAME)
    .setJars(SparkContext.jarOfClass(this.getClass).toList)
    .set(Config.CASSANDRA_HOST, Config.CASSANDRA_HOST_VALUE)
    .set(Config.CASSANDRA_NATIVE_PORT, Config.CASSANDRA_NATIVE_PORT_VALUE)
    .set(Config.CASSANDRA_RPC_PORT, Config.CASSANDRA_RPC_PORT_VALUE)

  val sc = new SparkContext(conf)

  def getSparkContext(): SparkContext = {
    return sc
  }

  def closeSparkContext(): Unit = {
    return sc.stop()
  }
}