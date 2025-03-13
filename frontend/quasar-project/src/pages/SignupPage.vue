<template>
  <div class="text-primary text-center q-pa-md flex flex-center">
    <div>
      <div class="text-h5">Signup Page</div>

      <q-form class="q-gutter-md signup-form" @submit.prevent="submitForm">
        
        <!-- Username -->
        <q-input
          v-model="username"
          label="Username"
          filled
          required
        />

        <!-- Profile Picture Upload -->
        <q-file
          v-model="profilePicture"
          label="Upload Profile Picture"
          filled
          accept="image/*"
          :max-files="1"
          @update:model-value="handleFileUpload"
        />

        <!-- Image Preview or Placeholder -->
        <div v-if="imageUrl" class="q-mt-md">
          <img :src="imageUrl" alt="Profile Preview" class="q-mb-md" style="max-width: 200px; max-height: 200px; object-fit: cover;" />
        </div>
        <div v-else class="q-mt-md" style="max-width: 200px; max-height: 200px; border: 2px dashed #ccc; display: flex; justify-content: center; align-items: center; font-size: 14px; color: #aaa;">
          No Image Uploaded
        </div>


        <!-- Email Address -->
        <q-input
          v-model="email"
          label="Email Address"
          type="email"
          filled
          required
        />

        <!-- Password -->
        <q-input
          v-model="password"
          label="Password"
          type="password"
          filled
          required
        />

        <!-- Password Confirmation -->
        <q-input
          v-model="passwordConfirm"
          label="Confirm Password"
          type="password"
          filled
          required
          :error="passwordMismatch"
          :error-message="'Passwords do not match'"
        />


        <!-- Terms of Use -->
        <q-checkbox
          v-model="termsAccepted"
          label="I agree to the Terms of Use"
          required
        />

        <!-- Submit Button -->
        <q-btn
          label="Sign Up"
          color="primary"
          type="submit"
          unelevated
          class="q-mt-md"
        />
      </q-form>

      <div class="text-h6" style="opacity:.4">
        Already have an account? <q-btn flat to="/profile" label="Login" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const passwordConfirm = ref('');
const username = ref('');
const termsAccepted = ref(false);
const profilePicture = ref(null);
const imageUrl = ref(null);
const response = "";

// Computed property to check if passwords match
const passwordMismatch = computed(() => password.value !== passwordConfirm.value);

const router = useRouter();

// Function to resize and compress the image
const resizeImage = (file, maxWidth = 180, maxHeight = 180, maxSizeInKB = 40) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      const img = new Image();
      img.src = e.target.result;

      img.onload = () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        // Calculate new dimensions while maintaining aspect ratio
        let width = img.width;
        let height = img.height;

        if (width > height) {
          if (width > maxWidth) {
            height *= maxWidth / width;
            width = maxWidth;
          }
        } else {
          if (height > maxHeight) {
            width *= maxHeight / height;
            height = maxHeight;
          }
        }

        // Set canvas dimensions
        canvas.width = width;
        canvas.height = height;

        // Draw the image on the canvas
        ctx.drawImage(img, 0, 0, width, height);

        // Function to compress the image iteratively
        const compressImage = (quality) => {
          return new Promise((resolve, reject) => {
            canvas.toBlob(
              (blob) => {
                if (!blob) {
                  reject(new Error('Failed to compress image.'));
                  return;
                }

                // Check if the blob size is within the limit
                if (blob.size / 1024 <= maxSizeInKB) {
                  resolve(blob);
                } else {
                  // Reduce quality and try again
                  const newQuality = quality - 0.1; // Reduce quality by 10%
                  if (newQuality >= 0.1) {
                    compressImage(newQuality).then(resolve).catch(reject);
                  } else {
                    reject(new Error('Unable to compress image below the specified size.'));
                  }
                }
              },
              'image/jpeg', // You can change this to 'image/png' if needed
              quality // Quality parameter (0.8 = 80% quality)
            );
          });
        };

        // Start compression with an initial quality of 0.9 (90%)
        compressImage(0.9)
          .then((blob) => resolve(blob))
          .catch((error) => reject(error));
      };

      img.onerror = (error) => {
        reject(error);
      };
    };

    reader.onerror = (error) => {
      reject(error);
    };

    reader.readAsDataURL(file); // Read the file as a data URL
  });
};

const handleFileUpload = async (profilePicture) => {
  if (profilePicture) {
    try {
      // Resize the image to 180x180 pixels and reduce quality
      const resizedImage = await resizeImage(profilePicture);

      // Convert the resized image blob to a base64 URL
      const reader = new FileReader();
      reader.onload = (e) => {
        imageUrl.value = e.target.result; // Set the resized image URL
      };
      reader.readAsDataURL(resizedImage);
    } catch (error) {
      console.error('Error resizing image:', error);
      alert('Failed to resize image. Please try again.');
    }
  } else {
    imageUrl.value = ''; // Clear the image if no file is selected
  }
};

const saveToLocalStorage = () => {
  if (imageUrl.value) {
    localStorage.setItem('uploadedImage', imageUrl.value);
    console.log('Image saved to local storage.');
  }
};

const submitForm = () => {
  if (passwordMismatch.value) {
    return; // Stop form submission if passwords do not match
  }

  // Handle form submission logic
  console.log({
    email: email.value,
    password: password.value,
    passwordConfirm: passwordConfirm.value,
    username: username.value,
    termsAccepted: termsAccepted.value,
    profilePicture: imageUrl.value,
  });
  var signupData = {
    email: email.value,
    password: password.value,
    //passwordConfirm: passwordConfirm.value,
    username: username.value,
    //termsAccepted: termsAccepted.value,
    //profilePicture: profilePicture.value,
    //profilePicture: imageUrl.value,
  };

  fetch('https://vibemapbe.com/auth/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(signupData)
  })
  .then(response => response.json())
  .then(data => {
    if(response.status != 200){
      alert(data);
      router.push('/profile');
    }
    else{
      // Handle successful signup
      console.log('Signup successful:', data);
      router.push('/');
      saveToLocalStorage();
    }
  })
  .catch(error => {
    // Handle signup error
    console.error('Signup error:', error);
    alert('Signup failed. Please try again. Error: ' + error);
  });
};

// Function to preview the image
//const previewImage = () => {
//  const file = profilePicture.value; // Get the first file from the array
//  if (file) {
//    const reader = new FileReader();
//    reader.onload = (e) => {
//      imageUrl.value = e.target.result; // Set the result as the image URL
//    };
//    reader.readAsDataURL(file); // Convert the file to a base64 string
//  }
//};

</script>
