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

package edu.uci.ics.cs221.finder.driver;

import java.util.Arrays;
import java.util.List;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import edu.uci.ics.crawler4j.crawler.CrawlConfig;
import edu.uci.ics.crawler4j.crawler.CrawlController;
import edu.uci.ics.crawler4j.fetcher.PageFetcher;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtConfig;
import edu.uci.ics.crawler4j.robotstxt.RobotstxtServer;
import edu.uci.ics.cs221.finder.crawler.FinderCrawler;
import edu.uci.ics.cs221.finder.utilities.Config;

/**
 * The driver class, from where the crawler configurations are set and the
 * crawler is run.
 * 
 * @since Feb 03, 2015
 * @author Varad Meru, vmeru@ics.uci.edu
 * @author University of California, Irvine
 */
public class Controller {
	private static final Logger logger = LogManager.getLogger(Controller.class);

	/**
	 * @param args
	 * @throws Exception
	 */
	public static void main(String[] args) throws Exception {
		long start = System.currentTimeMillis();
		logger.info("Crawler Starting; Start Time: " + start);

		// Configurations
		CrawlConfig config = new CrawlConfig();
		config.setCrawlStorageFolder(Config.CRAWL_STORAGE_FOLDER);
		config.setUserAgentString(Config.USER_AGENT_STRING);
		config.setMaxDepthOfCrawling(100);
		config.setPolitenessDelay(200);
		config.setResumableCrawling(true);

		/*
		 * Instantiate the controller for this crawl.
		 */
		PageFetcher pageFetcher = new PageFetcher(config);
		RobotstxtConfig robotstxtConfig = new RobotstxtConfig();
		RobotstxtServer robotstxtServer = new RobotstxtServer(robotstxtConfig,pageFetcher);
		CrawlController controller = new CrawlController(config, pageFetcher,robotstxtServer);

		/*
		 * For each crawl, you need to add some seed urls. These are the first
		 * URLs that are fetched and then the crawler starts following links
		 * which are found in these pages
		 */
		String[] seedStrings = new String[] { "http://www.ics.uci.edu/",
				"http://www.ics.uci.edu/~gbolcer/", "http://soc.ics.uci.edu",
				"http://hombao.ics.uci.edu",
				"http://www.ics.uci.edu/~ccgrid11/", "http://www.cs.uci.edu",
				"http://www.informatics.uci.edu" };

		List<String> seeds = Arrays.asList(seedStrings);

		logger.info("Added Seed URLS -" + seeds);

		// Adding the Seed URL from the list seeds.
		for (String seed : seeds) {
			controller.addSeed(seed);
		}

		/*
		 * Start the crawl. This is a blocking operation, meaning that your code
		 * will reach the line after this only when crawling is finished.
		 */
		logger.info("Starting Crawling with # crawlers -" + Config.NUM_OF_CRAWLERS);
		controller.start(FinderCrawler.class, Config.NUM_OF_CRAWLERS);
		if (controller.isFinished()) {
			logger.info("Crawler Finished Time: " + System.currentTimeMillis()
					+ ", Time Taken: " + (start - System.currentTimeMillis()));
		}
	}
}