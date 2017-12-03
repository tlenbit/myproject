''' copy artist and tracks data from musicbrainz db csv dump: '''
sudo su - postgres
\connect musicbrainz
\copy (select id, name from artist) to '/tmp/artist_dump.csv' with csv header delimiter ';';
\copy (select id, name from track) to '/tmp/track_dump.csv' with csv header delimiter ';';
\copy (select * from artist_track) to '/tmp/artist_track_dump.csv' with csv header delimiter ';';

''' make webpack bundle ''' 
npm run build
