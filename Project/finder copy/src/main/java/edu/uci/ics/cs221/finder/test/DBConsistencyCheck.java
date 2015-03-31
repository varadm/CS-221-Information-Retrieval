package edu.uci.ics.cs221.finder.test;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.datastax.driver.core.ResultSet;
import com.datastax.driver.core.Row;
import com.datastax.driver.core.Session;

import edu.uci.ics.cs221.finder.data.CassandraDAO;
import edu.uci.ics.cs221.finder.data.RedisDAO;
import edu.uci.ics.cs221.finder.utilities.Config;

public class DBConsistencyCheck {
	public static void main(String[] args) {
		CassandraDAO cassandraDAO = new CassandraDAO();
		RedisDAO redisDAO = new RedisDAO();

		Session session = cassandraDAO.getCassandraSession();
		ResultSet cassandraRS = session.execute("SELECT url_id, url FROM "
				+ Config.CASSANDRA_KEYSPACE_NAME + "."
				+ Config.CASSANDRA_CORPUS_TABLE);

		Map<Integer, String> map = convertToMap(cassandraRS);
		Set<String> keys = redisDAO.getKeys();
		List<String> list = new ArrayList<String>();

		for (String url : keys) {
			if (map.containsKey(Integer.parseInt(redisDAO.getKey(url)))) {
				continue;
			} else {
				list.add(url);
			}
		}
		System.out.println(map.size() + "::" + keys.size() + "::" + list.size());
		System.out.println("======================================");
		for (String string : list) {
			System.out.println(string);
		}
		cassandraDAO.close();
		redisDAO.close();
	}

	private static Map<Integer, String> convertToMap(ResultSet cassandraRS) {
		Map<Integer, String> map = new HashMap<Integer, String>();
		for (Row row : cassandraRS) {
			map.put(row.getInt("url_id"), row.getString("url"));
		}
		return map;
	}
}