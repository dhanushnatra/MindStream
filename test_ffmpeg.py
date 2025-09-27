import ffmpeg  # Make sure this is from the 'ffmpeg-python' package, not the 'ffmpeg' package
import os 
print(os.listdir("images"))

# List of image files (ensure they are sorted for correct order)
files = sorted([img for img in os.listdir('images') if img.endswith(('.jpg', '.jpeg', '.png'))])

# Write the list of files to a text file for ffmpeg concat demuxer
with open('images.txt', 'w') as f:
	for img in files:
		f.write(f"file 'images/{img}'\nduration 2\n")
	# Repeat last image without duration for ffmpeg concat demuxer
	if files:
		f.write(f"file 'images/{files[-1]}'\n")

# Use ffmpeg concat demuxer to create video from images
(
	ffmpeg
	.input('images.txt', format='concat', safe=0)
	.output('output.mp4', vcodec='libx264', pix_fmt='yuv420p', r=30)
	.run(overwrite_output=True)
)