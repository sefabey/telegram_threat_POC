import pandas as pd
from draw_weapon_boxes import draw_weapon
from run_ocr import get_ocr_results
from pathlib import Path

df = pd.read_csv("mock_tg_data_to_infer.csv")

df["ocr_results"] = ""
df["weapon_present"] = False
df["weapon_drawn_path"] = None
df["weapon_label"] = None
df["weapon_instance_count"] = None

for index, row in df.iterrows():
    image_path = Path(row["image_attachment"])
    ocr_results = get_ocr_results(image_path)
    df.loc[index, "ocr_results"] = ocr_results

    image, labels, instance_count = draw_weapon(image_path)
    df.loc[index, "weapon_present"] = bool(instance_count)
    df.loc[index, "weapon_drawn_path"] = image if instance_count else None
    df.loc[index, "weapon_label"] = labels if instance_count else None
    df.loc[index, "weapon_instance_count"] = instance_count

df.to_csv("mock_tg_data_to_inference_pythonic.csv", index=False)
