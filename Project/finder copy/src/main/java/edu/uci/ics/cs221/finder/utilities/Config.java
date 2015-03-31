/**
 * License - 
 * 
 * Finder: Search Engine for the CS 221 Information Retrieval, {@link http://www.ics.uci.edu/~lopes/teaching/cs221W15/}.
 * @since Feb 03, 2015
 * @version 0.0.2
 * @author Varad Meru, vmeru@ics.uci.edu
 * @author Nishaanth Reddy, nhreddy@uci.edu
 * @author University of California, Irvine
 */
package edu.uci.ics.cs221.finder.utilities;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

/**
 * @author varadmeru
 *
 */
public final class Config {
	private static final Logger logger = LogManager.getLogger(Config.class);

	public Config() {
		logger.info("Config has been initialised");
	}

	// CRAWLER CONFIGURATIONS
	/**
	 * The storage place for all the crawler related stuff, e.g. Frontier and
	 * others
	 */
	public static final String CRAWL_STORAGE_FOLDER = "/Users/varadmeru/uci-related/uci-courses/CS-221-Information-Retrieval/Project/data";

	/**
	 * Number of crawlers
	 */
	public static final int NUM_OF_CRAWLERS = 16;

	/**
	 * 
	 */
	public static final String USER_AGENT_STRING = "UCI WebCrawler 26648958 14765903";

	// CASSANDRA CONFIGURATIONS
	/**
	 * IP address of the host, hosting Cassandra
	 */
	public static final String CASSANDRA_HOST = "127.0.0.1";

	/**
	 * 
	 */
	public static final String CASSANDRA_PORT = "9042";

	/**
	 * 
	 */
	public static final String CASSANDRA_CORPUS_TABLE = "finder_corpus_1";

	/**
	 * 
	 */
	public static final String CASSANDRA_KEYSPACE_NAME = "finder_keyspace";

	// REDIS CONFIGURATIONS
	/**
	 * IP address of the host, hosting Redis
	 */
	public static final String REDIS_HOST = "127.0.0.1";

	/**
	 * 
	 */
	public static final String REDIS_PORT = "9042";

	/**
	 * 
	 */
	public static final int URL_PATH_DB = 1;

	// CASSANDRA PREPARED STATEMENTS
	/**
	 * webPage.getUrlId(),webPage.getURL(), webPage.getTitle(),
	 * webPage.getMetaTags(), webPage.getText(),
	 * webPage.getRawHtml(),webPage.getOutgoingLinks()
	 */
	public static final String CASSANDRA_INSERT_ENTRY_INTO_CORPUS = "INSERT INTO "
			+ CASSANDRA_KEYSPACE_NAME
			+ "."
			+ CASSANDRA_CORPUS_TABLE
			+ " (url_id, url, title, metatags, page_text, raw_html, outgoing_links) VALUES (?, ?, ?, ?, ?, ?, ?);";

	// TODO: To implement
	public static final String CASSANDRA_INSERT_ENTRY_INTO_CORPUS_2 = null;

	public static final String CASSANDRA_CORPUS_TABLE_URL_ID_LATEST = "SELECT url_id FROM "
			+ CASSANDRA_KEYSPACE_NAME + "." + CASSANDRA_CORPUS_TABLE;

	/*
	  CREATE TABLE finder_keyspace.finder_corpus_1 ( url_id int PRIMARY KEY,
	  metatags map<text, text>, outgoing_links set<text>, page_text text,
	  raw_html text, title text, url text )
	 */
}