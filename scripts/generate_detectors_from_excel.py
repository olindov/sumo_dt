import pandas as pd
from pathlib import Path

input_file = Path("../1_input/sensors/east_sarajevo_measurement_points.csv")
output_file = Path("../4_detectors/detectors_real.add.xml")

df = pd.read_csv(input_file)

required = ["ID", "SUMO_lane_id", "SUMO_pos_m"]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

lines = ["<additional>"]
for _, row in df.iterrows():
    lane = row.get("SUMO_lane_id")
    pos = row.get("SUMO_pos_m")
    if pd.notna(lane) and pd.notna(pos):
        lines.append(
            f'    <e1Detector id="{row["ID"]}" lane="{lane}" pos="{pos}" freq="60" file="../5_outputs/{row["ID"]}_detector.xml"/>'
        )
lines.append("</additional>")

output_file.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {output_file}")
