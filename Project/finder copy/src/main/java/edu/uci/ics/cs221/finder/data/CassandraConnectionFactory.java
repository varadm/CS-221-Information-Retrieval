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

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import com.datastax.driver.core.Cluster;
import com.datastax.driver.core.Session;

import edu.uci.ics.cs221.finder.utilities.Config;

public class CassandraConnectionFactory {
	private static final Logger logger = LogManager
			.getLogger(CassandraConnectionFactory.class);
	private static Cluster cluster = null;
	private static Session session = null;

	private CassandraConnectionFactory() {

	}

	/**
	 * 
	 */
	public static void close() throws Exception {
		try {
			cluster.close();
		} catch (Exception e) {
			throw e;
		}
	}

	/**
	 * @return
	 */
	public static Cluster getClusterInstance() {
		if (cluster == null) {
			try {
				cluster = Cluster.builder()
						.addContactPoint(Config.CASSANDRA_HOST).build();
			} catch (Exception e) {
				logger.error("Error getting the Cassandra Connection", e);
			}

		}
		logger.info("Fecthing the instance of Cluster: " + session);
		return cluster;
	}

	public static Session getSessionInstance() {
		if (session == null) {
			try {
				cluster = getClusterInstance();
				session = cluster.connect();
			} catch (Exception e) {
				logger.error("Error getting the Cassandra Session", e);
			}
		}
		logger.info("Fecthing the instance of Session: " + session);
		return session;
	}
}
