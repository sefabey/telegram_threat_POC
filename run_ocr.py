import boto3
import io
from PIL import Image
from pathlib import Path


def convert_to_jpg(file_path):
    try:
        file_path = Path(file_path)
        with Image.open(file_path) as img:
            # check if image extension is png or jpg/jpeg
            if img.format not in ["JPEG", "PNG"]:
                # convert to jpeg
                img = img.convert("RGB")
                # Update file extension to jpg
                new_file_path = Path(file_path).with_suffix(".jpg")
                img.save(new_file_path)
                print(
                    f"{file_path} has been converted to JPEG and saved as {new_file_path}"
                )

                return new_file_path
            else:
                print(f"{file_path} is already in {img.format} format")
                return file_path
    except Exception as e:
        print(f"Error occured while processing {file_path} : {e}")


def get_ocr_results(file_path):
    # Connect to the Textract client
    textract = boto3.client("textract")

    # check if the file is png OR jpg/jpeg, if not convert to jpg

    file_path = convert_to_jpg(file_path)

    # Read the file content
    with open(file_path, "rb") as f:
        file_content = f.read()

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

    # Return the list of text

    return text


def main():
    # file_path = (
    #     "/Users/sefa/adl_work/telegram_threat_POC/images/synagogues/img_4025.webp"
    # )
    # text = get_ocr_results(file_path)

    # print(" ".join(text))

    # loop through weapon images in images/synagogues folder and write to a jsonl file
    for photo in Path(
        "/Users/sefa/adl_work/telegram_threat_POC/images/synagogues/"
    ).glob("*"):
        text = get_ocr_results(photo)
        print(" ".join(text))

        # create a dictionary with file name and ocr results
        ocr_results = {"file_name": photo.name, "ocr_results": " ".join(text)}

        # write to a jsonl file
        with open("ocr_results.jsonl", "a") as f:
            f.write(str(ocr_results) + "\n")


if __name__ == "__main__":
    main()
