# import packages
import pandas as pd
import random
from datetime import datetime, timedelta

# read csv file mock_tg_data.csv
df = pd.read_csv("mock_tg_data.csv")

df.head()
# list all images in images/synagogues folder using pathlib
from pathlib import Path

# create a list of all images in images/synagogues folder with jpg, png and webp extensions
images = [
    str(image)
    for image in Path(
        "/Users/sefa/adl_work/telegram_threat_POC/images/synagogues/"
    ).glob("*")
    if image.suffix in [".jpg", ".png", ".webp"]
]

len(images)  # 38 images

# create a list of all images in images/weapos folder with jpg, png and webp extensions
weapon_images = [
    str(image)
    for image in Path("/Users/sefa/adl_work/telegram_threat_POC/images/weapons/").glob(
        "*"
    )
    if image.suffix in [".jpg", ".png", ".webp"]
]


len(weapon_images)  # 29

# create a list of all images in images/mix folder with jpg, png and webp extensions
mix_images = [
    str(image)
    for image in Path("/Users/sefa/adl_work/telegram_threat_POC/images/mix/").glob("*")
    if image.suffix in [".jpg", ".png", ".webp"]
]

len(mix_images)

# merge the two lists
images.extend(weapon_images)
images.extend(mix_images)

len(images)  # 67 images

# add the images to new row of dataframe in image_attachment column
#
for image in images:
    df = df.append({"image_attachment": image}, ignore_index=True)


# assing message_id to each row as a unique identifier string in the form of message_001, message_002, etc.
df["message_id"] = "message_" + df.index.astype(str).str.zfill(3)

df.head()
df.tail()

# create mock conversations
conversations = []
jewish_institutions = [
    "Jewish Museum",
    "Jewish Community Center",
    "Jewish Federation",
    "JCC",
    "Temple",
    "Synagogue",
    "Congregation",
    "Chabad",
    "Beth El",
]

# Create mock telegram chat dictionaries
for i in range(len(images)):
    message_id = "message_" + "{:03}".format(i + 1)
    if i % 3 == 0:
        message_text = (
            random.choice(jewish_institutions)
            + " "
            + random.choice(["is great", "is interesting", "is worth visiting"])
        )
    else:
        message_text = " ".join(
            [
                "This is a random sentence from an ext telegram channel."
                for _ in range(random.choice([2, 6]))
            ]
        )
    date_time = datetime(2022, 1, 1) + timedelta(
        days=random.randint(0, 14),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    conversations.append(
        {"message_id": message_id, "message_text": message_text, "date_time": date_time}
    )

df_mock = pd.DataFrame(conversations)
df_mock.info()


# merge the two dataframes on message_id and take message_text and date_time from df_mock
df = df.merge(df_mock, on="message_id", how="left")

# drop message_text_x and date_time_x columns
df = df.drop(columns=["message_text_x", "date_time_x"])

# rename message_text_y and date_time_y columns
df = df.rename(columns={"message_text_y": "message_text", "date_time_y": "date_time"})

# remove empty rows
df = df.dropna()

df.info()
# write to a csv file
df.to_csv("mock_tg_data_to_infer.csv", index=False)
