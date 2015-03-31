package edu.uci.ics.cs221.project3.parsers

import java.io.InputStream
import java.net.URL
import org.apache.tika.metadata.Metadata
import org.apache.tika.parser.ParseContext
import org.apache.tika.parser.html.HtmlParser
import org.apache.tika.sax.BodyContentHandler
import org.apache.tika.sax.LinkContentHandler
import org.apache.tika.sax.TeeContentHandler
import org.apache.tika.sax.ToHTMLContentHandler
import org.xml.sax.ContentHandler

object TestTikaInScala {
  def main(args: Array[String]): Unit = {
    val url = new URL("http://chrisjordan.ca/post/15219674437/parsing-html-with-apache-tika");
    val input = url.openStream();

    val linkHandler = new LinkContentHandler();
    val textHandler = new BodyContentHandler();
    val toHTMLHandler = new ToHTMLContentHandler();
    val teeHandler = new TeeContentHandler(linkHandler, textHandler, toHTMLHandler);
    val metadata = new Metadata();
    val parseContext = new ParseContext();
    val parser = new HtmlParser();

    parser.parse(input, teeHandler, metadata, parseContext);
    val links = linkHandler.getLinks()
    val n = 1
    println("*******************")
    println(links.get(n).getText)
    println(links.get(n).getTitle)
    println(links.get(n).getType)
    println(links.get(n).getUri)
    println(links.get(n).isAnchor())
    println(links.get(n).isImage())
    println(links.get(n).toString())
    println("*******************")
    println("title:\n" + metadata.get("title"))
    metadata.names().foreach(println)
    //    println("names:\n" + metadata.names().length)
    //    println("names:\n" + metadata.names().length)
    // System.out.println("links:\n" + linkHandler.getLinks());
    // System.out.println("text:\n" + textHandler.toString());
    // System.out.println("html:\n" + toHTMLHandler.toString());
  }
}