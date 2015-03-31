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

package edu.uci.ics.cs221.finder.crawler;

import java.util.regex.Pattern;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import edu.uci.ics.crawler4j.crawler.Page;
import edu.uci.ics.crawler4j.crawler.WebCrawler;
import edu.uci.ics.crawler4j.parser.HtmlParseData;
import edu.uci.ics.crawler4j.url.WebURL;
import edu.uci.ics.cs221.finder.data.RedisDAO;
import edu.uci.ics.cs221.finder.model.Corpus;
import edu.uci.ics.cs221.finder.model.WebPage;

/**
 * @author varadmeru
 */
public class FinderCrawler extends WebCrawler {
	private static final Logger logger = LogManager
			.getLogger(FinderCrawler.class);

	RedisDAO redisDAO = new RedisDAO();
	Corpus corpus = new Corpus();
	WebPage webPage = null;

	// Filters, not to include page that has any one of these extensions
	private final static Pattern FILTERS = Pattern
			.compile(".*\\.(css|js|gif|jpe?g|png|mp3|zip|gz"
					+ "|bmp|ico|PNG|tiff?|mid|mp2|mp4|wav|avi"
					+ "|mov|mpeg|ram|aaf|asf|flv|m4v|mkv|ogg"
					+ "|ogv|pdf|ps|eps|tex|ppt|pptx|doc|docx"
					+ "|xls|xlsx|names|data|xaml|pict|rif|dat"
					+ "|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub"
					+ "|dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar"
					+ "|csv|rm|smil|wm?v|swf|wma|au|aiff|flac"
					+ "|3gp|amr|au|vox|rar|aac|ace|alz|apk|arc"
					+ "|arj|lzip|lha|txt|java|javac|cc|h|pfm)" + "(\\?.*)?$");

	// skip URLs containing certain characters as probable queries, etc.
	private final static Pattern QFILTERS = Pattern.compile(".*[\\?@=].*");

	// Some explicit Traps to avoid
	// private final static String trap2 = "calendar.ics.uci.edu";
	private final static String trap4 = "drzaius.ics.uci.edu/cgi-bin/cvsweb.cgi/";
	// private final static String trap5 = "flamingo.ics.uci.edu/releases/";
	// private final static String trap6 = "fano.ics.uci.edu/ca/";
	private final static String trap7 = "ironwood.ics.uci.edu";
	private final static String trap8 = "djp3-pc2.ics.uci.edu/LUCICodeRepository/";
	private final static String trap9 = "archive.ics.uci.edu/ml";
	private final static String trap10 = "www.ics.uci.edu/~xhx/project/MotifMap/";

	/**
	 * This method receives two parameters. The first parameter is the page in
	 * which we have discovered this new url and the second parameter is the new
	 * url. You should implement this function to specify whether the given url
	 * should be crawled or not (based on your crawling logic). In this example,
	 * we are instructing the crawler to ignore urls that have css, js, git, ...
	 * extensions and to only accept urls that start with
	 * "http://www.ics.uci.edu/". In this case, we didn't need the referringPage
	 * parameter to make the decision.
	 */
	@Override
	public boolean shouldVisit(Page referringPage, WebURL url) {
		String href = url.getURL().toLowerCase();
		logger.debug("Should visit? - " + href);

		return !FILTERS.matcher(href).matches()
				&& !QFILTERS.matcher(href).matches()
				&& href.contains(".ics.uci.edu");
	}

	/**
	 * This function is called when a page is fetched and ready to be processed
	 * by your program.
	 */
	@Override
	public void visit(Page page) {
		String urlString = page.getWebURL().getURL();

		logger.debug("Visiting Page:- " + urlString);

		if (page.getParseData() instanceof HtmlParseData) {
			HtmlParseData htmlParseData = (HtmlParseData) page.getParseData();
			int nextId = corpus.getNextWebPageId();
			// Putting the abs URL into the Default DB
			redisDAO.putKey(urlString.toLowerCase(), nextId);
			webPage = new WebPage(nextId, urlString, htmlParseData.getTitle(),
					htmlParseData.getText(), htmlParseData.getMetaTags(),
					htmlParseData.getOutgoingUrls(), htmlParseData.getHtml());

			corpus.writePageIntoDB(webPage);
		}
	}
}