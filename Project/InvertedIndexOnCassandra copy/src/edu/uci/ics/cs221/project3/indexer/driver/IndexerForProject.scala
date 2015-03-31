package edu.uci.ics.cs221.project3.indexer.driver

import edu.uci.ics.cs221.project3.indexer.pagerank.PageRankingURLs

import edu.uci.ics.cs221.project3.indexer.tfidf.AnchorTextAnalysisIndexer
import edu.uci.ics.cs221.project3.indexer.tfidf.InvertedIndexer
import edu.uci.ics.cs221.project3.indexer.tfidf.TwoGramInvertedIndexer
import edu.uci.ics.cs221.project3.indexer.tfidf.PositionIndexer
import edu.uci.ics.cs221.project3.indexer.tfidf.URLTextIndexer

import edu.uci.ics.cs221.project3.sparkmanager.SparkAccessObject

import edu.uci.ics.cs221.project3.conf.Config

object IndexerForProject {
  def main(args: Array[String]): Unit = {
    PageRankingURLs.createPageRankIndex()
    AnchorTextAnalysisIndexer.createAnchorTextIndex()
    InvertedIndexer.createInvertedIndexOnText()
    TwoGramInvertedIndexer.createTwoGramInvertedIndexOnText()
    //    PositionIndexer.createPositionIndexOnText()
    //    URLTextIndexer.createURLTextIndex()
    SparkAccessObject.closeSparkContext()
  }
}