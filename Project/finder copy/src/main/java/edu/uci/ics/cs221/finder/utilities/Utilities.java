package edu.uci.ics.cs221.finder.utilities;

import io.mola.galimatias.GalimatiasParseException;
import io.mola.galimatias.URL;

/**
 * @author varadmeru
 *
 */
public class Utilities {
	/**
	 * @param completeURL
	 * @return
	 */
	public static String parseURLPath(String completeURL) {
		URL urlx = null;
		try {
			urlx = URL.parse(completeURL);
		} catch (GalimatiasParseException ex) {
			ex.printStackTrace();
		}
		return urlx.scheme() + "://" + urlx.authority() + urlx.path();
	}
}
