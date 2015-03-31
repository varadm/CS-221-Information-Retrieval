
# Finder: Search Engine for the CS 221 Information Retrieval, (http://www.ics.uci.edu/~lopes/teaching/cs221W15/).

#### A search engine using crawler4j from the [Mondego group](http://mondego.ics.uci.edu "Mondego Group") at UCI. 

#### Since: Feb 03, 2015
#### Version: 0.0.2
#### &copy;  Varad Meru (vmeru@ics.uci.edu, 26648958) and Nishaanth Reddy (nhreddy@uci.edu, 14765903)
#### &copy;  University of California, Irvine


## Project Structure and Details
#####Folders
*   {project.home}/logs
*   {project.home}/src
-	-/main/java
-	-/main/resources
-	-/test/java

#####/src Packages:
*	edu.uci.ics.cs221.finder
-	-crawler
-	-data
-	-driver
-	-model
-	-utilities

## Crawler Configurations
*	User Agent = "UCI WebCrawler 26648958 14765903"
*	Seed URLs ->
*	"http://www.ics.uci.edu/~lopes/"
*	"http://www.ics.uci.edu/"
*	"http://isg.ics.uci.edu/" 
*	"http://www.ics.uci.edu/~lopes/teaching/cs221W15/"

###### # of Crawlers= 10
###### Politeness Delay=500
###### Max Depth of Crawling=20
###### Extensions to Filter= 

	[css|js|gif|jpe?g|png|mp3|zip|gz|bmp|ico|PNG|tiff?|mid|mp2|mp4|wav|avi|mov|
	mpeg|ram|aaf|asf|flv|m4v|mkv|ogg|ogv|pdf|ps|eps|tex|ppt|pptx|doc|docx|xls|
	xlsx|names|data|xaml|pict|rif|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|
	dll|cnf|tgz|sha1|thmx|mso|arff|rtf|jar|csv|rm|smil|wm?v|swf|wma|au|aiff|flac|
	3gp|amr|au|vox|rar|aac|ace|alz|apk|arc|arj|lzip|lha|txt|java|class|cc|h|pfm]


## Probable Traps
* http://calendar.ics.uci.edu
* https://duttgroup.ics.uci.edu/
* http://djp3-pc2.ics.uci.edu/LUCICodeRepository/
* https://archive.ics.uci.edu/ml/datasets.html
* http://drzaius.ics.uci.edu/cgi-bin/cvsweb.cgi/
* http://flamingo.ics.uci.edu/releases/
* http://fano.ics.uci.edu/ca/
* http://ironwood.ics.uci.edu/
* http:www.ics.uci.edu/~xhx/project/MotifMap/