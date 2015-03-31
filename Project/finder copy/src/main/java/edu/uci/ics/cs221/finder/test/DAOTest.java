package edu.uci.ics.cs221.finder.test;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import edu.uci.ics.crawler4j.url.WebURL;
import edu.uci.ics.cs221.finder.model.Corpus;
import edu.uci.ics.cs221.finder.model.WebPage;

public class DAOTest {
	public static void main(String[] args) {
		Map<String, String> metaTags = new HashMap<String, String>();
		Corpus corpus = new Corpus();
		Set<WebURL> outgoingLinks = new HashSet<WebURL>();

		WebURL weburl = new WebURL();
		weburl.setURL("http://www.google.com");
		outgoingLinks.add(weburl);

		metaTags.put("key1", "value1");
		metaTags.put("key2", "value2");
		metaTags.put("key3", "value3");

		WebPage page = new WebPage(1, "http://www.google.com",
				"Welcome to Google!", "Hi, Put in your query", metaTags,
				outgoingLinks,
				"<title>Welcome to Google!</title> <body>Hi, Put in your query</body>");
		corpus.writePageIntoDB(page);
	}
}
