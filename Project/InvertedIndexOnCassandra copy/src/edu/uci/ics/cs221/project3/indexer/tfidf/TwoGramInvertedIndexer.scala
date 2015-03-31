package edu.uci.ics.cs221.project3.indexer.tfidf

import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.rdd.PairRDDFunctions
import com.datastax.spark.connector._

import edu.uci.ics.cs221.project3.conf.Config
import edu.uci.ics.cs221.project3.stemmer.PorterStemmer
import edu.uci.ics.cs221.project3.sparkmanager.SparkAccessObject

object TwoGramInvertedIndexer {

  /**
   * A list of common English stop words.
   */
  val stopWords = Set("a", "about", "above", "above", "across", "after",
    "afterwards", "again", "against", "all", "almost",
    "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amongst", "amount", "an", "and",
    "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere",
    "are", "around", "as", "at", "back", "be", "became", "because",
    "become", "becomes", "becoming", "been", "before", "beforehand",
    "behind", "being", "below", "beside", "besides", "between", "beyond",
    "bill", "both", "bottom", "but", "by", "call", "can", "cannot",
    "cant", "co", "con", "could", "couldnt", "cry", "de", "describe",
    "detail", "do", "done", "down", "due", "during", "each", "eg",
    "eight", "either", "eleven", "else", "elsewhere", "empty",
    "enough", "etc", "even", "ever", "every", "everyone", "everything",
    "everywhere", "except", "few", "fifteen", "fify", "fill", "find",
    "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give",
    "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here",
    "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him",
    "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc",
    "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last",
    "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither", "never",
    "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not",
    "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one",
    "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves",
    "out", "over", "own", "part", "per", "perhaps", "please", "put", "rather", "re",
    "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she",
    "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some",
    "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still",
    "such", "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore",
    "therein", "thereupon", "these", "they", "thick", "thin", "third", "this",
    "those", "though", "three", "through", "throughout", "thru", "thus", "to",
    "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un",
    "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well",
    "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter",
    "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which",
    "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will",
    "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves")

  // Spark Configuration with the custom configurations
  val sc = SparkAccessObject.getSparkContext()

  def createTwoGramInvertedIndexOnText() = {
    // Read the Cassandra table
    val tab = sc.cassandraTable("finder_keyspace", "finder_corpus_1")
    val idTextRDD = tab.select("url_id", "page_text")
    val idTextProjectionTableRDD = idTextRDD.map {
      cassandraRow => (cassandraRow.get[Int]("url_id"), cassandraRow.get[String]("page_text"))
    }
    val totalNumberOfDocuments = idTextProjectionTableRDD.count()
    val finalRDD = new PairRDDFunctions(idTextProjectionTableRDD.flatMap {
      case (urlId, pageText) => pageText.toLowerCase().split("""\W+""").filter { case (word) => !word.isEmpty() }
        .filter(!stopWords.contains(_)).filter { case (word) => !word.isEmpty() }
        .sliding(2)
        .map(p => p.mkString(" ")).filter { case (word) => !word.isEmpty() }
        .map { case (word) => (word, urlId) }
    }.map {
      case (word, urlId) => ((word, urlId), 1)
    })
      .reduceByKey {
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
    finalRDD.repartition(10);
    val savingToCassandra = finalRDD.saveToCassandra("finder_keyspace", "inverted_index_two_grams",
      SomeColumns("token_text", "collection_freq", "idf", "count_map", "tfidf_map"))
    // sc.stop()
  }
}