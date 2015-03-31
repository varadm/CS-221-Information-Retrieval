package edu.uci.ics.cs221.project3.indexer.tfidf

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.rdd.PairRDDFunctions

import org.apache.tika.metadata.Metadata
import org.apache.tika.parser.ParseContext
import org.apache.tika.parser.html.HtmlParser
import org.apache.tika.sax.BodyContentHandler
import org.apache.tika.sax.LinkContentHandler
import org.apache.tika.sax.TeeContentHandler
import org.apache.tika.sax.ToHTMLContentHandler

import org.xml.sax.ContentHandler

import com.datastax.spark.connector._

import java.io._
import java.nio.charset._

import org.jsoup._

import edu.uci.ics.cs221.project3.conf.Config
import edu.uci.ics.cs221.project3.sparkmanager.SparkAccessObject

object AnchorTextAnalysisIndexer {

  val linkHandler = new LinkContentHandler();
  val textHandler = new BodyContentHandler(10 * 1024 * 1024 * 1024);
  val toHTMLHandler = new ToHTMLContentHandler();
  val teeHandler = new TeeContentHandler(linkHandler, textHandler, toHTMLHandler);
  val metadata = new Metadata();
  val parseContext = new ParseContext();
  val parser = new HtmlParser();

  // Spark Configuration with the custom configurations
  val sc = SparkAccessObject.getSparkContext()

  def createAnchorTextIndex() = {
    try {

      // Read the Cassandra table
      val tab = sc.cassandraTable("finder_keyspace", "finder_corpus")
      val idTextRDD = tab.select("url_id", "raw_html")

      val idHtmlProjectionTableRDD = idTextRDD.map {
        cassandraRow => (cassandraRow.get[Int]("url_id"), cassandraRow.get[String]("raw_html"))
      }
      val totalNumberOfDocuments = idHtmlProjectionTableRDD.count()

      val finalRDD = idHtmlProjectionTableRDD.foreach {
        x =>
          println(x._2.length())
          parser.parse(new ByteArrayInputStream(x._2.getBytes(Charset.forName("UTF-8"))), teeHandler, metadata, parseContext)
          val links = linkHandler.getLinks()
          println(links.size())
      }

      //    val anchorsRDD = finalRDD.map { x => x.select("a[href]") }
      //    println(anchorsRDD.first().text)
    } catch {
      case t: Throwable =>
        t.printStackTrace() // TODO: handle error
        System.exit(1)
    } finally {
      sc.stop()
    }
  }
}