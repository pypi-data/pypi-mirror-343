import os

def create_output_dir(output_dir):
    """
    Creates the output directory if it does not exist.

    Args:
        output_dir (str): The path to the output directory.

    Returns:
        str: The output directory path, or None if there was an error.
    """
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        except OSError as e:
            print(f"Error: Could not create output directory {output_dir}. Details: {e}")
            return None
    return output_dir