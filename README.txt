# East Sarajevo Digital Twin - SUMO Project Package

This ZIP is a **ready project skeleton** for your CCAM2ZERO pilot.

## What is included
1. A **toy test network** that you can build locally with `netconvert`
2. A **working test scenario** (`east_sarajevo_test.sumocfg`)
3. Your **real measurement points** exported from Excel
4. A **detector template** for mapping real East Sarajevo points to SUMO edges
5. Dashboard KPI template and workflow notes

## What is still needed for the real pilot
Because SUMO binaries are not available in this environment, the final `network.net.xml` for the **real East Sarajevo road network** must be generated locally on your machine from OSM or NetEdit.

## Quick start
### Windows
1. Install SUMO
2. Open `2_network/build_network.bat`
3. Run `run_test_scenario.bat`

### Linux
1. Install SUMO
2. `bash 2_network/build_network.sh`
3. `bash run_test_scenario.sh`

## Next step for the real pilot
- Replace the toy network with East Sarajevo OSM network
- Fill `SUMO_edge_id`, `SUMO_lane_id`, `SUMO_pos_m` for each real measurement point
- Generate real detectors with `scripts/generate_detectors_from_excel.py`
