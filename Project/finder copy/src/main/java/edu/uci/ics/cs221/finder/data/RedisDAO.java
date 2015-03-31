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

import java.util.Set;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import redis.clients.jedis.Jedis;

/**
 * @author varadmeru
 *
 */
public class RedisDAO {
	private static final Logger logger = LogManager.getLogger(RedisDAO.class);
	Jedis jedis = null;

	/**
	 * 
	 */
	public RedisDAO() {
		jedis = RedisConnectionFactory.getRedisConnectionInstance();
	}

	/**
	 * 
	 */
	public RedisDAO(int dbNumber) {
		jedis = RedisConnectionFactory.getRedisConnectionInstance();
		jedis.select(dbNumber);
	}

	/**
	 * @param key
	 * @param value
	 */
	public void putKey(String key, int value) {
		jedis.select(0);
		jedis.set(key, Integer.toString(value));
	}

	/*	*//**
	 * @param key
	 * @param value
	 */
	/*
	 * public void putKey(String key, String value, int dbNumber) {
	 * jedis.select(dbNumber); jedis.set(key, value); }
	 *//**
	 * @param key
	 * @param value
	 */
	/*
	 * public void putKey(String key, int value, int dbNumber) {
	 * jedis.select(dbNumber); jedis.set(key, Integer.toString(value)); }
	 */

	/**
	 * @param key
	 * @param value
	 */
	public void putKey(String key, String value) {
		jedis.set(key, value);
	}

	/**
	 * @param key
	 * @return
	 */
	public String getKey(String key) {
		jedis.select(0);
		return jedis.get(key);
	}

	/**
	 * @param key
	 * @param isInt
	 * @return
	 */
	public int getKey(String key, boolean isInt) {
		jedis.select(0);
		logger.info("Fetching key " + key + " from Redis.");
		if (hasKey(key, 0)) {
			logger.info("key exists, with the value being returned");
			return Integer.parseInt(jedis.get(key));
		} else {
			logger.info("key does not exists. Integer.MIN_VALUE being returned.");
			return Integer.MIN_VALUE;
		}
	}

	/**
	 * @param key
	 * @return
	 */
	public String getKey(String key, int dbNumber) {
		jedis.select(dbNumber);
		return jedis.get(key);
	}

	/**
	 * @param key
	 * @param isInt
	 * @return
	 */
	public int getKey(String key, boolean isInt, int dbNumber) {
		jedis.select(dbNumber);
		logger.info("Fetching key " + key + " from Redis.");
		if (hasKey(key, dbNumber)) {
			logger.info("key exists, with the value being returned");
			return Integer.parseInt(jedis.get(key));
		} else {
			logger.info("key does not exists. Integer.MIN_VALUE being returned.");
			return Integer.MIN_VALUE;
		}
	}

	/**
	 * @param key
	 * @param dbNumber
	 * @return
	 */
	public boolean hasKey(String key) {
		logger.info("Checking if key exists: " + key);
		jedis.select(0);
		return jedis.exists(key);
	}

	/**
	 * @param key
	 * @param dbNumber
	 * @return
	 */
	public boolean hasKey(String key, int dbNumber) {
		logger.info("Checking if key exists: " + key);
		jedis.select(dbNumber);
		return jedis.exists(key);
	}

	/**
	 * For Debug Purposes.
	 * 
	 * @return {@link Set} of {@link String} which would be all the keys with
	 *         pattern *
	 */
	public Set<String> getKeys() {
		logger.debug("Fetching all the Keys");
		return jedis.keys("*");
	}

	/**
	 * For Debug Purposes.
	 * 
	 * @return {@link Set} of {@link String} which would be all the keys with
	 *         pattern *, in the db specified.
	 */
	public Set<String> getKeys(int dbNumber) {
		jedis.select(dbNumber);
		logger.debug("Fetching all the Keys for DB Number -" + dbNumber);
		return jedis.keys("*");
	}

	/**
	 * Interface to close the Redis Connection.
	 */
	public void close() {
		logger.info("Closing the connection for redis");
		RedisConnectionFactory.close();
	}
}
