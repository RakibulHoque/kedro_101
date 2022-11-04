### Useful link
https://nithanaroy.medium.com/create-your-own-tile-server-and-map-client-5f7515fff28
https://atmamani.github.io/cheatsheets/open-geo/geopandas-4/
https://help.openstreetmap.org/questions/40080/osmconvert-csv-and-relations-ways
https://stackoverflow.com/questions/36054926/osmosis-get-all-nodes-ways-relations-with-the-same-tags
https://manpages.ubuntu.com/manpages/focal/man1/osmconvert.1.html
https://github.com/openstreetmap/osmosis/blob/main/doc/detailed-usage.adoc#used-way-uw

## Geofabrik
https://download.geofabrik.de/asia/bangladesh.html

## Osmosis
https://github.com/openstreetmap/osmosis/releases/download/0.48.3/osmosis-0.48.3.zip

### steps:
- download zipfile
- move it to a folder and unzip
- copy the bin path and add it to path variable of os
- restart the terminal (in case of vscode: close and open)
- write osmosis to check if add to path is correct
- example command: `osmosis --rbf osm/data/bangladesh-latest.osm.pbf --nk keyList="amenity" --wx osm/data/amenity.osm` extracts to amenity tags

#### Converting elements to nodes:
```
osmconvert64-0.8.8p.exe --all-to-nodes --max-objects=500000000 bangladesh-latest.osm.pbf -o=bangladesh-latest-allnodes.osm.pbf
```
#### Filtering nodes to POIs:
```
osmosis --rbf osm/data/bangladesh-latest-allnodes.osm.pbf --tf accept-nodes addr:housenumber=* addr:housename=* addr:flat=* addr:flats=* addr:unit=* addr:conscriptionnumber=* addr:streetnumber=* addr:street=* addr:place=* addr:postbox=* addr:postcode=* addr:city=* addr=* addr:full=* addr:town=* addr:quarter=* addr:suburb=* addr:subdistrict=* addr:district=* addr:province=* addr:region=* addr:state=* addr:county=* addr:country=* amenity=* source:name=* name=* name:en=* name:bn=* name:left=* name:right=* int_name=* int_name:en=* int_name:bn=* loc_name=* loc_name:en=* loc_name:bn=* nat_name=* nat_name:en=* nat_name:bn=* official_name=* official_name:en=* official_name:bn=* old_name=* reg_name=* reg_name:en=* reg_name:bn=* short_name=* short_name:en=* short_name:bn=* sorting_name=* alt_name=* --tf reject-ways --tf reject-relations --wx osm/data/poinode.osm.pbf
```
#### Converting POIs pbf to csv:
```
osmconvert64-0.8.8p.exe --max-objects=500000000 poinode.osm.pbf -o=poinode.csv --csv="@id @lon @lat name addr:city addr:postcode addr:district amenity place addr:street addr:country addr:housenumber building:material name:en addr:union addr:ward addr:province addr:division addr:subdistrict addr:state name:bn addr:suburb addr:word addr:neighbourhood addr:place alt_name addr:housename" --csv-headline --csv-separator=,
```