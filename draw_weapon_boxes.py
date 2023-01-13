import boto3
import io
from PIL import Image, ImageDraw
from pathlib import Path

from run_ocr import convert_to_jpg


def draw_weapon(photo):
    # Connect to the Rekognition client
    client = boto3.client("rekognition")

    file_path = convert_to_jpg(photo)

    # Read the image file
    with open(file_path, "rb") as f:
        image_data = f.read()

    # Create a binary stream for the image data
    image_stream = io.BytesIO(image_data)

    # Call the detect_labels method
    response = client.detect_labels(
        Image={"Bytes": image_stream.getvalue()}, MinConfidence=50
    )
    # dump response to file
    with open("response.json", "w") as f:
        f.write(str(response))

    # Load the image
    image = Image.open(photo)

    # Create an ImageDraw object
    draw = ImageDraw.Draw(image)

    # Initialize an empty list to store the labels
    labels = []

    instance_count = 0

    # Iterate over the labels in the response
    for label in response["Labels"]:
        if (
            label["Name"]
            in [
                "Rifle",
                "Firearm",
                "Weapon",
                "Gun",
                "Armory",
                "Handgun",
                "Pistol",
                "Knife",
                "Gun barrel",
                "Bow",
            ]
            and len(label["Instances"]) != 0
        ):
            # Append the label to the list
            labels.append(label["Name"])

            # Get the bounding box coordinates for each instance

            for instance in label["Instances"]:
                instance_count += 1
                box = instance["BoundingBox"]
                left = image.width * box["Left"]
                top = image.height * box["Top"]
                width = image.width * box["Width"]
                height = image.height * box["Height"]

                # Draw a rectangle around the label
                draw.rectangle(
                    [left, top, left + width, top + height],
                    outline="#d4af37",  # outline color
                    width=3,
                )

    # Save the image with the bounding boxes to an output folder called annotated_images under the original image's parent folder

    # print original image path

    print("Original image path:", photo)

    # if the file path is not in jpg or png, move to processed_images folder
    if file_path.suffix not in [".jpg", ".png"]:
        # find parent folder of the image
        parent_folder = file_path.parent
        # check if processed_files folder exists in the parent folder
        if not Path(parent_folder / "processed_images").exists():
            # create processed_images folder
            Path(parent_folder / "processed_images").mkdir()

        # move the old file to a old_images folder
        file_path.rename(Path(parent_folder / "processed_images") / file_path.name)

    # get the parent folder of the original image using pathlib
    parent_folder = Path(photo).parent

    # create a new folder called annotated images if it does not exist in parent folder
    annotated_images_folder = parent_folder / "annotated_images"

    if not annotated_images_folder.exists():
        annotated_images_folder.mkdir()

    # generate the new path for the annotated image

    annotated_image_path = annotated_images_folder / Path(photo).name
    image.save(annotated_image_path)

    # image.save("annotated_image.jpg")
    # labels should be string
    labels = ", ".join(labels)
    return annotated_image_path, labels, instance_count


def main():
    photo = "/Users/sefa/adl_work/telegram_threat_POC/images/synagogues/ki_building_horizontal.jpg"
    image, labels, instance_count = draw_weapon(photo)
    print("Detected labels in the image are:", labels)
    print("Number of weapon instances detected:", instance_count)

    # # loop through weapon images in images/weapons folder
    # for photo in Path("/Users/sefa/adl_work/telegram_threat_POC/images/weapons").glob(
    #     "*.jpg"
    # ):
    #     image, labels, instance_count = draw_weapon(photo)
    #     print("Detected labels in the image are:", labels)
    #     print("Number of instances detected:", instance_count)


if __name__ == "__main__":
    main()
