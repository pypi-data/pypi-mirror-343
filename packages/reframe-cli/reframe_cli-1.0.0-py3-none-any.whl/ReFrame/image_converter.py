import cv2
import os
import argparse
import numpy as np  #import numpy as np for array operations
from PIL import Image #import Image from pillow library
import sys
from .utils import create_output_dir


def convert_image(image_path, output_dir, output_format):
    """
    Converts an image from one format to another.

    Args:
        image_path (str): Path to the input image file or directory.
        output_dir (str): Directory where the converted images will be saved.
        output_format (str): The desired output format (e.g., 'png', 'jpg', 'jpeg', 'webp', 'heic').
    """
        
    #validation of output format
    if output_format.lower() not in ['png', 'jpg', 'jpeg', 'webp', 'heic', 'heif']:
        print(f"Error: Unsupported output format '{output_format}'.")
        return
    
    #directory input for batch conversion
    if os.path.isdir(image_path):
        process_directory(image_path, output_dir, output_format)
    elif os.path.isfile(image_path):
        process_file(image_path, output_dir, output_format)
    else:
        print(f"Error: Invalid image path. Must be a file or directory: {image_path}")
        return

def process_file(image_file, output_dir, output_format, is_bulk=False):
    """
    Processes a single image file.

    Args:
        image_file (str): Path to the image file.
        output_dir (str): Directory to save the converted image.
        output_format (str): The desired output format.
        is_bulk (bool): Flag to indicate if this is a bulk operation or not.
    """
    #check if the input image exists
    if not os.path.exists(image_file):
        print(f"Error: Image file not found at {image_file}")
        return

    #read image using opencv
    try:
        #For heif/heic conversion, first convert the image to BGR cause opencv can't process heif/heic formats
        if image_file.lower().endswith(('.heif', '.heic')):
            from pillow_heif import register_heif_opener
            register_heif_opener()  # register HEIF opener with Pillow
            pil_image = Image.open(image_file)  #read the HEIF/HEIC image using pillow
            img = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR) #convert to BGR
        else:
            img = cv2.imread(image_file) #use directly without converting for other formats
        if img is None:
            print(f"Warning: Could not read image file: {image_file}. Skipping.")
            return
    except ImportError:
        print("Error: HEIF/HEIC conversion requires the 'pillow-heif' library. Please install it (pip install pillow-heif).")
        if is_bulk:
            sys.exit(1)
        return
    
    except Exception as e:
        print(f"Error: Could not read image file: {image_file}. Details: {e}")
        if is_bulk:
            sys.exit(1)
        return

    #output file name and whether to replace the original or not
    replace_original = False
    if output_dir == os.path.dirname(image_file) or output_dir is None:
        output_file = os.path.splitext(image_file)[0] + "." + output_format.lower()
        replace_original = True
    else:
        if not create_output_dir(output_dir):
            if is_bulk:
                sys.exit(1)
            return
        output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(image_file))[0] + "." + output_format.lower())

    #convert the image based on the specified format
    try:
        if output_format.lower() in ['jpg', 'jpeg']:
            cv2.imwrite(output_file, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])  #95 is the jpg quality set to
        elif output_format.lower() == 'png':
            cv2.imwrite(output_file, img)
        elif output_format.lower() == 'webp':
            cv2.imwrite(output_file, img, [int(cv2.IMWRITE_WEBP_QUALITY), 95])
        elif output_format.lower() in ['heic', 'heif']:
            try:
                from pillow_heif import register_heif_opener
                register_heif_opener()  #register heif opener with pillow
                pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                #save as heic or heif based on the output format
                save_format = 'heif' if output_format.lower() in ['heic', 'heif'] else output_format.lower()
                pil_image.save(output_file, format=save_format)
            except ImportError:
                print("Error: HEIF/HEIC conversion requires the 'pillow-heif' library. Please install it (pip install pillow-heif).")
                if is_bulk:
                    sys.exit(1)
                return
            except Exception as e:
                print(f"Error: Could not convert image to {output_format.upper()}: {image_file}. Details: {e}")
                if is_bulk:
                    sys.exit(1)
                return
        else:
            print(f"Error: Unsupported output format '{output_format}'.")
            if is_bulk:
                sys.exit(1)
            return
        if not is_bulk and not replace_original:
            print(f"Converted {image_file} to {output_file}")
    except Exception as e:
        print(f"Error: Could not convert image: {image_file}. Details: {e}")
        if is_bulk:
            sys.exit(1)
        return
    
    #delete the original files after successful conversion and replacement
    if replace_original:
        try:
            os.remove(image_file)
        except Exception as e:
            print(f"Error: Could not delete original image file {image_file}. Details: {e}")

def process_directory(image_dir, output_dir, output_format):
    """
    Processes all image files in a directory.

    Args:
        image_dir (str): Path to the directory containing images.
        output_dir (str): Directory to save converted images.
        output_format (str): The desired output format.
    """
    if output_dir != image_dir and output_dir is not None:
        if not create_output_dir(output_dir):
            return
        
    #get a list of files from the directory
    files = os.listdir(image_dir)
    total_files = len(files)
    converted_count = 0
    for i, file in enumerate(files):
        file_path = os.path.join(image_dir, file)
        if os.path.isfile(file_path) and file.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.heic', '.heif')):
            process_file(file_path, output_dir, output_format, is_bulk=True)
            converted_count += 1
            sys.stdout.write(f"\rConverted {converted_count}/{total_files}")
            sys.stdout.flush()
    print(f"\nFinished converting {converted_count} images.")

def main():
    """
    Main function to parse command line arguments and call the convert_image function.
    """
    parser = argparse.ArgumentParser(description="Convert an image to a different format.")
    parser.add_argument("image_path", help="Path to the image file to convert.")
    parser.add_argument("output_dir", nargs='?', default=None, help="Directory to save the converted image(s). If not provided, images are replaced in-place.")
    parser.add_argument("output_format", help="The desired output format (png, jpg, jpeg, webp, heic, heif).")

    args = parser.parse_args()
    convert_image(args.image_path, args.output_dir, args.output_format)

if __name__ == "__main__":
    main()