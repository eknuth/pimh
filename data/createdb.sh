createdb homeland -O homeland
createlang plpgsql homeland
psql -d homeland -f /usr/share/postgresql/8.4/contrib/postgis.sql
psql -d homeland -d homeland -f /usr/share/postgresql/8.4/contrib/spatial_ref_sys.sql 
psql homeland -c 'alter table geometry_columns owner to homeland'
psql homeland -c 'alter table spatial_ref_sys owner to homeland'
psql homeland -e -f data/srid.sql
