import numpy as np
import moviepy.editor as mp
import os
from scipy.ndimage import zoom
import cv2


# replace classroom name and video name from the inputs from frontend
classroom_name = "test_classroom"
video_name = "test_video"
folder_path = f"{classroom_name}/{video_name}"

# replace this with path to the raw video that is recieved as input from frontend
stored_vid_path = f"{folder_path}/stored_vid.mp4"
audio_path = f"{folder_path}/audio.mp3"
temp_vid_path = f"{folder_path}/temp_vid.mp4"
returned_vid_path = f"{folder_path}/final_vid.mp4"


def read_video_to_numpy(video_path):
    """
    This function takes the previously compressed video file
    and loads it as a numpy array ready for decompression.
    """

    clip = mp.VideoFileClip(video_path)
    fps = clip.fps
    frames = []
    for frame in clip.iter_frames():
        # Extract RGB channels only (discard alpha)
        frames.append(frame[:, :, :3])
    clip.close()
    return np.array(frames), fps

video, fps = read_video_to_numpy(stored_vid_path)  # function call
frames, height, width, channel = video.shape


ycbcr_video = np.empty_like(video)

# Convert each frame from RGB to YCbCr
for i in range(video.shape[0]):
    ycbcr_video[i] = cv2.cvtColor(video[i], cv2.COLOR_RGB2YCrCb)


def upsample_channel(downsampled_channel, factor=4):
    """
    Upsample a given downsampled channel by a factor of 4 using bilinear interpolation
    """
    upsampled_channel = zoom(downsampled_channel, factor, order=1)

    return upsampled_channel


upsampled_y = np.stack(
    [upsample_channel(ycbcr_video[i][:, :, 0]) for i in range(frames)])
upsampled_cb = np.stack(
    [upsample_channel(ycbcr_video[i][:, :, 1]) for i in range(frames)])
upsampled_cr = np.stack(
    [upsample_channel(ycbcr_video[i][:, :, 2]) for i in range(frames)])

upsampled_ycbcr = np.dstack(
    (upsampled_y, upsampled_cb, upsampled_cr), axis=-1)


rgb_video_array = np.empty([frames, (height*4), (width*4), channel])

for i in range(video.shape[0]):
    rgb_video_array[i] = cv2.cvtColor(upsampled_ycbcr[i], cv2.COLOR_YCrCb2RGB)


def numpy_to_video(frames, output_path, fps=fps):
    """
    re-create a video as an mp4 file to store the downsampled video
    """

    height, width, _ = frames[0].shape
    video_clip = mp.ImageSequenceClip(list(frames), fps=fps)
    video_clip.without_audio().write_videofile(output_path)
    video_clip.close()

numpy_to_video(rgb_video_array, temp_vid_path)


def add_audio_to_video(video_path, audio_path, output_path):
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = mp.AudioFileClip(audio_path)
    
    video_with_audio = video_clip.set_audio(audio_clip)
    video_with_audio.write_videofile(output_path, codec='libx264', audio_codec='aac')
    
    video_clip.close()
    audio_clip.close()

add_audio_to_video(temp_vid_path, audio_path, returned_vid_path)