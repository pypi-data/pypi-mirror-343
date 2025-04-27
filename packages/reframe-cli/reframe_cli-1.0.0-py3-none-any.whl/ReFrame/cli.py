import argparse
from ReFrame.extract_frames import extract_frames
from ReFrame.image_converter import convert_image
from ReFrame.gif_creator import create_gif

def main():
    parser = argparse.ArgumentParser(
        description="ReFrame-CLI. A great tool to boost your productivity in video and image manipulation tasks. Ideal for preparing image datasets for training machine learning models, including generative AI and diffusion models."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    #subcommand: extract
    extract_parser = subparsers.add_parser("extractf", help="Extract frames from a video")
    extract_parser.add_argument("-input", "--input_path", required=True, help="Path to the video file")
    extract_parser.add_argument("-output", "--output_dir", required=True, help="Directory to save the extracted frames")
    extract_parser.add_argument("-f", "--format", default="png", choices=["png", "jpg", "jpeg"],
                                help="Format of the output frames (png or jpg). Default is png.")
    extract_parser.add_argument("-fps", "--fps", type=float,
                                help="Frames per second to extract. If not specified, extracts all frames.")
    extract_parser.add_argument("-start", "--start_time", type=float,
                                help="Start time (in seconds) for frame extraction.")
    extract_parser.add_argument("-end", "--end_time", type=float,
                                help="End time (in seconds) for frame extraction.")

    #subcommand: convert
    convert_parser = subparsers.add_parser("convert", help="Convert images to different formats")
    convert_parser.add_argument("-input", "--input_path", required=True, help="Path to the image file or directory")
    convert_parser.add_argument("-output", "--output_dir", required=True, help="Directory to save the converted images")
    convert_parser.add_argument("-f", "--format", required=True, choices=["png", "jpg", "jpeg", "webp", "heic", "heif"],
                                help="The desired output format")

    #subcommand: gif
    gif_parser = subparsers.add_parser("gifc", help="Create an animated GIF by stakcing up images")
    gif_parser.add_argument("-input", "--input_dir", required=True, help="Path to the directory containing images")
    gif_parser.add_argument("-output", "--output_path", required=True, help="Path to save the output GIF file must be specified with .gif format")
    gif_parser.add_argument("-d", "--duration", type=int, default=100,
                             help="Duration of each frame in the GIF in milliseconds (default: 100ms)")

    #parse the arguments
    args = parser.parse_args()

    #routing
    if args.command == "extractf":
        extract_frames(
            video_path=args.input_path,
            output_dir=args.output_dir,
            format=args.format,
            fps=args.fps,
            start_time=args.start_time,
            end_time=args.end_time,
        )
    elif args.command == "convert":
        convert_image(
            image_path=args.input_path,
            output_dir=args.output_dir,
            output_format=args.format,
        )
    elif args.command == "gifc":
        create_gif(
            image_dir=args.input_dir,
            output_path=args.output_path,
            duration=args.duration,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()