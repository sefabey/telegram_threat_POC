import boto3
import io


def moderate_image(photo):
    # Connect to the Rekognition client
    client = boto3.client("rekognition")

    # Read the image file
    with open(photo, "rb") as f:
        image_data = f.read()

    # Create a binary stream for the image data
    image_stream = io.BytesIO(image_data)

    # Call the detect_moderation_labels method
    response = client.detect_moderation_labels(Image={"Bytes": image_stream.getvalue()})

    # Print the labels and confidence levels
    print("Detected labels for " + photo)
    for label in response["ModerationLabels"]:
        print(label["Name"] + " : " + str(label["Confidence"]))
        print(label["ParentName"])

    # Return the number of labels detected
    return len(response["ModerationLabels"])


def main():
    photo = "/Users/sefa/adl_work/telegram_threat_POC/images/test/IMGP0122.jpg"
    label_count = moderate_image(photo)
    print("Labels detected: " + str(label_count))


if __name__ == "__main__":
    main()
