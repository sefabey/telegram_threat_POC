import boto3
import io


def detect_weapons(photo):
    # Connect to the Rekognition client
    client = boto3.client("rekognition")

    # Read the image file
    with open(photo, "rb") as f:
        image_data = f.read()

    # Create a binary stream for the image data
    image_stream = io.BytesIO(image_data)

    # Call the detect_labels method
    response = client.detect_labels(
        Image={"Bytes": image_stream.getvalue()}, MinConfidence=90
    )

    # Initialize an empty list to store the labels
    labels = []

    # Iterate over the labels in the response
    for label in response["Labels"]:
        # Check if the label is in the list of labels to keep
        if label["Name"] in ["Rifle", "Firearm", "Weapon", "Gun", "Armory", "Handgun"]:
            # Append the label to the list
            labels.append(label["Name"])

    # Print the labels
    print("Detected labels for " + photo)
    print(labels)

    # Return the number of labels detected
    return len(labels)


def main():
    photo = "/Users/sefa/adl_work/telegram_threat_POC/images/test/IMGP0122.jpg"
    label_count = detect_weapons(photo)
    print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    main()
