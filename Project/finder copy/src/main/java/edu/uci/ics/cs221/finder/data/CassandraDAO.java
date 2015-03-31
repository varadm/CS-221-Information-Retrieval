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

package edu.uci.ics.cs221.finder.data;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import com.datastax.driver.core.BoundStatement;
import com.datastax.driver.core.PreparedStatement;
import com.datastax.driver.core.ResultSet;
import com.datastax.driver.core.Row;
import com.datastax.driver.core.Session;

import edu.uci.ics.cs221.finder.model.WebPage;
import edu.uci.ics.cs221.finder.utilities.Config;

/**
 *
 */
public class CassandraDAO {
	private static final Logger logger = LogManager
			.getLogger(CassandraDAO.class);

	private Session session = null;
	private PreparedStatement insertIntoCorpus = null;

	public CassandraDAO() {
		session = CassandraConnectionFactory.getSessionInstance();
		insertIntoCorpus = session.prepare(Config.CASSANDRA_INSERT_ENTRY_INTO_CORPUS);
	}

	// READ SECTION
	public int getLastURLIdFromDB() {
		List<Integer> integers = new ArrayList<Integer>();
		integers.add(0);
		ResultSet x = session
				.execute(Config.CASSANDRA_CORPUS_TABLE_URL_ID_LATEST);
		Iterator<Row> it = x.iterator();

		while (it.hasNext()) {
			int urlId = (it.next().getInt(0));
			integers.add(urlId);
		}
		return findMax(integers);
	}

	private int findMax(List<Integer> integers) {
		int max = Integer.MIN_VALUE;
		for (Integer integer : integers) {
			if (max < integer) {
				max = integer;
			}
		}
		return max;
	}

	WebPage readFromDatabase(int URLId) {
		return null;
	}

	WebPage readFromDatabase(String URL) {
		return null;
	}

	// WRITE SECTION

	/**
	 * @param webPage
	 * @deprecated
	 * 
	 *             Remember, the write with the same url_id already present in
	 *             the DB overwrites the already present data.
	 */
	@Deprecated
	public void writeIntoDB(WebPage webPage) {
		logger.debug("Writing the URL: " + webPage.getURL());
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

			session.execute(boundStatement);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void close() {
		try {
			CassandraConnectionFactory.close();
		} catch (Exception e) {
			logger.info(
					"Exception while closing the Connection and the Session", e);
		}
	}

	public void execute(BoundStatement boundStatement) {
		try {
			session.execute(boundStatement);
		} catch (Exception e) {
			logger.debug("Error while Executing the statement on DB", e);
		}

	}

	public Session getCassandraSession() {
		return session;
	}
}
