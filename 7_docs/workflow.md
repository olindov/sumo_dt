# Digital Twin Workflow - East Sarajevo

## Objective
Build a repeatable workflow from measurement points in QGIS to SUMO calibration and KPI monitoring.

## Package contents
- `1_input/sensors/east_sarajevo_measurement_points.csv` - imported from your Excel file
- `2_network/plain/*` - toy test network definition
- `3_demand/routes_test.rou.xml` - one-hour test scenario
- `4_detectors/detectors_test.add.xml` - working detectors for toy network
- `4_detectors/detectors_from_measurement_points_template.add.xml` - template to map your real points
- `scripts/generate_detectors_from_excel.py` - helper for your real detector file

## Workflow
1. Correct and validate measurement-point coordinates in QGIS.
2. Snap points to nearest road and identify road direction.
3. Export OSM network for East Sarajevo.
4. Convert OSM to SUMO using `netconvert`.
5. Open the resulting `.net.xml` in NetEdit.
6. For each measurement point, record:
   - `SUMO_edge_id`
   - `SUMO_lane_id`
   - `SUMO_pos_m`
7. Update the spreadsheet / CSV and generate final `detectors.add.xml`.
8. Calibrate flows using observed counts by peak period.
9. Run baseline, stress-test, and intervention scenarios.
10. Export KPIs for dashboarding.

## Suggested real-world scenarios
- AM peak (07:00-09:00)
- PM peak (15:00-17:00)
- School peak
- Weekend / seasonal corridor to Pale
- Incident diversion / work zone
