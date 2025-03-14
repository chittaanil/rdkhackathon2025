#!/usr/bin/env python3
import subprocess
import os
import time
import glob

def play_video(video_path):
    """Execute GStreamer pipeline to play a video file with debugging enabled."""
    
    # Set GST_DEBUG environment variable for detailed logging
    os.environ["GST_DEBUG"] = "4"
    log_file = "/home/vboxuser/Documents/logs/gstreamer.log"
    
    # Define the log directory for DOT and PNG files
    log_dir = "/home/vboxuser/Documents/logs/DOT"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Generate a dynamic prefix for the .dot file (e.g., timestamp)
    timestamp = time.time()
    dynamic_prefix = f"{timestamp:.6f}-"
    dot_filename = os.path.join(log_dir, f"{dynamic_prefix}PAUSED_PLAYING.dot")
    
    # Generate a timestamp-based filename for the PNG file to ensure uniqueness
    png_filename = os.path.join(log_dir, f"PAUSED_PLAYING-{timestamp:.6f}.png")
    
    # Set the environment variable for GStreamer to dump the DOT file
    os.environ["GST_DEBUG_DUMP_DOT_DIR"] = log_dir
    
    # Define the pipeline command
    gst_pipeline = [
        "gst-launch-1.0",
        "filesrc", f"location={video_path}",
        "!", "decodebin",
        "!", "autovideosink"
    ]
    
    # Run the pipeline and redirect logs to file
    try:
        print("Running GStreamer pipeline...")
        with open(log_file, "w") as log:
            subprocess.run(gst_pipeline, check=True, stdout=log, stderr=log)
    except subprocess.CalledProcessError as e:
        print(f"Error executing GStreamer pipeline: {e}")
    
    # Wait for a moment to ensure GStreamer has finished writing the DOT file
    time.sleep(2)  # Adjust the sleep time if necessary
    
    # After pipeline completes, try to find the most recent .dot file and generate PNG
    find_dot_and_convert(log_dir, png_filename)


def find_dot_and_convert(log_dir, png_filename):
    """Find the most recent .dot file in the log directory and convert it to PNG."""
    try:
        # Find all .dot files in the log directory
        dot_files = glob.glob(os.path.join(log_dir, "*.PAUSED_PLAYING.dot"))
        
        if dot_files:
            # Sort the .dot files by their modification time (newest first)
            dot_files.sort(key=os.path.getmtime, reverse=True)
            latest_dot_file = dot_files[0]  # Take the most recently modified .dot file
            print(f"Using the latest .dot file: {latest_dot_file}")
            
            # Convert the .dot file to PNG using Graphviz
            subprocess.run(f"dot -Tpng {latest_dot_file} -o {png_filename}", shell=True, check=True)
            print(f"PNG image generated: {png_filename}")
        else:
            print(f"Error: No .dot files found in {log_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Error converting DOT to PNG: {e}")


if __name__ == "__main__":
    video_file = "/home/vboxuser/Downloads/sam.mp4"  # Replace with the actual video path
    play_video(video_file)
