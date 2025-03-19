import os
from PIL import Image
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def process_images(input_folder, output_file):
    print(f"Processing {input_folder}...")
    results = []

    with ThreadPoolExecutor() as executor:
        futures = []
        for file_name in os.listdir(input_folder):
            file_path = os.path.join(input_folder, file_name)
            if not (file_name.lower().endswith(".jpg") or file_name.lower().endswith(".png")):
                continue
            futures.append(executor.submit(process_image_wrapper, file_name, file_path))

        for future in futures:
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                print(f"Error occurred: {e}")

    save_results(results, output_file)

def process_image_wrapper(file_name, file_path):
    try:
        image = Image.open(file_path).convert("RGB")
        return process_image(file_name, image)
    except Exception as e:
        print(f"Error processing {file_name}: {e}")
        return None

def process_image(file_name, image):
    pixel_count = count_pixels(image)

    return {
        "Tarih": file_name.split("_to_")[0],
        "Pixel": pixel_count,
    }

def save_results(results, output_file):
    df = pd.DataFrame(results)
    df = df.sort_values(by=["Tarih"])
    df.to_excel(output_file, index=False)

def count_pixels(image):
    pixels = list(image.getdata())
    white_count = 0

    for pixel in pixels:
        r, g, b = pixel
        if r == 255 and g == 255 and b == 255:
            white_count += 1

    return white_count

def process_all_lakes(input_base_folder, output_base_folder):
    lake_folders = [f for f in os.listdir(input_base_folder) if os.path.isdir(os.path.join(input_base_folder, f))]
    
    for lake_name in lake_folders:
        input_folder = os.path.join(input_base_folder, lake_name)
        output_file = os.path.join(output_base_folder, f"{lake_name}.xlsx")
        process_images(input_folder, output_file)

input_base_folder = "input"
output_base_folder = "output"
process_all_lakes(input_base_folder, output_base_folder)