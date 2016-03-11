from create_ponds import *

# Directories
root_dir = 'E:/_data/welikia/beaver_ponds/_test'
input_dir = os.join(root_dir, 'inputs')
output_dir = os.join(root_dir, 'outputs')

# Environment Setting
env.workspace = root_dir
print env.workspace
env.scratchWorkspace = os.join(root_dir, 'Scratch_Geodatabase.gdb')
print env.scratchWorkspace
env.overWriteOutput = True

# Inputs
DEM = os.join(input_dir, 'UPLAND_DEM_BURNED_STREAMS_5m_FILL.tif')

flow_direction = os.join(input_dir, 'flow_direction.tif')

suitable_streams = os.join(input_dir, 'suitability_surface.tif')

time_since_disturbance = os.join(output_dir, 'time_since_last_disturbance_0.tif')
time_since_disturbance = arcpy.Raster(time_since_disturbance)
# landcover = os.join(input_dir, 'landcover.tif')

# Paths
suitability_points = os.join(input_dir, 'suitability_points.shp')

pond_points = os.join(output_dir, 'pond_points.shp')


# Model Parameters
CARRYING_CAPACITY = 5
MINIMUM_DISTANCE = 1000
for year in range(1, 5):

    print 'year %s trial start' % year



    print 'incrementing time since disturbance'
    time_since_disturbance = arcpy.sa.SetNull(time_since_disturbance <= 0, time_since_disturbance)

    time_since_disturbance += 1
    # time_since_disturbance.save(os.join(output_dir, 'time_since_last_disturbance_%s.tif' % (year + 10)))

    print 'updating landcover'
    landcover = succession(time_since_disturbance)

    print 'counting ponds...'
    pond_count, region_group = count_ponds(landcover, year)

    if pond_count < CARRYING_CAPACITY:
        print 'creating new ponds'
        new_ponds = CARRYING_CAPACITY - pond_count

        print 'calculating suitable points'
        # suitability_points = os.join(input_dir, 'suitability_points.shp')

        if arcpy.Exists(suitability_points):
            arcpy.Delete_management(suitability_points)

        calculate_suitability(landcover=landcover,
                              streams=suitable_streams,
                              suitability_points=suitability_points)

        # choose pond locations
        print 'selecting pond locations'
        # pond_points = os.join(output_dir, 'pond_points.shp')

        if arcpy.Exists(pond_points):
            arcpy.Delete_management(pond_points)

        assign_pond_locations(constraint=suitability_points,
                              num_points=new_ponds)

        # convert pond points feature to coordinate list
        print 'converting pond points to coordinate list'

        coordinate_list = dam_points_coordinates(pond_points)

        # create ponds
        pond_list = []
        for p, i in zip(coordinate_list, range(len(coordinate_list))):
            print 'calculating pond %s' % i
            temp_point = os.join(output_dir, 'temp_point.shp')

            if arcpy.Exists(temp_point):
                arcpy.Delete_management(temp_point)

            pond = create_pond(dem=DEM,
                               flow_direction=flow_direction,
                               coordinates=p,
                               temp_point=temp_point)

            pond_list.append(pond)
            # out_path = os.join(output_dir, 'ponds',('pond_%s.tif' % i))
            # pond.save(out_path)

        ponds = arcpy.sa.Con(arcpy.sa.CellStatistics(pond_list, 'SUM') > 0, 1, 0)
        # print 'ponds', type(ponds)

        ponds.save(os.join(output_dir, 'ponds_%s.tif' % year))

        print 'updating landcover'

        # landcover = arcpy.Raster(landcover)
        # print 'landcover', type(landcover)

        landcover = ponds_to_landcover(ponds=ponds,
                                       landcover=landcover)

        print 'updating time since disturbance'
        update_time_since_disturbance(time_since_disturbance, ponds)

        landcover.save(os.join(output_dir, 'landcover_%s.tif' % year))

        time_since_disturbance.save(os.join(output_dir, 'time_since_last_disturbance_%s.tif' % year))

    else:
        landcover.save(os.join(output_dir, 'landcover_%s.tif' % year))

        time_since_disturbance.save(os.join(output_dir, 'time_since_last_disturbance_%s.tif' % year))

