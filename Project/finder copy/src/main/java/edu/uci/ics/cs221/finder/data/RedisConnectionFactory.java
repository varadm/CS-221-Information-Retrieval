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

import redis.clients.jedis.Jedis;
import redis.clients.jedis.exceptions.JedisException;
import edu.uci.ics.cs221.finder.utilities.Config;

/**
 * @author varadmeru
 *
 */
public class RedisConnectionFactory {
	private static final Logger logger = LogManager.getLogger(RedisConnectionFactory.class);
	private static Jedis jedisConnection = null;

	/**
	 * 
	 */
	public static void close() {
        try {
                jedisConnection.close();
        } catch (JedisException e) {
                logger.info("Error while closing the Redis Connection", e);
        }
        jedisConnection = null;
}

	/**
	 * @return
	 */
	public static Jedis getRedisConnectionInstance() {
		if (jedisConnection == null) {
			logger.debug("Getting a new Redis connection");
			jedisConnection = new Jedis(Config.REDIS_HOST);
		}
		return jedisConnection;
	}
}
