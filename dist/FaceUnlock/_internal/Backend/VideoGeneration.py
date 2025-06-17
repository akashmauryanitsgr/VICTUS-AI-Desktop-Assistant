# --- Install required libraries ---
# pip install diffusers transformers torch torchvision safetensors accelerate imageio einops opencv-python moviepy

import torch
from diffusers import AnimateDiffPipeline, DDIMScheduler
import imageio
import os
from tqdm import tqdm
#from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy import VideoFileClip,AudioFileClip
# --- Settings ---
prompt = "a futuristic city with flying cars at sunset, cinematic, ultra-detailed, 4K"
negative_prompt = "low quality, blurry, bad anatomy, distorted, ugly"
output_folder = "generated_frames"
raw_video_file = "animated_video.mp4"
final_video_with_music = "animated_video_with_music.mp4"
music_file = "background_music.mp3"  # Your music file here
num_frames = 24
height, width = 512, 512
guidance_scale = 7.5
fps = 30

device = "cuda" if torch.cuda.is_available() else "cpu"

# --- Create output folder ---
os.makedirs(output_folder, exist_ok=True)

# --- Load AnimateDiff pipeline ---
pipe = AnimateDiffPipeline.from_pretrained(
    "cagliostrolab/animatelcm",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
).to(device)

pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)

# --- Generate Frames ---
frames = []
print("🎨 Generating frames...")
for i in tqdm(range(num_frames), desc="Frames"):
    generator = torch.manual_seed(i)  # Slight randomness for motion
    output = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        height=height,
        width=width,
        num_inference_steps=30,
        guidance_scale=guidance_scale,
        generator=generator
    )
    
    frame = output.frames[0]
    frame_path = os.path.join(output_folder, f"frame_{i:04d}.png")
    frame.save(frame_path)
    frames.append(frame_path)

# --- Assemble Video ---
print("🎥 Compiling frames into video...")
writer = imageio.get_writer(raw_video_file, fps=fps)
for frame_path in frames:
    frame = imageio.imread(frame_path)
    writer.append_data(frame)
writer.close()

print(f"✅ Video saved as {raw_video_file}")

# --- Add Music ---
print("🎶 Adding background music...")

if os.path.exists(music_file):
    # Load video and music
    videoclip = VideoFileClip(raw_video_file)
    audioclip = AudioFileClip(music_file)

    # If music is shorter or longer, match the video length
    audioclip = audioclip.set_duration(videoclip.duration)
    videoclip = videoclip.set_audio(audioclip)

    # Save final video
    videoclip.write_videofile(final_video_with_music, codec="libx264", audio_codec="aac")

    print(f"✅ Final video with music saved as {final_video_with_music}")
else:
    print("⚠️ No music file found! Please add 'background_music.mp3' in the folder.")

