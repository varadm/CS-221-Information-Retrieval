CREATE KEYSPACE finder_keyspace
WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 } ;

CREATE TABLE IF NOT EXISTS finder_keyspace.finder_corpus (
url_id INT PRIMARY KEY,
url TEXT,
title TEXT,
metatags MAP<TEXT,TEXT>, 
page_text TEXT,
raw_html TEXT,
outgoing_links SET<TEXT>
);

CREATE TABLE IF NOT EXISTS finder_keyspace.finder_corpus_v1 (
url_id INT PRIMARY KEY,
url TEXT,
title TEXT,
metatags MAP<TEXT,TEXT>, 
page_text TEXT,
raw_html TEXT,
outgoing_links SET<TEXT>
);

cqlsh -k finder_keyspace -e 'COPY finder_corpus(url_id,url,title,metatags, page_text,raw_html,outgoing_links) TO STDOUT' | head -n -1 | 
cqlsh -k finder_keyspace -e 'COPY finder_corpus_v1(url_id,url,title,metatags, page_text,raw_html,outgoing_links) FROM STDIN'

CREATE TABLE IF NOT EXISTS finder_keyspace.tokens_per_page (
url_id INT PRIMARY KEY,
title_count MAP<TEXT,INT>,
title_pos MAP<TEXT,TEXT>,
title_tfidf MAP<TEXT,FLOAT>,
token_count MAP<TEXT,INT>,
token_pos MAP<TEXT,TEXT>,
token_tfidf MAP<TEXT,FLOAT>
);

CREATE TABLE IF NOT EXISTS finder_keyspace.tokens_index (
token_text TEXT PRIMARY KEY,
cf INT,
url_df INT,
url_pos MAP<INT,TEXT>,
url_tf MAP<INT,INT>,
url_tfidf MAP<INT,FLOAT>,
);

CREATE TABLE finder_keyspace.inverted_index (
token_text TEXT PRIMARY KEY,
collection_freq INT,
idf FLOAT,
count_map MAP<INT, INT>,
tfidf_map MAP<INT, FLOAT>
);

CREATE INDEX ON finder_keyspace.finder_corpus(url_id);
CREATE INDEX ON finder_keyspace.finder_corpus(url);