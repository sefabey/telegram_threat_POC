# import libraries

import pandas as pd
from draw_weapon_boxes import draw_weapon
from run_ocr import get_ocr_results
from pathlib import Path

# read the csv file

df = pd.read_csv("mock_tg_data_to_infer.csv")

# create a new column to store the results

df["ocr_results"] = ""

# iterate over the rows of the dataframe

for index, row in df.iterrows():
    # get the image path from the row
    image_path = row["image_attachment"]
    print("image path:", image_path)
    print(type(image_path))
    # get the ocr results
    ocr_results = get_ocr_results(image_path)
    # store the results in the dataframe
    df.loc[index, "ocr_results"] = ocr_results

df.head()


# run weapon detection
# iterate over the rows of the dataframe

for index, row in df.iterrows():
    # get the image path from the row
    image_path = row["image_attachment"]
    print("image path:", image_path)
    print(type(image_path))
    # get the ocr results
    image, labels, instance_count = draw_weapon(image_path)
    # store the results in the dataframe
    # weapon_present is a boolean column that is True if the weapon is present in the image
    df.loc[index, "weapon_present"] = True if instance_count > 0 else False
    df.loc[index, "weapon_drawn_path"] = Path(image) if instance_count > 0 else None
    df.loc[index, "weapon_label"] = labels if instance_count > 0 else None
    df.loc[index, "weapon_instance_count"] = instance_count


# save the dataframe to a csv file

df.to_csv("mock_tg_data_to_inference.csv", index=False)
