# **********************************************************************************************************************
# Python Toolbox for Floodwater Depth Analysis of Rhode Island Coast
#
# Description: This toolbox includes three different tools that can be utilized in ArcMap for calculating water depth
# based on FEMA BFE (base flood elevation) and ground elevation, and calculating additional feet of floodwater from
# varying sea level rise scenarios for the state of Rhode Island. Sea level rise floodwater depth based on SDE
# (suggested design elevation) data created by Coastal Resources Center.
#
# Author: Sean Grandy, 4/30/2019
# All tools released under MIT license, and no warranty is implied
#
# Example data included with Toolbox: FEMA_Flood_Hazard_Areas.shp, South_Kingstown_Boundary.shp, skdem, slr3_depth
# **********************************************************************************************************************


# Import arcpy modules
import arcpy


# Script for creating toolbox
class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Python Toolbox: Floodwater Depth Analysis"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [FEMAClip, FEMA_BFE, Depth]


# Script for first tool
class FEMAClip(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Step 1: FEMA AOI Clip"
        self.description = "This tool projects the FEMA Flood Hazards feature class for Rhode Island into Rhode " \
                           "Island State Plane Feet. The projected feature class is then clipped to the input area " \
                           "of interest boundaries."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        workspace = arcpy.Parameter(name="Workspace",
                                     displayName="Work Space (for intermediate files)",
                                     datatype="DEWorkspace",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        params.append(workspace)
        fema_floodzones = arcpy.Parameter(name="FEMA_FloodZones",
                                     displayName="FEMA Flood Zones",
                                     datatype="DEFeatureClass",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        params.append(fema_floodzones)
        aoi_boundary = arcpy.Parameter(name="AOI_Boundary",
                                        displayName="Area of Interest",
                                        datatype="DEFeatureClass",
                                        parameterType="Required",  # Required|Optional|Derived
                                        direction="Input",  # Input|Output
                                        )
        params.append(aoi_boundary)
        fema_aoi_clip = arcpy.Parameter(name="FEMA_AOI_Clip",
                                 displayName="FEMA Area of Interest Clip",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(fema_aoi_clip)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # Import os for creating temporary files
        import os

        # Set variables
        workspace = parameters[0].valueAsText
        fema_floodzones = parameters[1].valueAsText
        aoi_boundary = parameters[2].valueAsText
        fema_aoi_clip = parameters[3].valueAsText

        # Process: Project to RI State Plane Feet
        arcpy.Project_management(fema_floodzones, os.path.join(workspace, "Temp.shp"),
                                 "PROJCS['NAD_1983_StatePlane_Rhode_Island_FIPS_3800_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],PARAMETER['False_Easting',328083.3333333333],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',-71.5],PARAMETER['Scale_Factor',0.99999375],PARAMETER['Latitude_Of_Origin',41.08333333333334],UNIT['Foot_US',0.3048006096012192]]",
                                 "WGS_1984_(ITRF00)_To_NAD_1983",
                                 "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]",
                                 "NO_PRESERVE_SHAPE", "", "NO_VERTICAL")

        # Check to see if temporary projected shapefile exists
        if arcpy.Exists(os.path.join(workspace, "Temp.shp")):
            print "FEMA Flood Zones projected!"

        # Process: Clip projected shapefile to area of interest
        arcpy.Clip_analysis(in_features=os.path.join(workspace, "Temp.shp"),
                            clip_features=aoi_boundary,
                            out_feature_class=fema_aoi_clip,
                            cluster_tolerance="")

        # Check to see if FEMA Flood Hazard Zones AOI clip shapefile exists, and delete temporary shapefile if it does
        if arcpy.Exists(fema_aoi_clip) :
            print "FEMA Area of Interest Clip created!"
            print "Deleting intermediate files"
            arcpy.Delete_management(os.path.join(workspace, "Temp.shp"))

        return


# Script for second tool
class FEMA_BFE(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Step 2: FEMA BFE"
        self.description = "This tool takes the FEMA area of interest clip output from Step 1 and converts the " \
                           "feature class into a base flood elevation raster dataset based on the attribute " \
                           "'STATIC_BFE'. This raster dataset is then reclassified to remove areas that do not " \
                           "undergo flooding. NOTE: FEMA BFE raster dataset that is created has a pixel size of 30."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        workspace = arcpy.Parameter(name="Workspace",
                                     displayName="Workspace (for intermediate files)",
                                     datatype="DEWorkspace",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        params.append(workspace)
        fema_aoi_clip = arcpy.Parameter(name="FEMA_aoi_clip",
                                 displayName="FEMA Area of Interest Clip",
                                 datatype="DEFeatureClass",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Input",  # Input|Output
                                 )
        params.append(fema_aoi_clip)
        fema_bfe = arcpy.Parameter(name="FEMA_BFE",
                                 displayName="FEMA Base Flood Elevation (reclassified)",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(fema_bfe)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # Import os to store temporary files
        import os

        # Set variables
        workspace = parameters[0].valueAsText
        fema_aoi_clip = parameters[1].valueAsText
        fema_bfe = parameters[2].valueAsText

        # Process: Convert FEMA area of interest clip feature class to FEMA BFE raster dataset
        arcpy.FeatureToRaster_conversion(fema_aoi_clip, "STATIC_BFE", os.path.join(workspace, "Temp"), "30")

        # Check to see if temporary FEMA BFE raster dataset was created
        if arcpy.Exists(os.path.join(workspace, "Temp")):
            print "FEMA BFE raster created!"

        # Process: Reclass to remove zones that have no flooding
        arcpy.gp.Reclassify_sa(os.path.join(workspace, "Temp"), "VALUE", "-9999 NODATA", fema_bfe, "DATA")

        # Check to see if corrected, reclassified FEMA BFE exists and delete temporary FEMA BFE if it does
        if arcpy.Exists(fema_bfe) :
            print "FEMA BFE reclassified!"
            print "Deleting intermediate files"
            arcpy.Delete_management(os.path.join(workspace, "Temp"))

        return


# Script for third tool
class Depth(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Step 3: Depth and Depth Diff"
        self.description = "This tool uses the FEMA Base Flood Elevation raster dataset from Step 2 to produce two " \
                           "floodwater depth raster datasets. The first raster dataset showcases floodwater depth " \
                           "based on the difference of FEMA BFE and the input DEM raster. The second raster dataset " \
                           "showcases additional floodwater depth from a given sea level rise scenario based on " \
                           "the difference of the input sea level rise floodwater depth and the FEMA floodwater " \
                           "depth output. NOTE: input raster datasets should have a pixel size of 30 to undergo " \
                           "raster calculations with FEMA BFE from Step 2."
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = []
        workspace = arcpy.Parameter(name="Workspace",
                                     displayName="Workspace (for output)",
                                     datatype="DEWorkspace",
                                     parameterType="Required",  # Required|Optional|Derived
                                     direction="Input",  # Input|Output
                                     )
        params.append(workspace)
        fema_bfe = arcpy.Parameter(name="FEMA_BFE",
                                 displayName="FEMA Base Flood Elevation (reclassified)",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Input",  # Input|Output
                                 )
        params.append(fema_bfe)
        dem = arcpy.Parameter(name="DEM",
                                 displayName="Area of Interest DEM (elevation data)",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Input",  # Input|Output
                                 )
        params.append(dem)
        slr_depth = arcpy.Parameter(name="SLR_Depth",
                                 displayName="Sea Level Rise Floodwater Depth",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Input",  # Input|Output
                                 )
        params.append(slr_depth)
        depth_diff = arcpy.Parameter(name="Depth_Diff",
                                 displayName="SLR and FEMA Depth Difference",
                                 datatype="DERasterDataset",
                                 parameterType="Required",  # Required|Optional|Derived
                                 direction="Output",  # Input|Output
                                 )
        params.append(depth_diff)
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""

        # Import os to store intermediate output
        import os

        # Set variables
        workspace = parameters[0].valueAsText
        fema_bfe = parameters[1].valueAsText
        dem = parameters[2].valueAsText
        slr_depth = parameters[3].valueAsText
        depth_diff = parameters[4].valueAsText

        # Process: Raster Calculator (FEMA floodwater depth from difference of FEMA BFE and ground elevation)
        arcpy.gp.RasterCalculator_sa(str('"' + str(fema_bfe) + '" - "' + str(dem) + '"'), os.path.join(workspace, "FEMA_depth"))

        # Check to see if FEMA floodwater depth raster created
        if arcpy.Exists(os.path.join(workspace, "FEMA_depth")):
            print "FEMA water depth raster created!"

        # Process: Raster Calculator (depth difference from SLR scenario floodwater depth and FEMA floodwater depth)
        arcpy.gp.RasterCalculator_sa(str('"' + str(slr_depth) + '" - "' + str(os.path.join(workspace, "FEMA_depth")) + '"'), depth_diff)

        # Check to see if floodwater depth difference of SLR and FEMA created
        if arcpy.Exists(depth_diff):
            print "Depth difference raster created!"

        return

