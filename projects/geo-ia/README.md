# geo-ia

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6814252.svg)](https://doi.org/10.5281/zenodo.6814252)

This repository contains the code for my International Baccalaureate Geography Internal Assessment (May 2022 examinations).

The original paper submitted to the IBO can be downloaded [here](https://doi.org/10.5281/zenodo.6814252), licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

To view main project file, resolve the missing datasets in the [remarks](#remarks) and open the main [QGIS](https://qgis.org/en/site) project file [here](section3/gis/main.qgz).

## Abstract
With land in Hong Kong generally sold to the highest bidder, the land value is often argued to increase closer to the PLVI. By using building heights along four transects as a proxy indicator for the land value, this paper attempts to explore to what extent does Hong Kong fit this pattern, and verify whether land use models (Burgess Model, Hoyt Model, Functional Zone Model) apply.

## Documentation

Apologies for the messy code - the repository is very roughly structured by the section number in the paper.

### Technologies used

- Python (pyproj, fastkml, shapely, bs4)
- HTML, CSS, JS (ArcGIS JS API)
- QGIS 3.20, Google MyMaps, Google Earth, KML
- Google Sheets (Google Visualization API Query Language)
- MS Excel, PowerPoint, Word

### Section 1 - Introduction

[`findProperty.py`](section1/findProperty.py) calls the CentaMap API to retrieve all buildings in Hong Kong sorted by the current unit price. The separate API calls are then [merged](section1/merge.py) and [converted](section1/analyse.py) to [`analysed.csv`](section1/analysed.csv). The number of floors are then [retrieved](section1/getBldHeight.py) with a separate API.

The building geometries within a specified district code are then visualised in a [KML file](section1/test.kml) using [`master.py`](section1/master.py). Data is used for a quick pilot study.

### Section 2 - Methodology

For each transect:
1. The route is first drawn using [GeoInfo Map](https://www.map.gov.hk/gm/) or Google Earth to a [KML file](section2/0_raw.kml)
2. [`1_separate.py`](section2/1_separate.py) automatically splits the route into regular 200m intervals with lerp, adds markers at each point, outputting it to [`1_separated.kml`](section2/1_separated.kml).
3. [`2_getSurroundingBuildings.py`](section2/2_getSurroundingBuildings.py) probes for buildings in the 20m/40m vicinity of the marker, at 45° regular intervals by querying the government iB1000 HKMS database, outputting it to [`2_buildings.kml`](section2/2_buildings.kml).
4. [`3_getBuildingHeight_new_2.py`](section2/3_getBuildingHeight_new_2.py) retrieves the height (roofLevel - baseLevel), name and geometry for each building, and outputting it to [`3_buildings_geometry.kml`](section2/3_buildings_geometry.kml).
5. [`4_analyse.py`](section2/4_analyse.py) outputs the average valid building heights to [`4_analysed.csv`](section2/4_analysed.csv).

The results are then compiled for all transects and visualised using a [static website](section2/all/all.html).

### Section 3 - Data Presentation

[`ib1000/getStoreys.py`](section3/ib1000/getStoreys.py) scrapes the government's [BMIS](https://bmis2.buildingmgt.gov.hk/bd_hadbiex/home.jsf) database to retrieve the registered floor count and official english name for each building. In case it fails to return the building using the name, the official address is used instead ([queried](section3/getAddress/getAddress.py) with the [OGCIO address lookup API](https://data.gov.hk/en-data/dataset/hk-ogcio-st_div_02-als)).

SRCC and other coarse data manipulations are performed in a Google Sheet with `QUERY()` commands. Graphs are generated using MS Excel.

### Section 4 - Data Presentation/Conclusion/Evaluation

The following operations are performed with [QGIS](https://qgis.org/):

- KMLs that store the building geometries and average heights along the transect (see Section 2) are visualised using [`QgsInterpolatedLineSymbolLayer`](https://api.qgis.org/api/3.20/classQgsInterpolatedLineSymbolLayer.html);

- City-wide building geometries are loaded to demonstrate the role of [urban design guidelines and strategic viewpoints](https://www.pland.gov.hk/pland_en/tech_doc/hkpsg/full/pdf/ch11.pdf) as being a limiting factor to horizontal urban sprawl;

- Simplified [iC1000 land use data](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-development-hkms-digital-c1k) is used to demonstrate the socio-economic implications of select areas;

- Normalised building height restriction data is extracted from the [Outline Zoning Plans](https://www.pland.gov.hk/pland_en/info_serv/digital_planning_data/download.htm) to demonstrate physical constraints to the building height;

- [Average household median income data](https://www.bycensus2016.gov.hk/data/LSBG_16BC.xlsx) matched with the corresponding regions in the [PPU/SPU/TPU GML file](https://data.gov.hk/en-data/dataset/hk-pland-pland1-boundaries-of-tpu-sb-vc) is used to explain the disparities/outliers in the land value;

- list of bus stops and MTR stations are filtered from the [iGeoCom maps](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-development-hkms-digital-geocom) to generate their own Kernel Density Estimations (KDE) of the transport accessibility.

- [5m DTM](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-5m-grid-dtm) used is visualise the terrain in HK with a raster layer.

## Remarks
The following files are compressed/missing:

- `section3/gis/shapefiles/buildings_all.zip` - extract it.
- `section3/gis/shapefiles/GeoCom.zip` - extract it.
- `section3/gis/shapefiles/S_buildings_geometry_old.zip` - extract it.
- `section3/gis/shapefiles/W_buildings_geometry_old.zip` - extract it.
- `section3/gis/iB1000.gdb` - [download here](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-development-hkms-digital-b1k/resource/a3aa069d-9f40-460c-87bf-486b49173846), relink the path in QGIS.
- some datasets are shared with my [geography EE](https://github.com/abc8747/ibo), if there are any missing datasets follow the `Remarks` section in the README.