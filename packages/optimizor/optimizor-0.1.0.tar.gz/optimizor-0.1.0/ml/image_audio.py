#!/usr/bin/env python
# coding: utf-8

# <b> IMAGE PROCESSING </b>

# In[ ]:


import cv2
import numpy as np
import matplotlib.pyplot as plt


# In[ ]:


image = cv2.imread('dog.jpg')

# Convert from BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image_rgb)
plt.axis('off')
plt.show()


# In[ ]:


# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Display the grayscale image
plt.imshow(gray_image, cmap='gray')
plt.axis('off')
plt.show()


# In[ ]:


# Adjust brightness and contrast
alpha = 1
beta = 20 

adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

# Display the adjusted image
plt.imshow(adjusted_image, cmap='gray')
plt.axis('off')
plt.show()


# In[ ]:


# Path to the image file
file_path = 'dog.jpg'  # Adjust this to the correct path

# Load the image in grayscale mode
image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

# Verify if image is loaded
if image is None:
    print("Error: Image not loaded. Check the file path.")
else:
    print("Image loaded successfully. Shape:", image.shape)

    # Display the original grayscale image
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.show()

    # Apply histogram equalization
    equalized_image = cv2.equalizeHist(image)

    # Display the equalized image
    plt.imshow(equalized_image, cmap='gray')
    plt.axis('off')
    plt.show()


# In[ ]:


# Apply Gaussian Blur to the grayscale image
blurred_image = cv2.GaussianBlur(gray_image, (15, 15), 0)

# Display the blurred image
plt.imshow(blurred_image, cmap='gray')
plt.axis('off')
plt.show()


# In[ ]:


# Perform Canny edge detection
edges = cv2.Canny(gray_image, 100, 200)

# Display the edges
plt.imshow(edges, cmap='gray')
plt.axis('off')
plt.show()


# In[ ]:


# Apply binary thresholding
_, thresholded_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)

# Display the thresholded image
plt.imshow(thresholded_image, cmap='gray')
plt.axis('off')
plt.show()


# In[ ]:


# Resize the image to half its original size
height, width = image.shape[:2]
resized_image = cv2.resize(image, (width // 2, height // 2))

# Convert to RGB for display
resized_image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

# Display the resized image
plt.imshow(resized_image_rgb)
plt.axis('off')
plt.show()


# In[ ]:


cv2.imwrite('processed_image_dog.jpg', image)


# In[ ]:


import cv2
import matplotlib.pyplot as plt

# Load the grayscale image
file_path = 'dog.jpg'  # Adjust this to the correct path
image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

# Simple Binary Thresholding
thresh_value = 127
_, binary_thresholded_image = cv2.threshold(image, thresh_value, 255, cv2.THRESH_BINARY)
plt.imshow(binary_thresholded_image, cmap='gray')
plt.title(f'Simple Thresholding (Threshold = {thresh_value})')
plt.axis('off')
plt.show()

# Adaptive Thresholding
block_size = 11
C = 2
adaptive_thresh_image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)
plt.imshow(adaptive_thresh_image, cmap='gray')
plt.title(f'Adaptive Thresholding (Block Size = {block_size}, C = {C})')
plt.axis('off')
plt.show()

# Otsu's Thresholding
_, otsu_thresh_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
plt.imshow(otsu_thresh_image, cmap='gray')
plt.title("Otsu's Thresholding")
plt.axis('off')
plt.show()

# Experimenting with Different Thresholds
threshold_values = [50, 100, 150, 200]
for thresh in threshold_values:
    _, thresh_image = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)
    plt.imshow(thresh_image, cmap='gray')
    plt.title(f'Simple Thresholding (Threshold = {thresh})')
    plt.axis('off')
    plt.show()


# In[ ]:


# Apply Median Filtering
median_filtered_image = cv2.medianBlur(image, 5)

# Display the median filtered image
plt.imshow(median_filtered_image, cmap='gray')
plt.title("Median Filtering")
plt.axis('off')
plt.show()


# In[ ]:


#Morphological Operations
# Define a kernel
kernel = np.ones((5, 5), np.uint8)

# Apply Erosion
eroded_image = cv2.erode(image, kernel, iterations=1)

# Display the eroded image
plt.imshow(eroded_image, cmap='gray')
plt.title("Erosion")
plt.axis('off')
plt.show()


# In[ ]:


# Apply an affine transformation
rows, cols = image.shape
points1 = np.float32([[50, 50], [200, 50], [50, 200]])
points2 = np.float32([[10, 100], [200, 50], [100, 250]])
affine_matrix = cv2.getAffineTransform(points1, points2)
affine_transformed_image = cv2.warpAffine(image, affine_matrix, (cols, rows))

# Display the affine transformed image
plt.imshow(affine_transformed_image, cmap='gray')
plt.title("Affine Transformation")
plt.axis('off')
plt.show()


# In[ ]:


# Rotate the image
center = (image.shape[1] // 2, image.shape[0] // 2)
angle = 67  # Angle of rotation
scale = 1.0

# Compute the rotation matrix
rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
rotated_image = cv2.warpAffine(image, rotation_matrix, (image.shape[1], image.shape[0]))

# Display the rotated image
plt.imshow(rotated_image, cmap='gray')
plt.title("Rotated Image")
plt.axis('off')
plt.show()


# <b> Speech Processing </b>

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display


# In[ ]:


# Load the audio file using librosa
file_path = "audio.mp3"
samples, sample_rate = librosa.load(file_path, sr=None)
# Plot the original waveform
plt.figure(figsize=(14, 5))
librosa.display.waveshow(samples, sr=sample_rate)
plt.title("Original Waveform")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()

# Print the sampling rate
print("Sampling Rate:", sample_rate)


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

# Load the audio file using librosa
file_path = "audioe.mp3"
samples, sample_rate = librosa.load(file_path, sr=None)

# Calculate the Zero Crossing Rate
frame_length = 2048
hop_length = 512 
zcr = librosa.feature.zero_crossing_rate(y=samples, frame_length=frame_length, hop_length=hop_length)[0]

# Plot the original waveform
plt.figure(figsize=(14, 5))
librosa.display.waveshow(samples, sr=sample_rate, alpha=0.5)
plt.title("Original Waveform")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")

# Calculate time values for ZCR
frames = np.arange(len(zcr))
t = librosa.frames_to_time(frames, sr=sample_rate, hop_length=hop_length)

# Plot the Zero Crossing Rate
plt.plot(t, zcr, label='Zero Crossing Rate', color='green')

# Add a threshold for highlighting high ZCR regions
threshold = 0.1  # adjust the threshold as needed
zcr_flags = zcr > threshold

# Highlight high ZCR regions
for i, flag in enumerate(zcr_flags):
    if flag:
        plt.axvspan(t[i] - hop_length/sample_rate/2, t[i] + hop_length/sample_rate/2, color='blue', alpha=0.3)

plt.legend()
plt.show()


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

# Load the audio file using librosa
file_path = "audioe.mp3"
samples, sample_rate = librosa.load(file_path, sr=None)
print(f'Sampling rate: {sample_rate} Hz')
# Play audio
# display(Audio(audio, rate=sr))


# Calculate the RMS energy
frame_length = 2048
hop_length = 512
rms = librosa.feature.rms(y=samples, frame_length=frame_length, hop_length=hop_length)[0]

# Set a threshold for detecting voiced regions
threshold = 0.02  # You may need to adjust this value
voiced_flags = rms > threshold

# Plot the original waveform
plt.figure(figsize=(14, 5))
librosa.display.waveshow(samples, sr=sample_rate, alpha=0.5)
plt.title("Original Waveform")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")

# Plot the RMS energy
frames = np.arange(len(rms))
t = librosa.frames_to_time(frames, sr=sample_rate, hop_length=hop_length)
plt.plot(t, rms, label='RMS Energy')

plt.legend()
plt.show()


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

# Load the audio file using librosa with sr=16000
file_path = "saudio.mp3"  # Make sure this path is correct
sample_rate = 44100  # Set the correct sampling rate
samples, _ = librosa.load(file_path, sr=sample_rate)

# Calculate the RMS energy
frame_length = 2048
hop_length = 512
rms = librosa.feature.rms(y=samples, frame_length=frame_length, hop_length=hop_length)[0]

# Set a threshold for detecting voiced regions
threshold = 0.02  # You may need to adjust this value
voiced_flags = rms > threshold

# Plot the original waveform
plt.figure(figsize=(14, 5))
librosa.display.waveshow(samples, sr=sample_rate, alpha=0.5)
plt.title("Original Waveform with Voiced and Unvoiced Regions")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")



# Highlight and annotate voiced and unvoiced regions
prev_flag = None
start_time = 0

for i, flag in enumerate(voiced_flags):
    if prev_flag is None:
        prev_flag = flag
        start_time = t[i]
    elif prev_flag != flag:
        end_time = t[i]
        if prev_flag:  # Voiced region
            plt.axvspan(start_time, end_time, color='red', alpha=0.3)
            plt.text((start_time + end_time) / 2, np.max(samples) * 0.9, 'Voiced', rotation=90, verticalalignment='center', fontsize=10, color='red')
        else:  # Unvoiced region
            plt.axvspan(start_time, end_time, color='blue', alpha=0.3)
            plt.text((start_time + end_time) / 2, np.max(samples) * 0.9, 'Unvoiced', rotation=90, verticalalignment='center', fontsize=10, color='blue')
        start_time = t[i]
        prev_flag = flag

# Handle the last segment
if prev_flag is not None:
    end_time = t[-1]
    if prev_flag:  # Voiced region
        plt.axvspan(start_time, end_time, color='red', alpha=0.3)
        plt.text((start_time + end_time) / 2, np.max(samples) * 0.9, 'Voiced', rotation=90, verticalalignment='center', fontsize=10, color='red')
    else:  # Unvoiced region
        plt.axvspan(start_time, end_time, color='blue', alpha=0.3)
        plt.text((start_time + end_time) / 2, np.max(samples) * 0.9, 'Unvoiced', rotation=90, verticalalignment='center', fontsize=10, color='blue')

plt.legend()
plt.show()


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

# Load the audio file using librosa with sr=16000
file_path = "saudioe.mp3"  # Make sure this path is correct
sample_rate = 44100 # Set the correct sampling rate
samples, _ = librosa.load(file_path, sr=sample_rate)

# Calculate the RMS energy
frame_length = 2048
hop_length = 512
rms = librosa.feature.rms(y=samples, frame_length=frame_length, hop_length=hop_length)[0]

# Calculate the Zero-Crossing Rate (ZCR)
zcr = librosa.feature.zero_crossing_rate(y=samples, frame_length=frame_length, hop_length=hop_length)[0]

# Set a threshold for detecting voiced regions
threshold = 0.02  # You may need to adjust this value
voiced_flags = rms > threshold

# Create time variable for plotting
frames = np.arange(len(rms))
t = librosa.frames_to_time(frames, sr=sample_rate, hop_length=hop_length)

# Plot the original waveform
plt.figure(figsize=(14, 5))
librosa.display.waveshow(samples, sr=sample_rate, alpha=0.5)
plt.title("Original Waveform with Voiced and Unvoiced Regions")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")

# Plot the ZCR
plt.plot(t, zcr, label='ZCR', color='green')

# Plot the RMS energy
plt.plot(t, rms, label='RMS Energy', color='orange')

# Highlight and annotate voiced and unvoiced regions
prev_flag = None
start_time = 0
for i, flag in enumerate(voiced_flags):
    if prev_flag is None:
        prev_flag = flag
        start_time = t[i]
    elif prev_flag != flag:
        end_time = t[i]
        if prev_flag:  # Voiced region
            plt.axvspan(start_time, end_time, color='red', alpha=0.3)
            plt.text((start_time + end_time) / 2, np.max(samples) * 0.9, 'Voiced', rotation=90, verticalalignment='center', fontsize=10, color='red')
        else:  # Unvoiced region
            plt.axvspan(start_time, end_time, color='darkblue', alpha=0.5)  # Darker blue
            plt.text((start_time + end_time) / 2, np.max(samples) * 0.9, 'Unvoiced', rotation=90, verticalalignment='center', fontsize=10, color='black')  # Black text
        start_time = t[i]
        prev_flag = flag

# Handle the last segment if exists
if prev_flag is not None:
    end_time = t[-1]
    if prev_flag:  # Voiced region
        plt.axvspan(start_time, end_time, color='red', alpha=0.3)
        plt.text((start_time + end_time) / 2, np.max(samples) * 0.9, 'Voiced', rotation=90, verticalalignment='center', fontsize=10, color='red')
    else:  # Unvoiced region
        plt.axvspan(start_time, end_time, color='darkblue', alpha=0.5)  # Darker blue
        plt.text((start_time + end_time) / 2, np.max(samples) * 0.9, 'Unvoiced', rotation=90, verticalalignment='center', fontsize=10, color='black')  # Black text

# Print the duration of the audio
duration = librosa.get_duration(y=samples, sr=sample_rate)
print(f"Duration of the audio file: {duration:.2f} seconds")

plt.legend()
plt.show()


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

# Load your audio file
file_path = "audio.mp3"  # Update with your audio file path
sample_rate = 44100  # Set the correct sampling rate
samples, _ = librosa.load(file_path, sr=sample_rate)

# Calculate the RMS energy
frame_length = 2048
hop_length = 512
rms = librosa.feature.rms(y=samples, frame_length=frame_length, hop_length=hop_length)[0]

# Calculate the Zero-Crossing Rate (ZCR)
zcr = librosa.feature.zero_crossing_rate(y=samples, frame_length=frame_length, hop_length=hop_length)[0]

# Convert frames to time
frames = np.arange(len(rms))
t_rms = librosa.frames_to_time(frames, sr=sample_rate, hop_length=hop_length)
t_zcr = librosa.frames_to_time(frames, sr=sample_rate, hop_length=hop_length)

# Set a threshold for detecting voiced regions (you may need to tune this)
threshold_rms = 0.02
voiced_flags = rms > threshold_rms

# Create a figure with subplots for original signal, RMS and ZCR
plt.figure(figsize=(14, 10))

# Plot original signal
plt.subplot(3, 1, 1)
librosa.display.waveshow(samples, sr=sample_rate, alpha=0.5)
plt.title("Original Waveform")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")

# Highlight voiced and unvoiced regions
prev_flag = None
start_time = 0
for i, flag in enumerate(voiced_flags):
    if prev_flag is None:
        prev_flag = flag
        start_time = t_rms[i]
    elif prev_flag != flag:
        end_time = t_rms[i]
        color = 'red' if prev_flag else 'blue'
        plt.axvspan(start_time, end_time, color=color, alpha=0.3, label='Voiced' if prev_flag else 'Unvoiced')
        prev_flag = flag
        start_time = t_rms[i]

# Handle the last segment
if prev_flag is not None:
    end_time = t_rms[-1]
    color = 'red' if prev_flag else 'blue'
    plt.axvspan(start_time, end_time, color=color, alpha=0.3, label='Voiced' if prev_flag else 'Unvoiced')

plt.legend()
plt.tight_layout()

# Plot RMS energy
plt.subplot(3, 1, 2)
plt.plot(t_rms, rms, label='RMS Energy', color='orange')
plt.title("RMS Energy")
plt.xlabel("Time (s)")
plt.ylabel("Energy")
plt.legend()

# Plot ZCR
plt.subplot(3, 1, 3)
plt.plot(t_zcr, zcr, label='Zero-Crossing Rate', color='green')
plt.title("Zero-Crossing Rate (ZCR)")
plt.xlabel("Time (s)")
plt.ylabel("ZCR")
plt.legend()

# Adjust layout and show the plot
plt.tight_layout()
plt.show()


# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

# Function to load and visualize the waveform
def load_and_plot_waveform(file_path):
    samples, sample_rate = librosa.load(file_path, sr=None)
    plt.figure(figsize=(14, 5))
    librosa.display.waveshow(samples, sr=sample_rate)
    plt.title("Original Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.show()
    return samples, sample_rate

# Function to compute and plot Zero Crossing Rate (ZCR)
def plot_zcr(samples, sample_rate, frame_length=2048, hop_length=512, threshold=0.1):
    zcr = librosa.feature.zero_crossing_rate(y=samples, frame_length=frame_length, hop_length=hop_length)[0]
    plt.figure(figsize=(14, 5))
    librosa.display.waveshow(samples, sr=sample_rate, alpha=0.5)
    plt.title("Waveform and Zero Crossing Rate")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")

    frames = np.arange(len(zcr))
    t = librosa.frames_to_time(frames, sr=sample_rate, hop_length=hop_length)
    plt.plot(t, zcr, label='Zero Crossing Rate', color='green')

    zcr_flags = zcr > threshold
    for i, flag in enumerate(zcr_flags):
        if flag:
            plt.axvspan(t[i] - hop_length/sample_rate/2, t[i] + hop_length/sample_rate/2, color='blue', alpha=0.3)

    plt.legend()
    plt.show()

# Function to compute and plot RMS energy
def plot_rms(samples, sample_rate, frame_length=2048, hop_length=512):
    rms = librosa.feature.rms(y=samples, frame_length=frame_length, hop_length=hop_length)[0]
    plt.figure(figsize=(14, 5))
    librosa.display.waveshow(samples, sr=sample_rate, alpha=0.5)
    plt.plot(librosa.frames_to_time(np.arange(len(rms)), sr=sample_rate, hop_length=hop_length), rms, label='RMS Energy', color='orange')
    plt.title("Waveform and RMS Energy")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude / RMS")
    plt.legend()
    plt.show()

# Function to compute and plot STFT, Spectral Centroid, and MFCC
def plot_spectral_features(samples, sample_rate, n_fft=2048, hop_length=512, n_mfcc=13):
    D = librosa.stft(samples, n_fft=n_fft, hop_length=hop_length)
    DB = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    spectral_centroid = librosa.feature.spectral_centroid(y=samples, sr=sample_rate, n_fft=n_fft, hop_length=hop_length)[0]
    mfccs = librosa.feature.mfcc(y=samples, sr=sample_rate, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)

    frames = np.arange(mfccs.shape[1])
    t = librosa.frames_to_time(frames, sr=sample_rate, hop_length=hop_length)

    plt.figure(figsize=(15, 10))

    plt.subplot(3, 1, 1)
    librosa.display.specshow(DB, sr=sample_rate, hop_length=hop_length, x_axis='time', y_axis='log', cmap='coolwarm')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Short-Time Fourier Transform (STFT)')

    plt.subplot(3, 1, 3)
    librosa.display.specshow(mfccs, sr=sample_rate, x_axis='time', hop_length=hop_length, cmap='coolwarm')
    plt.colorbar()
    plt.title('Mel-Frequency Cepstral Coefficients (MFCCs)')

    plt.tight_layout()
    plt.show()

# File path to the audio file
file_path = "saudioe.mp3" # Update with the actual file path

# Run the tasks
samples, sample_rate = load_and_plot_waveform(file_path)
plot_zcr(samples, sample_rate)
plot_rms(samples, sample_rate)
plot_spectral_features(samples, sample_rate)

