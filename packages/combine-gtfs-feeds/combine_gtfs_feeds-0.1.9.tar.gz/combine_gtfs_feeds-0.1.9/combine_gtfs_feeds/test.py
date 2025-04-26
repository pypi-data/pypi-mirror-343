from combine_gtfs_feeds import cli
import pandas as pd
#my_path = r"W:\gis\projects\OSM\Transit\Transit_2023\feeds"
#my_date = 20230321

# my_path = r"C:\Stefan\gtfs_2024\raw_gtfs"
# my_date = 20250107
# output_path = r"T:\2025Q1\Kris\GTFS_2024\combined"

# test = cli.run.combine(
#     my_path, my_date, output_path
# )

gtfs_dir_2050 = r'X:\Trans\Transit\2026 RTP\Transit Network Data\GTFS\2050'
output_dir = r'C:\Users\scoe\Puget Sound Regional Council\GIS - Sharing\Projects\RTP_Transit\combined_2050'

test = cli.run.combine(gtfs_dir_2050, 20250408, output_dir)

print ('done')
