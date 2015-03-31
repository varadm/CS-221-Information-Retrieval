package edu.uci.ics.cs221.project3.indexer.pagerank

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.rdd.PairRDDFunctions
import org.apache.spark.graphx._

import com.datastax.spark.connector._

import edu.uci.ics.cs221.project3.conf.Config
import edu.uci.ics.cs221.project3.sparkmanager.SparkAccessObject

object PageRankingURLs {

  // Spark Configuration with the custom configurations
  val sc = SparkAccessObject.getSparkContext()

  def createPageRankIndex() = {

    // Read the Cassandra table
    val tab = sc.cassandraTable("finder_keyspace", "finder_corpus_1")

    val outgoingUrlsRDD = tab.select("url_id", "outgoing_links")
    val urls = tab.select("url_id", "url")

    val urlsRDD = urls.map {
      cassandraRow => (cassandraRow.get[String]("url"), cassandraRow.get[Int]("url_id"))
    }

    val urlOutgoingLinksRDD = outgoingUrlsRDD.map {
      cassandraRow => (cassandraRow.get[Int]("url_id"), cassandraRow.get[Set[String]]("outgoing_links"))
    }

    val flattenedURLRDD = urlOutgoingLinksRDD.flatMap {
      case (urlId, outgoing_urls) => outgoing_urls.map { x => (urlId, x) }
    }

    // For Join, swapping the keys.
    val flattenedURLRDD2 = flattenedURLRDD.map {
      x => (x._2, x._1)
    }

    val pairflattenedURLRDD = new PairRDDFunctions(flattenedURLRDD2)
    val joinResult = pairflattenedURLRDD.join(urlsRDD)
    val edgesRDD = joinResult.map {
      x => Edge(x._2._1, x._2._2, "")
    }

    val graph = Graph.fromEdges(edgesRDD, "")
    val pageRankOutputRDD = graph.pageRank(0.0001)
    val ranks = pageRankOutputRDD.vertices
    ranks.sortBy({
      k => k._2
    }, false).saveToCassandra("finder_keyspace", "pagerank_urls",
      SomeColumns("url_id", "pagerank"))
    /*
     * cqlsh> select * from finder_keyspace.pagerank_urls limit 5;
     * url_id | pagerank
     *--------+----------
     *   4317 |  0.16444
     *  25269 |  0.16683
     *   3372 |  0.86344
     *  14340 |  0.20361
     *  18417 |  0.83239
     *  (5 rows)
     * 
     */
  }
}