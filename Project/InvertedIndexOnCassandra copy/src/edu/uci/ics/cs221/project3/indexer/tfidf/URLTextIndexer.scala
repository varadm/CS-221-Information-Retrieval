package edu.uci.ics.cs221.project3.indexer.tfidf

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.rdd.PairRDDFunctions
import com.datastax.spark.connector._

import io.mola.galimatias.URL

import edu.uci.ics.cs221.project3.conf.Config
import edu.uci.ics.cs221.project3.sparkmanager.SparkAccessObject

object URLTextIndexer {
  // Spark Configuration with the custom configurations
  val sc = SparkAccessObject.getSparkContext()

  def main(args: Array[String]): Unit = {
    createURLTextIndex()
  }

  def createURLTextIndex() = {
    val tab = sc.cassandraTable("finder_keyspace", "finder_corpus")
    val idURLRDD = tab.select("url_id", "url")
    val urlIdURLRDD = idURLRDD.map {
      cassandraRow => (cassandraRow.get[Int]("url_id"), cassandraRow.get[String]("url"))
    }
    val totalNumberOfDocuments = urlIdURLRDD.count()

    val parsedUrlRDD = urlIdURLRDD.map { case (urlId, url) => (urlId, url.toLowerCase()) }
      .map { case (urlId, url) => (urlId, URL.parse(url)) }

    val authorityTokensRDD = new PairRDDFunctions(parsedUrlRDD.flatMap {
      case (urlId, url) => url.authority().split("""\W+""")
        .map { case (word) => (word.toLowerCase()) }
        .map { case (word) => (word, urlId) }
    }.map {
      case (word, urlId) => ((word, urlId), 2)
    }).reduceByKey {
      case (sumFromLeft, count) => sumFromLeft + count
    }.map {
      case ((word, urlId), count) => (word, (urlId, count))
    }.groupBy {
      case (word, (urlId, count)) => word
    }
    
    val pathTokensRDD = new PairRDDFunctions(parsedUrlRDD.flatMap {
      case (urlId, url) => url.path().split("""\W+""")
        .map { case (word) => (word.toLowerCase()) }
        .map { case (word) => (word, urlId) }
    }.map {
      case (word, urlId) => ((word, urlId), 1)
    }).reduceByKey {
      case (sumFromLeft, count) => sumFromLeft + count
    }.map {
      case ((word, urlId), count) => (word, (urlId, count))
    }.groupBy {
      case (word, (urlId, count)) => word
    }
    
    val authorityTokensPairRDD = new PairRDDFunctions(authorityTokensRDD)
    authorityTokensPairRDD.join(pathTokensRDD).saveAsTextFile("/Users/varadmeru/url_indexer")
    
//    authorityTokensPairRDD.reduceByKey {
//      case (word, value) => word
//    }.map {
//      case ((word, urlId), count) => (word, (urlId, count))
//    }.groupBy {
//      case (word, (urlId, count)) => word
//    }

    /* val authorityTokensRDD = new PairRDDFunctions(parsedUrlRDD.flatMap {
      case (urlId, url) => url.authority().split("""\W+""")
        .map { case (word) => (word.toLowerCase()) }
        .map { case (word) => (word, urlId) }
    }.map {
      case (word, urlId) => ((word, urlId), 2)
    }).reduceByKey {
      case (sumFromLeft, count) => sumFromLeft + count
    }.map {
      case ((word, urlId), count) => (word, (urlId, count))
    }.groupBy {
      case (word, (urlId, count)) => word
    }.map {
      case tupleWordUrlIdCount =>
        (tupleWordUrlIdCount._1, // Token
          tupleWordUrlIdCount._2.toList.map(_._2).map(_._2).sum, // Collection Frequency
          math.log(totalNumberOfDocuments / tupleWordUrlIdCount._2.toList.size), // IDF
          tupleWordUrlIdCount._2.toList.map(tupleUrlIdCount => tupleUrlIdCount._2).toMap,
          tupleWordUrlIdCount._2.toList.map(tupleUrlIdCount =>
            (tupleUrlIdCount._2._1, math.log(tupleUrlIdCount._2._2 + 1) * math.log(totalNumberOfDocuments / tupleWordUrlIdCount._2.toList.size))).toMap)
    }
    * 
    * 
    * 
    *val pathTokensRDD = new PairRDDFunctions(parsedUrlRDD.flatMap {
      case (urlId, url) => url.path().split("""\W+""")
        .map { case (word) => (word.toLowerCase()) }
        .map { case (word) => (word, urlId) }
    }.map {
      case (word, urlId) => ((word, urlId), 1)
    }).reduceByKey {
      case (sumFromLeft, count) => sumFromLeft + count
    }.map {
      case ((word, urlId), count) => (word, (urlId, count))
    }.groupBy {
      case (word, (urlId, count)) => word
    }.map {
      case tupleWordUrlIdCount =>
        (tupleWordUrlIdCount._1, // Token
          tupleWordUrlIdCount._2.toList.map(_._2).map(_._2).sum, // Collection Frequency
          math.log(totalNumberOfDocuments / tupleWordUrlIdCount._2.toList.size), // IDF
          tupleWordUrlIdCount._2.toList.map(tupleUrlIdCount => tupleUrlIdCount._2).toMap,
          tupleWordUrlIdCount._2.toList.map(tupleUrlIdCount =>
            (tupleUrlIdCount._2._1, math.log(tupleUrlIdCount._2._2 + 1) * math.log(totalNumberOfDocuments / tupleWordUrlIdCount._2.toList.size))).toMap)
    }
    *  
    */

    authorityTokensRDD.saveToCassandra("finder_keyspace", "url_index",
      SomeColumns("token_text", "collection_freq", "idf", "count_map", "tfidf_map"))

    pathTokensRDD.saveToCassandra("finder_keyspace", "url_index",
      SomeColumns("token_text", "collection_freq", "idf", "count_map", "tfidf_map"))

    // .sasaveAsTextFile("/Users/varadmeru/trial-1")
    /*
 * CREATE TABLE finder_keyspace.url_index (
    token_text text PRIMARY KEY,
    collection_freq int,
    count_map map<int, int>,
    idf float,
    tfidf_map map<int, float>
)
 */
  }
}