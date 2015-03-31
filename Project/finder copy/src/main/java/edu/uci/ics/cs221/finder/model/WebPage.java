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
package edu.uci.ics.cs221.finder.model;

import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import edu.uci.ics.crawler4j.url.WebURL;

/**
 * @author varadmeru
 *
 */
public class WebPage {
	private static final Logger logger = LogManager.getLogger(WebPage.class);

	private int urlId;
	private String URL;
	private String title;
	private String text;
	private Map<String, String> metaTags;
	private Set<String> outgoingLinks;
	private String rawHtml;

	public WebPage() {
		this.urlId = 0;
		this.URL = null;
		this.title = null;
		this.text = null;
		this.metaTags = null;
		this.rawHtml = null;
		this.outgoingLinks = null;
	}

	public WebPage(int urlId, String URL) {
		this.urlId = urlId;
		this.URL = URL;
		this.title = null;
		this.text = null;
		this.metaTags = null;
		this.rawHtml = null;
		this.outgoingLinks = null;
	}

	public WebPage(int urlId, String URL, String title) {
		this.urlId = urlId;
		this.URL = URL;
		this.title = title;
		this.text = null;
		this.metaTags = null;
		this.rawHtml = null;
		this.outgoingLinks = null;
	}

	public WebPage(int urlId, String URL, String title, String text) {
		this.urlId = urlId;
		this.URL = URL;
		this.title = title;
		this.text = text;
		this.metaTags = null;
		this.rawHtml = null;
		this.outgoingLinks = null;
	}

	public WebPage(int urlId, String URL, String title, String text,
			Map<String, String> metaTags) {
		this.urlId = urlId;
		this.URL = URL;
		this.title = title;
		this.text = text;
		this.metaTags = metaTags;
		this.rawHtml = null;
		this.outgoingLinks = null;
	}

	public WebPage(int urlId, String URL, String title, String text,
			Map<String, String> metaTags, Set<WebURL> outgoingLinks) {
		logger.debug("A new WebPage object being created for urlId: " + urlId);
		this.urlId = urlId;
		this.URL = URL;
		this.title = title;
		this.text = text;
		this.metaTags = metaTags;
		this.rawHtml = null;
		this.outgoingLinks = outgoingLinks.stream()
				.map(new Function<WebURL, String>() {

					@Override
					public String apply(WebURL url) {
						return url.getURL();
					}
				}).collect(Collectors.toSet());
	}

	public WebPage(int urlId, String URL, String title, String text,
			Map<String, String> metaTags, Set<WebURL> outgoingLinks,
			String rawHtml) {
		logger.debug("A new WebPage object being created for urlId: " + urlId);
		this.urlId = urlId;
		this.URL = URL;
		this.title = title;
		this.text = text;
		this.metaTags = metaTags;
		this.rawHtml = rawHtml;
		this.outgoingLinks = outgoingLinks.stream()
				.map(new Function<WebURL, String>() {

					@Override
					public String apply(WebURL url) {
						return url.getURL();
					}
				}).collect(Collectors.toSet());
	}

	public int getUrlId() {
		return urlId;
	}

	public void setUrlId(int urlId) {
		this.urlId = urlId;
	}

	public String getURL() {
		return URL;
	}

	public void setURL(String uRL) {
		URL = uRL;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}

	public Map<String, String> getMetaTags() {
		return metaTags;
	}

	public void setMetaTags(Map<String, String> metaTags) {
		this.metaTags = metaTags;
	}

	public Set<String> getOutgoingLinks() {
		return outgoingLinks;
	}

	public void setOutgoingLinks(Set<String> outgoingLinks) {
		this.outgoingLinks = outgoingLinks;
	}

	public String getRawHtml() {
		return rawHtml;
	}

	public void setRawHtml(String rawHtml) {
		this.rawHtml = rawHtml;
	}

	@Override
	public String toString() {
		return " URL Id: " + urlId + "\n URL: " + URL + "\n Title: " + title
				+ "\n Text Length: " + text.length() + "\n HTML Length: "
				+ rawHtml.length() + "\n Metatags: " + metaTags.size()
				+ "\n Outgoing Links: " + outgoingLinks.size();
	}
}