import boto3
import io
from PIL import Image


def get_ocr_results(file_path):
    # Connect to the Textract client
    textract = boto3.client("textract")

    # Read the file content
    with open(file_path, "rb") as f:
        file_content = f.read()

    # Check if the file is not a JPEG image
    if not file_path.endswith(".jpg"):
        # Convert the image to JPEG format
        image = Image.open(io.BytesIO(file_content))
        file_content = io.BytesIO()
        image.save(file_content, "JPEG")
        file_content.seek(0)

    # Create a binary stream for the file content
    file_stream = io.BytesIO(file_content)

    # Call the detect_document_text method
    response = textract.detect_document_text(Document={"Bytes": file_stream.getvalue()})

    # Initialize an empty list to store the text
    text = []

    # Iterate over the blocks in the response
    for block in response["Blocks"]:
        # Check if the block is a word
        if block["BlockType"] == "WORD":
            # Append the text to the list
            text.append(block["Text"])

    # Return the list of text
    return text


def main():
    file_path = "/Users/sefa/adl_work/telegram_threat_POC/images/test/3.20.29.1-Young-Israel.jpg"

    text = get_ocr_results(file_path)

    print(" ".join(text))


if __name__ == "__main__":
    main()
