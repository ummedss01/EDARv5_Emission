# EDGARv5 Anthropogenic Emissions for Atmospheric Chemistry Transport Modeling

## Project Overview

This repository provides ready-to-use EDGARv5 anthropogenic emissions for atmospheric chemistry transport models (e.g., WRF-Chem, GEOS-Chem, CMAQ).  Sector- and pollutant-specific emissions are available from the EDGAR website.  Large-scale fire emissions are *not* included in this dataset, allowing users to incorporate fire emissions data from alternative sources (e.g., FINN, GFED) as needed.

## Data Source

Global sector- and pollutant-specific emissions are estimated by the Joint European Commission under the Emissions Database for Global Atmospheric Research (EDGAR) using a bottom-up methodology.  The data can be accessed at the [EDGARv5 website](https://edgar.jrc.ec.europa.eu/dataset_ap50).

## Tools

*   NCL scripts for data download
*   Python for data analysis
*   QGIS for visualization

## VOC Emission Estimation

EDGARv5 provides total NMVOC emissions, while EDGARv4.3 provides emissions for 25 individual VOC species.  To generate speciated VOC emissions for EDGARv5, the percentage distribution of the 25 VOC species in each grid cell from EDGARv4.3 was applied to the EDGARv5 NMVOC totals.  This approach assumes a similar spatial distribution of VOC species in EDGARv5 as in EDGARv4.3.

## Large-Scale Fire Emissions

Large-scale fire emissions are *not* included in this dataset.  Users should obtain fire emissions data from other sources, such as FINN or GFED, and incorporate them separately into their modeling simulations.

## Final EDGARv5 Emissions

The final emissions provided here are the sum of emissions from all sectors for each pollutant. These totals have been converted to kg m⁻² s⁻¹.

## Application to the Indian Region

These emissions were used in WRF-Chem simulations with the MOZART-MOSAIC, aqueous 4-bin (chem_opt=202) chemical mechanism over the Indian region for the year 2018. The results demonstrate the model's ability to simulate air pollution levels exceeding 550 µg/m³ over Delhi  (Saharan et al., 2024). Previous studies, using other emission inventories, have struggled to simulate concentrations above 250 µg/m³ without the use of nudging. The related publication can be found [here](https://www.sciencedirect.com/science/article/pii/S0269749124007279).

