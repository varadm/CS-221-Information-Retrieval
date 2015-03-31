package edu.uci.ics.cs221.finder.model;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import com.datastax.driver.core.BoundStatement;
import com.datastax.driver.core.PreparedStatement;
import com.datastax.driver.core.Session;

import edu.uci.ics.cs221.finder.data.CassandraConnectionFactory;
import edu.uci.ics.cs221.finder.data.CassandraDAO;
import edu.uci.ics.cs221.finder.utilities.Config;

/**
 * @author varadmeru
 *
 */
public class Corpus {
	private static final Logger logger = LogManager.getLogger(Corpus.class);
	private static CassandraDAO cassandraDAO = new CassandraDAO();
	private static int lastId = cassandraDAO.getLastURLIdFromDB();
	private static int count = (lastId == 0) ? 0 : lastId;

	private Session session = CassandraConnectionFactory.getSessionInstance();
	private PreparedStatement insertIntoCorpus = session
			.prepare(Config.CASSANDRA_INSERT_ENTRY_INTO_CORPUS);

	/**
	 * 
	 */
	public Corpus() {
	}

	/**
	 * @return
	 */
	public synchronized int getNextWebPageId() {
		int result = count;
		count++;
		return result;
	}
	
	
	/**
	 * @param webPage
	 */
	public void writePageIntoDB(WebPage webPage) {
		BoundStatement boundStatement = new BoundStatement(insertIntoCorpus);
		try {
			// url_id, url, title, metatags, page_text, raw_html, outgoing_links
			boundStatement.setInt(0, webPage.getUrlId());
			boundStatement.setString(1, webPage.getURL());
			boundStatement.setString(2, webPage.getTitle());
			boundStatement.setMap(3, webPage.getMetaTags());
			boundStatement.setString(4, webPage.getText());
			boundStatement.setString(5, webPage.getRawHtml());
			boundStatement.setSet(6, webPage.getOutgoingLinks());
			cassandraDAO.execute(boundStatement);
		} catch (Exception e) {
			logger.debug("Error while binding the statement", e);
		}
	}
	
	// TODO Complete the implementation for transferring the URL, URL_ID
	// as well as URL_ID to URL to REDIS and specify the associated tables
	// for it.
	/**
	 * 
	 */
	public void populateURLTableFromCassandra() {
	}

	/**
	 * 
	 */
	public void closeDBConnection() {
		cassandraDAO.close();
	}
}
