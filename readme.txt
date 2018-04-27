The app is intended to share playlists (host is playing top track in real life) for people who are physically in the same room with ability to vote for tracks and add new ones


''' copy artist and tracks data from musicbrainz db csv dump: '''
sudo su - postgres
\connect musicbrainz
\copy (select id, name from artist) to '/tmp/artist_dump.csv' with csv header delimiter ';';
\copy (select id, name from track) to '/tmp/track_dump.csv' with csv header delimiter ';';
\copy (select * from artist_track) to '/tmp/artist_track_dump.csv' with csv header delimiter ';';

''' copy from csv to table '''
\copy artist from '/tmp/artist_dump.csv' DELIMITERS ';' CSV;
\copy track from '/tmp/track_dump.csv' DELIMITERS ';' CSV;
\copy artist_track from '/tmp/artist_track_dump.csv' DELIMITERS ';' CSV;

''' make webpack bundle ''' 
npm run build

''' make all names unaccent '''
update artist set name = unaccent(name);
update track set title = unaccent(title);

''' indexes '''
# used in WHERE awdawdaw='awdawdaw'
create index artist_name_idx on artist(name);
create index track_title_idx on track(title);

# use gin when row values won't change
# use gist if they will
CREATE INDEX artist_name_simple_fts_idx ON artist USING GIN (to_tsvector('simple', name));
CREATE INDEX track_title_simple_fts_idx ON track USING GIN (to_tsvector('simple', title));

# delete duplicates from artist_track like this one:
#         ARTIST                  ARTIST_TRACK              TRACK
#-----------------------------------------------------------------------
#    id         name    |  id   artist_id track_id |   id      title
#-----------------------------------------------------------------------
#    ...         ...    | ...       ...      ...   |   ...      ...
#     1        Hendrix  | 123        1        5    |    5     Hey Joe
#     2        Hendrix  | 124        2        5    |   ...     ...
#    ...         ...    | ...       ...      ...   |   ...     ... 
#
join artist, track and artist_track, then delete duplicate (title, name) pairs
https://wiki.postgresql.org/wiki/Deleting_duplicates
then normalize again
insert into artist (id, name) select distinct artist_id, name from artist_track_tmp;
insert into track (id, title) select distinct track_id, title from artist_track_tmp;




# don't use trigram, fts is more stable

# django uses 
# UPPER(col) LIKE upper('%awdawd%')
# instead of
# col ilike '%awdawd%'
# because it is somewhat faster
create extension pg_trgm;
CREATE INDEX track_title_upper_trgm_idx ON track USING gin (upper(title) gin_trgm_ops);
CREATE INDEX artist_name_upper_trgm_idx ON artist USING gin (upper(name) gin_trgm_ops);

# django orm translates somequery[:42] into LIMIT 42. 
# 42 is small and postgres planner uses SEQUENTIAL SCAN (_-~?!wtf!?~-_)
# (which is VERY slow), rather than bitmap index

# disable seqscan for testing only
SET enable_seqscan = OFF;
# this doesn't turn seqscan completly and it still will be used as last resort
# bitmap trgm index is slow on 1-2-3 length queries, but seqscan is fast
