# geo-ee

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6814244.svg)](https://doi.org/10.5281/zenodo.6814244)

This repository contains the code for my International Baccalaureate Geography Extended Essay (May 2022 examinations).

The original paper submitted to the IBO are available to download [here](https://doi.org/10.5281/zenodo.6814244), licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

To view main project file, resolve the missing datasets in the [remarks](#remarks) and open the main [QGIS](https://qgis.org/en/site) project file [here](gis/main.qgz).

## Abstract
Since the industrialisation of Hong Kong, the territory has observed a shortage in parking supply, resulting from the steady increase in car ownership and the declining growth rate in the number of parking spaces. This investigation focuses on providing a more solid understanding of the relationship between the spatial distribution of parking spaces and the local traffic in urban areas of Hong Kong, through on-site surveys and the Ga2SFCA method, so to build a more resilient and sustainable transport system.

## Technologies
The high-level overview of the methodology is as follows (see Section 5 of the paper for more details):

![flowchart](img/flowchart.png)

The OD matrix is first generated using the [QNEAT3](https://github.com/root676/QNEAT3) plugin for [QGIS](https://github.com/qgis/QGIS). This is stored in an sqlite database ([graph/main/db/data.db](graph/main/db/data.db)), which is then accessed by the Ga2SFCA algorithm using [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) ([graph/main/db/common.py](graph/main/db/common.py)). The rest of the data processing and analysis is performed using QGIS, Python and Excel.

## uh...

this is what happened when i realised that my 75% done EE is corrupted:

![me](img/me.png)

## Remarks
The following files are excluded from the repo:
- `gis/iB1000.gdb` - [download here](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-development-hkms-digital-b1k/resource/a3aa069d-9f40-460c-87bf-486b49173846)
- `gis/iC1000.gdb` - [download here](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-development-hkms-digital-c1k/resource/912f3e55-fc69-432c-9d5e-3a64b8ec28ea)
- `gis/iB5000.gdb` - [download here](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-development-hkms-digital-b5k/resource/83c666df-a740-46bd-908c-0283e8f56bc7)
- `gis/dTAD_IRNP.gdb` - [download here](https://data.gov.hk/en-data/dataset/hk-td-tis_16-traffic-aids-drawings-v2/resource/0f157998-acc9-4fbd-b559-da94e4b5b221)
- `gis/all/mtr.tif` - missing, extract it from iB1000 map, perform KDE in QGIS.
- `gis/all/kmb.tif` - convert the [JSON file](https://data.gov.hk/en-data/dataset/hk-td-tis_21-etakmb/resource/059d4c98-3573-46fe-96a1-5f680c7f9afa), perform KDE in QGIS.
- `gis/all/dtm.tif` - too large, convert the [ASC file](https://data.gov.hk/en-data/dataset/hk-landsd-openmap-5m-grid-dtm/resource/1c01fbe1-4c24-49ef-af00-8fdd0c9661f4) to TIF.
- `main.docx` - too large (210.153MB)

The following files are compressed:
- `gis/all/buildings_all.zip` - extract it.