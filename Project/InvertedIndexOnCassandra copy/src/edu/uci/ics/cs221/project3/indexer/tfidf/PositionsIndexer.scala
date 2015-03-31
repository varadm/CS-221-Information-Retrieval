package edu.uci.ics.cs221.project3.indexer.tfidf

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.rdd.PairRDDFunctions
import com.datastax.spark.connector._

import edu.uci.ics.cs221.project3.conf.Config
import edu.uci.ics.cs221.project3.stemmer.PorterStemmer
import edu.uci.ics.cs221.project3.sparkmanager.SparkAccessObject

object PositionIndexer {

  // Spark Configuration with the custom configurations
  val sc = SparkAccessObject.getSparkContext()

  def createPositionIndexOnText() = {
    // Read the Cassandra table
    val tab = sc.cassandraTable("finder_keyspace", "finder_corpus")
    val idTextRDD = tab.select("url_id", "page_text")

    val idTextProjectionTableRDD = idTextRDD.map {
      cassandraRow => (cassandraRow.get[Int]("url_id"), cassandraRow.get[String]("page_text"))
    }
    val totalNumberOfDocuments = idTextProjectionTableRDD.count()

    val finalRDD = idTextProjectionTableRDD
      .flatMap {
        case (urlId, pageText) => pageText.split("""\W+""")
          .zipWithIndex
          .map { case (word, index) => (word.toLowerCase(), index) }
          .filter { case (word, index) => !word.isEmpty() }
          .map { case (word, index) => (word, urlId, index) }
      }.map {
        case (word, urlId, index) => (word, (urlId, index))
      }.groupBy {
        case (word, (urlId, index)) => word
      }
    val finalRDD1 = finalRDD.map {
      case (word, listOfPosition) => (word, listOfPosition.toList.map(tuple => tuple._2))
    }.map {
      case (word, listOfPosition) => (word, listOfPosition.groupBy {
        case (urlid, position) => urlid
      })
    }

    val finalRDD2 = finalRDD1.map {
      case (word, listOfPosition) => (word, listOfPosition.toMap.map {
        case (one, two) => (one, two.map {
          case (three, four) => four.toString()
        })
      })
    }.map {
      case (word, someMap) => (word, someMap.map {
        case (key, value) => (key, value.mkString(","))
      })
    }

    finalRDD2.saveToCassandra("finder_keyspace", "positions_index", SomeColumns("token_text", "positions_map"))
  }
}