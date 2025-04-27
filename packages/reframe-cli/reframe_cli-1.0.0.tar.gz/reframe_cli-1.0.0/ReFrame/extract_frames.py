import cv2  # opencv library for video
import os 
import argparse
import math
from .utils import create_output_dir

#extract frames from a video file
def extract_frames(video_path, output_dir, format='png', fps=None, start_time=None, end_time=None):
    """
    Arguments:
        video_path (str): The path to the video file
        output_dir (str): The directory where the frames will be saved
        format (str, optional): The image format for the extracted frames ('png' or 'jpg'). Defaults to 'png'
        fps (float, optional): The frames per second to extract. If None, extracts all frames
        start_time (float, optional): The time (in seconds) from where you want to start the extraction
        end_time (float, optional): The time (in seconds) till where you want to extract
    """

    #check if the video file exists or not
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return

    #check if the output directory exists - create it if it doesn't using os
    if not create_output_dir(output_dir):
        return

    #check if the specified format is valid(png/jpg/jpeg) - png is default
    if format.lower() not in ['png', 'jpg', 'jpeg']:
        print(f"Error: Invalid format '{format}'.  Please choose 'png', 'jpg', or 'jpeg'.")
        return

    #opens the video file using opencv
    try:
        video_capture = cv2.VideoCapture(video_path)
    except Exception as e:
        print(f"Error: Could not open video file.  Details: {e}")
        return

    #getting the video's frames per second (FPS)
    video_fps = video_capture.get(cv2.CAP_PROP_FPS)
    if not video_fps or video_fps <= 0:
        print("Warning: Could not determine video FPS.  Extracting frames based on frame count.")
        video_fps = 30  #assume 30 FPS if unknown, to avoid division by zero :) .

    #total number of frames
    total_frames = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    
    #video duration
    video_duration = total_frames/video_fps

    #initializing frame counter and setting the frame step
    frame_number = 0
    frame_step = 1  #defauult: 1 i.e.(extract every frame)
    extracted_frames_count = 0
    
    #calculating start and end frames based on time
    start_frame = 0
    end_frame = total_frames
    
    if start_time is not None:
        if start_time < 0:
            print("Error: Start time cannot be negative. Setting start time to 0.")
            start_time = 0
        if start_time > video_duration:
            print("Error: Start time cannot be greater than video duration. Setting start time to video duration...")
            start_time = video_duration
        start_frame = int(math.floor(start_time * video_fps))
        frame_number = start_frame #start at the starting frame
    
    if end_time is not None:
        if end_time < 0:
            print("Error: End time cannot be negative. Setting end time to 0.")
            end_time = 0
        if end_time > video_duration:
            print("Error: End time cannot be greater than video duration. Setting end time to video duration...")
            end_time = video_duration
        end_frame = int(math.floor(end_time * video_fps))

    if fps is not None:
        if fps <= 0:
            print("Error: FPS must be a positive number.")
            video_capture.release()
            return
        frame_step = int(math.floor(video_fps / fps)) #calculating how many frames to skip
        if frame_step < 1: #prevents division by 0 or negative values
            frame_step = 1

    print(f"Extracting frames from {video_path} with a frame step of {frame_step} to {output_dir} in {format.upper()} format.")
    if start_time is not None or end_time is not None:
        print(f"Extraction time range: {start_time if start_time is not None else 0}s - {end_time if end_time is not None else video_duration}s")
        
    #set the video to start from the start frame
    video_capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    #loop through the video frames
    while True:
        #read the next frame from the video
        success, frame = video_capture.read()

        #if no more frames, break out of the loop
        if not success or frame_number > end_frame:
            break

        #naming convention (processing frames according to the frame_step that is the number of the frame)
        if frame_number % frame_step == 0 and frame_number >= start_frame:
            #construct the output file name
            if format.lower() == 'png':
                output_file = os.path.join(output_dir, f"frame_{extracted_frames_count:06d}.png")
                cv2.imwrite(output_file, frame)  #save the frame (note: format = png by default)
            elif format.lower() in ['jpg', 'jpeg']:
                output_file = os.path.join(output_dir, f"frame_{extracted_frames_count:06d}.jpg")
                cv2.imwrite(output_file, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 95]) #save as jpg
            print(f"Extracted frame {frame_number}/{total_frames}", end='\r')
            extracted_frames_count += 1

        frame_number += 1

    #release the video capture object to free some resources
    video_capture.release()
    print(f"\nFinished extracting frames. Total frames extracted: {extracted_frames_count}")



def main():
    #creating an argument parser
    parser = argparse.ArgumentParser(description="Extract frames from a video file.")

    #pass the required arguments: video path and output directory
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("output_dir", help="Directory to save the extracted frames")

    #pass optional arguments: image format and fps
    parser.add_argument("-f", "--format", default="png", choices=['png', 'jpg', 'jpeg'],
                        help="Format of the output frames (png or jpg). Default is png.")
    parser.add_argument("-fps", "--fps", type=float,
                        help="Frames per second to extract. If not specified, extracts all frames.")
    parser.add_argument("-start", "--start_time", type=float,
                        help="Start time (in seconds) for frame extraction.")
    parser.add_argument("-end", "--end_time", type=float,
                        help="End time (in seconds) for frame extraction.")

    #parsing the command line arguments
    args = parser.parse_args()

    #call the extract_frames function with the parsed arguments
    extract_frames(args.video_path, args.output_dir, args.format, args.fps, args.start_time, args.end_time)



if __name__ == "__main__":
    main()
