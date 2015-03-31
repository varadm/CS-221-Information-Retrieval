package edu.uci.ics.cs221.finder.test;

import io.mola.galimatias.GalimatiasParseException;
import io.mola.galimatias.URL;

public class URLLibTest {
	public static void main(String[] args) {

		String s = "http://archive.ics.uci.edu/ml/datasets.html?area&att&format=mat&numAtt&numIns&sort=nameUp&task&type=ts&view=table";
		String s2 = "http://archive.ics.uci.edu/ml/datasets.html";

		URL urlx = null;
		try {
			urlx = URL.parse(s);
		} catch (GalimatiasParseException ex) {
			ex.printStackTrace();
		} catch (Exception ex) {
			ex.printStackTrace();
		}

		System.out.println("***************************************");
		System.out.println("1 " + urlx.path());
		System.out.println("2 " + urlx.query());
		System.out.println("3 " + urlx.authority());
		System.out.println("4 " + urlx.defaultPort());
		System.out.println("5 " + urlx.toHumanString());
		System.out.println("6 " + urlx.scheme());
		System.out.println("URL - " + urlx.scheme() + "://" + urlx.authority()
				+ urlx.path());
		System.out.println("***************************************");

		try {
			urlx = URL.parse(s2);
		} catch (GalimatiasParseException ex) {
			ex.printStackTrace();
		}

		System.out.println("***************************************");
		System.out.println("1 " + urlx.path());
		System.out.println("2 " + urlx.query());
		System.out.println("3 " + urlx.authority());
		System.out.println("4 " + urlx.defaultPort());
		System.out.println("5 " + urlx.toHumanString());
		System.out.println("6 " + urlx.scheme());
		System.out.println("URL - " + urlx.scheme() + "://" + urlx.authority()
				+ urlx.path());
		System.out.println("***************************************");
	}
}
