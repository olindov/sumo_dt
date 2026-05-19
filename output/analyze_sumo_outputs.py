import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

EDGE_XML = "edge_data.xml"
TRIP_XML = "tripinfo.xml"

OUT_EDGE_CSV = "edge_data_parsed.csv"
OUT_TRIP_CSV = "tripinfo_parsed.csv"
OUT_KPI_CSV = "final_kpi_summary.csv"
OUT_TOP_EDGES = "top_congested_edges.csv"
OUT_TOP_TRIPS = "top_longest_trips.csv"
OUT_EDGE_TS = "edge_timeseries.csv"

def to_float(value, default=0.0):
    try:
        if value is None or value == "":
            return default
        return float(value)
    except Exception:
        return default

def parse_edge_data(xml_path: Path) -> pd.DataFrame:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    rows = []

    for interval in root.findall("interval"):
        begin = to_float(interval.get("begin"))
        end = to_float(interval.get("end"))
        interval_id = interval.get("id", "")

        for edge in interval.findall("edge"):
            rows.append({
                "interval_id": interval_id,
                "begin": begin,
                "end": end,
                "edge_id": edge.get("id", ""),
                "sampledSeconds": to_float(edge.get("sampledSeconds")),
                "traveltime": to_float(edge.get("traveltime")),
                "density": to_float(edge.get("density")),
                "occupancy": to_float(edge.get("occupancy")),
                "waitingTime": to_float(edge.get("waitingTime")),
                "speed": to_float(edge.get("speed")),
                "speedRelative": to_float(edge.get("speedRelative")),
                "departed": to_float(edge.get("departed")),
                "arrived": to_float(edge.get("arrived")),
                "entered": to_float(edge.get("entered")),
                "left": to_float(edge.get("left")),
                "laneChangedFrom": to_float(edge.get("laneChangedFrom")),
                "laneChangedTo": to_float(edge.get("laneChangedTo")),
            })

    return pd.DataFrame(rows)

def parse_tripinfo(xml_path: Path) -> pd.DataFrame:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    rows = []

    for trip in root.findall("tripinfo"):
        row = {
            "vehicle_id": trip.get("id", ""),
            "depart": to_float(trip.get("depart")),
            "departLane": trip.get("departLane", ""),
            "departPos": trip.get("departPos", ""),
            "departSpeed": to_float(trip.get("departSpeed")),
            "departDelay": to_float(trip.get("departDelay")),
            "arrival": to_float(trip.get("arrival")),
            "arrivalLane": trip.get("arrivalLane", ""),
            "arrivalPos": trip.get("arrivalPos", ""),
            "arrivalSpeed": to_float(trip.get("arrivalSpeed")),
            "duration": to_float(trip.get("duration")),
            "routeLength": to_float(trip.get("routeLength")),
            "waitingTime": to_float(trip.get("waitingTime")),
            "waitingCount": to_float(trip.get("waitingCount")),
            "stopTime": to_float(trip.get("stopTime")),
            "timeLoss": to_float(trip.get("timeLoss")),
            "rerouteNo": to_float(trip.get("rerouteNo")),
            "devices": trip.get("devices", ""),
            "vType": trip.get("vType", ""),
            "speedFactor": to_float(trip.get("speedFactor")),
            "vaporized": trip.get("vaporized", ""),
        }

        emissions = trip.find("emissions")
        if emissions is not None:
            row.update({
                "CO_abs": to_float(emissions.get("CO_abs")),
                "CO2_abs": to_float(emissions.get("CO2_abs")),
                "HC_abs": to_float(emissions.get("HC_abs")),
                "PMx_abs": to_float(emissions.get("PMx_abs")),
                "NOx_abs": to_float(emissions.get("NOx_abs")),
                "fuel_abs": to_float(emissions.get("fuel_abs")),
                "electricity_abs": to_float(emissions.get("electricity_abs")),
            })
        else:
            row.update({
                "CO_abs": 0.0,
                "CO2_abs": 0.0,
                "HC_abs": 0.0,
                "PMx_abs": 0.0,
                "NOx_abs": 0.0,
                "fuel_abs": 0.0,
                "electricity_abs": 0.0,
            })

        rows.append(row)

    return pd.DataFrame(rows)

def build_kpi_summary(edge_df: pd.DataFrame, trip_df: pd.DataFrame) -> pd.DataFrame:
    kpis = []

    if not edge_df.empty:
        kpis.extend([
            {"metric": "edge_num_rows", "value": len(edge_df)},
            {"metric": "edge_num_unique_edges", "value": edge_df["edge_id"].nunique()},
            {"metric": "edge_avg_speed", "value": edge_df["speed"].mean()},
            {"metric": "edge_avg_density", "value": edge_df["density"].mean()},
            {"metric": "edge_avg_occupancy", "value": edge_df["occupancy"].mean()},
            {"metric": "edge_avg_waiting_time", "value": edge_df["waitingTime"].mean()},
            {"metric": "edge_avg_traveltime", "value": edge_df["traveltime"].mean()},
            {"metric": "edge_total_entered", "value": edge_df["entered"].sum()},
            {"metric": "edge_total_left", "value": edge_df["left"].sum()},
            {"metric": "edge_avg_speed_relative", "value": edge_df["speedRelative"].mean()},
        ])

    if not trip_df.empty:
        kpis.extend([
            {"metric": "trip_num_completed_trips", "value": len(trip_df)},
            {"metric": "trip_avg_duration_s", "value": trip_df["duration"].mean()},
            {"metric": "trip_avg_route_length_m", "value": trip_df["routeLength"].mean()},
            {"metric": "trip_avg_waiting_time_s", "value": trip_df["waitingTime"].mean()},
            {"metric": "trip_avg_time_loss_s", "value": trip_df["timeLoss"].mean()},
            {"metric": "trip_avg_depart_delay_s", "value": trip_df["departDelay"].mean()},
            {"metric": "trip_total_waiting_time_s", "value": trip_df["waitingTime"].sum()},
            {"metric": "trip_total_time_loss_s", "value": trip_df["timeLoss"].sum()},
            {"metric": "trip_total_route_length_m", "value": trip_df["routeLength"].sum()},
            {"metric": "trip_avg_depart_speed_mps", "value": trip_df["departSpeed"].mean()},
            {"metric": "trip_avg_arrival_speed_mps", "value": trip_df["arrivalSpeed"].mean()},
            {"metric": "trip_total_CO2_abs", "value": trip_df["CO2_abs"].sum()},
            {"metric": "trip_total_fuel_abs", "value": trip_df["fuel_abs"].sum()},
            {"metric": "trip_total_NOx_abs", "value": trip_df["NOx_abs"].sum()},
        ])

    return pd.DataFrame(kpis)

def main():
    edge_path = Path(EDGE_XML)
    trip_path = Path(TRIP_XML)

    edge_df = pd.DataFrame()
    trip_df = pd.DataFrame()

    if edge_path.exists():
        edge_df = parse_edge_data(edge_path)
        if not edge_df.empty:
            edge_df.to_csv(OUT_EDGE_CSV, index=False, encoding="utf-8-sig")
            print(f"Generisan: {OUT_EDGE_CSV}")

            edge_df["time_min"] = edge_df["begin"] / 60.0
            edge_ts = (
                edge_df.groupby("time_min", as_index=False)
                .agg(
                    avg_speed=("speed", "mean"),
                    avg_density=("density", "mean"),
                    avg_waiting=("waitingTime", "mean"),
                    total_entered=("entered", "sum"),
                )
            )
            edge_ts.to_csv(OUT_EDGE_TS, index=False, encoding="utf-8-sig")
            print(f"Generisan: {OUT_EDGE_TS}")

            top_edges = (
                edge_df.groupby("edge_id", as_index=False)
                .agg(
                    mean_waiting=("waitingTime", "mean"),
                    mean_density=("density", "mean"),
                    mean_speed=("speed", "mean"),
                    total_entered=("entered", "sum"),
                )
                .sort_values(["mean_waiting", "mean_density"], ascending=[False, False])
            )
            top_edges.to_csv(OUT_TOP_EDGES, index=False, encoding="utf-8-sig")
            print(f"Generisan: {OUT_TOP_EDGES}")

            plt.figure(figsize=(10, 5))
            plt.plot(edge_ts["time_min"], edge_ts["avg_speed"])
            plt.xlabel("Vrijeme [min]")
            plt.ylabel("Prosječna brzina")
            plt.title("Prosječna brzina kroz vrijeme")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig("avg_speed_timeseries.png", dpi=200)
            plt.close()

            plt.figure(figsize=(10, 5))
            plt.plot(edge_ts["time_min"], edge_ts["avg_density"])
            plt.xlabel("Vrijeme [min]")
            plt.ylabel("Prosječna gustina")
            plt.title("Prosječna gustina kroz vrijeme")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig("avg_density_timeseries.png", dpi=200)
            plt.close()

            plt.figure(figsize=(10, 5))
            plt.plot(edge_ts["time_min"], edge_ts["avg_waiting"])
            plt.xlabel("Vrijeme [min]")
            plt.ylabel("Prosječno čekanje")
            plt.title("Prosječno vrijeme čekanja kroz vrijeme")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig("avg_waiting_timeseries.png", dpi=200)
            plt.close()

    else:
        print(f"Nije pronađen: {EDGE_XML}")

    if trip_path.exists():
        trip_df = parse_tripinfo(trip_path)
        if not trip_df.empty:
            trip_df.to_csv(OUT_TRIP_CSV, index=False, encoding="utf-8-sig")
            print(f"Generisan: {OUT_TRIP_CSV}")

            top_trips = trip_df.sort_values("duration", ascending=False).head(20)
            top_trips.to_csv(OUT_TOP_TRIPS, index=False, encoding="utf-8-sig")
            print(f"Generisan: {OUT_TOP_TRIPS}")

            plt.figure(figsize=(10, 5))
            plt.hist(trip_df["duration"], bins=30)
            plt.xlabel("Trajanje putovanja [s]")
            plt.ylabel("Broj vozila")
            plt.title("Distribucija trajanja putovanja")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig("trip_duration_hist.png", dpi=200)
            plt.close()

            plt.figure(figsize=(10, 5))
            plt.hist(trip_df["waitingTime"], bins=30)
            plt.xlabel("Vrijeme čekanja [s]")
            plt.ylabel("Broj vozila")
            plt.title("Distribucija vremena čekanja")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig("waiting_time_hist.png", dpi=200)
            plt.close()

            plt.figure(figsize=(10, 5))
            plt.scatter(trip_df["routeLength"], trip_df["duration"], s=10)
            plt.xlabel("Dužina rute [m]")
            plt.ylabel("Trajanje putovanja [s]")
            plt.title("Dužina rute vs trajanje putovanja")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig("route_length_vs_duration.png", dpi=200)
            plt.close()

    else:
        print(f"Nije pronađen: {TRIP_XML}")

    kpi_df = build_kpi_summary(edge_df, trip_df)
    if not kpi_df.empty:
        kpi_df.to_csv(OUT_KPI_CSV, index=False, encoding="utf-8-sig")
        print(f"Generisan: {OUT_KPI_CSV}")
        print("\nFinal KPI Summary:")
        print(kpi_df.to_string(index=False))
    else:
        print("Nema KPI podataka za izvoz.")

if __name__ == "__main__":
    main()