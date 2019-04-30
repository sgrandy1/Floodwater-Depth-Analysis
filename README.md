# RI-Floodwater-Depth-Tools
*Python Toolbox for Floodwater Depth Analysis of Rhode Island Coast*

This repository contains tools that can be used to calculate floodwater depth of 100 year floods along the Rhode Island coast and additional feet of flooding from a given sea level rise scenario. The tools produce two water depth raster datasets:

**FEMA Water Depth:** Based on FEMA BFE (base flood elevation) from FEMA Flood Hazards data and ground elevation data from an input DEM

**Depth Difference:** Based on FEMA floodwater depth output and input floodwater depth from a given sea level rise scenario. Floodwater depth for various sea level scenarios were created by the Coastal Resources Center for their STORMTOOLS web map application. The CRC floodwater depth is based on new BFE datat they calculated through STORMTOOL models; it is referred to as "Suggested Design Elevation" (SDE) to avoid confusion with existing FEMA BFE maps.



