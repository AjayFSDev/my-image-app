<template>
  <div class="dashboard">
    <h1>Your Dashboard</h1>

    <div class="upload-section">
      <h2>Upload Images/Files</h2>
      <input type="file" @change="handleFileUpload" accept="image/*" />
      <button @click="uploadImage">Upload</button>
    </div>

    <div v-if="selectedImage" class="selected-image-preview">
      <h2>Image Preview</h2>
      <img :src="selectedImage" alt="Selected Image" />
    </div>

    <div class="uploaded-images-section">
      <h2>Your Uploaded Images</h2>
      <div v-if="images.length === 0" class="no-images">
        No images uploaded yet.
      </div>
      <div v-else class="image-gallery">
        <div v-for="(image, index) in images" :key="index" class="image-container">
          <img :src="image" alt="Uploaded Image" />
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const images = ref<string[]>([]);
    const selectedFile = ref<File | null>(null);
    const selectedImage = ref<string | null>(null);

    const handleFileUpload = (event: Event) => {
      const target = event.target as HTMLInputElement;
      if (target.files && target.files.length > 0) {
        selectedFile.value = target.files[0];
        selectedImage.value = URL.createObjectURL(target.files[0]);
      }
    };

    const uploadImage = async () => {
      if (selectedFile.value) {
        const formData = new FormData();
        formData.append('file', selectedFile.value);

        try {
          const response = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData,
          });

          if (response.ok) {
            fetchImages(); // Refresh the image list after upload
            selectedFile.value = null; // Reset the file input
            selectedImage.value = null; // Reset the preview image
          } else {
            const data = await response.json();
            alert(data.error || 'Failed to upload!');
          }
        } catch (error) {
          console.error('Error uploading image:', error);
        }
      } else {
        alert('Please select a file to upload.');
      }
    };

    const fetchImages = async () => {
      try {
        const response = await fetch('http://localhost:5000/images');
        const data = await response.json();
        images.value = data.map((img: string) => `http://localhost:5000${img}`); // Construct full URL
      } catch (error) {
        console.error('Error fetching images:', error);
      }
    };

    // Fetch images when the component is mounted
    onMounted(() => {
      fetchImages();
    });

    return { images, handleFileUpload, uploadImage, selectedImage };
  },
};
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  align-items: center; /* Center horizontally */
  justify-content: center; /* Center vertically */
  min-height: 100vh; /* Full viewport height */
  text-align: center; /* Center text */
  background-color: #f9f9f9; /* Light background color */
  padding: 20px;
}

h1 {
  margin-bottom: 20px;
}

.upload-section,
.uploaded-images-section {
  background-color: white; /* White background for sections */
  border-radius: 8px; /* Rounded corners */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
  padding: 20px;
  margin-bottom: 20px;
  width: 100%; /* Full width */
  max-width: 600px; /* Max width for larger screens */
}

.upload-section h2,
.uploaded-images-section h2 {
  margin: 10px 0;
}

input[type="file"] {
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  background-color: #4caf50; /* Green background */
  color: white; /* White text */
  border: none;
  border-radius: 5px; /* Rounded corners */
  cursor: pointer;
}

button:hover {
  background-color: #45a049; /* Darker green on hover */
}

.no-images {
  margin: 10px 0;
  font-style: italic; /* Italic for no images message */
}

.image-gallery {
  display: flex;
  flex-wrap: wrap; /* Allow images to wrap */
  justify-content: center; /* Center images */
  margin-top: 20px;
}

.image-container {
  margin: 10px;
}

img {
  max-width: 100px; /* Set a max width */
  border: 2px solid #ccc; /* Add a border */
  border-radius: 5px; /* Rounded corners */
}

.selected-image-preview {
  margin-top: 20px;
}
</style>
