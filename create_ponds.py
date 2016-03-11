# Import system modules
import arcpy
from arcpy import env
import sys
import random
import posixpath as os

# checkout spatial analyst
if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.AddMessage("Checking out Spatial")
    arcpy.CheckOutExtension("Spatial")
else:
    arcpy.AddError("Unable to get spatial analyst extension")
    arcpy.AddMessage(arcpy.GetMessages(0))
    sys.exit(0)

# input_dir = 'E:/_data/welikia/beaver_ponds'
#
# # environment settings
# env.overWriteOutput = True

# Inputs
# streams = "E:/_data/welikia/beaver_ponds/WELIKIA_STREAMS_SYNTHESIS_NO_CREEKS/WELIKIA_STREAMS_SYNTHESIS_NO_CREEKS.shp"
# DENSITY = 2.0
#
#
# '''
# Calculate number of ponds in landscape
# '''
# def number_of_ponds(density, streams):
#     cursor = arcpy.SearchCursor(streams)
#
#     total_stream_length = 0
#
#     for row in cursor:
#         total_stream_length += row.getValue('length')
#
#     return int(total_stream_length / 1000 * density)
#
#
# ponds = .4 * 1214
#
#


#
# assign_pond_locations(constraint=streams, num_points=ponds)

# PARAMETERS
DISTANCE = 800
CELL_SIZE = 5


def assign_pond_locations(constraint, num_points):

    """
    assign random locations for each pond that fall within the bounds of suitable habitat
    """

    # constraint is the area of all suitable loacations for ponds
    # num_points is the maximum number of ponds that should be assigned
    arcpy.CreateRandomPoints_management(out_path="E:/_data/welikia/beaver_ponds/_test/outputs/",
                                        out_name="pond_points.shp",
                                        constraining_feature_class=constraint,
                                        number_of_points_or_field=num_points,
                                        minimum_allowed_distance=1000)


def dam_points_coordinates(points):

    """
    take points shp and convert to X Y coordinate tuples
    """

    cursor = arcpy.da.SearchCursor(points, 'SHAPE@XY')

    coordinate_list = []
    for point in cursor:
        # print point[0]
        coordinate_list.append((point[0][0], point[0][1]))

    return coordinate_list


def create_pond(dem, flow_direction, coordinates, temp_point):

    """
    create pond raster
    """

    pour_point = arcpy.Point(coordinates[0], coordinates[1])

    arcpy.CopyFeatures_management(in_features=arcpy.PointGeometry(pour_point),
                                  out_feature_class=temp_point)

    # print type(pour_point)
    # get pour point elevation
    pour_point_elevation = arcpy.sa.ExtractByPoints(points=pour_point,
                                                    in_raster=dem)
    # print pour_point_elevation.maximum

    # set dam height
    dam_height = pour_point_elevation.maximum + 9
    # print dam_height

    # calculate watershed for dam
    watershed = arcpy.sa.Watershed(in_flow_direction_raster=flow_direction,
                                   in_pour_point_data=temp_point)

    # calculate flooded area
    pond = arcpy.sa.Con(watershed == 0, arcpy.sa.Con((arcpy.Raster(dem) <= dam_height), dam_height, 0))

    pond = arcpy.sa.Con(arcpy.sa.IsNull(pond), 0, pond)

    return pond


def sum_ponds(pond_dir):
    # sum ponds into single raster
    env.workspace = os.join(pond_dir)

    print env.workspace

    l = arcpy.ListRasters()

    sum = arcpy.Raster(l[0])

    for r in l[1:]:
        print r
        sum += arcpy.Raster(r)

    sum_ponds_binary = arcpy.sa.Con(sum > 0, 1, 0)

    return sum_ponds_binary


def ponds_to_landcover(ponds, landcover):
    # arcpy.env.workspace = os.join(output_dir)
    #
    # l = arcpy.ListRasters()
    #
    # sum = arcpy.Raster(l[0])
    #
    # for r in l[1:]:
    #     print r
    #     sum += arcpy.Raster(r)
    #
    # sum_pond_binary = arcpy.sa.Con(sum > 0, 1, 0)

    landcover = arcpy.sa.Con(ponds == 1, 1,landcover)
    return landcover


def calculate_territory(landcover):

    """
    calculate territory
    """

    landcover_set_null = arcpy.sa.SetNull((landcover == 2) | (landcover == 3), 1)

    territory = arcpy.sa.EucDistance(in_source_data=landcover_set_null,
                                     maximum_distance=DISTANCE,
                                     cell_size=CELL_SIZE)

    exclude_territory = arcpy.sa.IsNull(territory)

    return exclude_territory


def count_ponds(ponds, year):

    """
    count the current number of beaver ponds
    """

    # sum_ponds = arcpy.Raster(in_raster)
    print 'setting null'
    sum_ponds_set_null = arcpy.sa.SetNull(ponds != 1, 1)
    sum_ponds_set_null.save('E:/_data/welikia/beaver_ponds/_test/outputs/ponds_set_null_%s.tif' % year)

    print 'region grouping'
    region_group = arcpy.sa.RegionGroup(in_raster=sum_ponds_set_null,
                                        number_neighbors='EIGHT',
                                        zone_connectivity='CROSS')

    region_group.save('E:/_data/welikia/beaver_ponds/_test/outputs/region_group_%s.tif' % year)
    print 'getting count'
    pond_count = arcpy.GetRasterProperties_management(in_raster=region_group,
                                                      property_type='UNIQUEVALUECOUNT')

    pond_count = int(pond_count.getOutput(0))

    return pond_count, region_group


def calculate_suitability(streams, landcover, suitability_points):

    """
    calculate suitability points
    streams
    landcover
    suitability_points
    """
    if type(streams) == str:
        streams = arcpy.Raster(streams)

    if type(landcover) == str:
        landcover = arcpy.Raster(landcover)

    exclude_territory = calculate_territory(landcover)

    suitability_surface = exclude_territory * streams

    suitability_surface_set_null = arcpy.sa.SetNull(suitability_surface, suitability_surface, "VALUE = 0")

    arcpy.RasterToPoint_conversion(in_raster=suitability_surface_set_null,
                                   out_point_features=suitability_points)


def initial_time_since_disturbance(in_raster, landcover):

    """
    calculate random age
    """

    pond_count = in_raster

    arcpy.AddField_management(in_table=pond_count,
                              field_name='age',
                              field_type='SHORT')

    cursor = arcpy.UpdateCursor(pond_count)

    for row in cursor:
        age = random.randint(0,9)
        row.setValue("age", age)
        cursor.updateRow(row)

    age = arcpy.sa.Lookup(in_raster=pond_count,
                          lookup_field="age")

    start_age = arcpy.sa.Con((arcpy.sa.IsNull(pond_count) == 1) & (landcover), 30,
                             arcpy.sa.Con(pond_count, age))

    return start_age


def update_time_since_disturbance(time_since_disturbance, new_ponds):

    time_since_disturbance = arcpy.sa.Con(time_since_disturbance,
                                          arcpy.sa.Con(new_ponds == 1, 1, time_since_disturbance))

    return time_since_disturbance


def succession(age):

    """
    succession
    """

    landcover = arcpy.sa.Con(age >= 30, 3, (arcpy.sa.Con(age >= 10, 2, 1)))

    return landcover

