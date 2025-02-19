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
          @added="previewImage"
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

const email = ref('');
const password = ref('');
const passwordConfirm = ref('');
const username = ref('');
const termsAccepted = ref(false);
const profilePicture = ref(null);
const imageUrl = ref(null);

// Computed property to check if passwords match
const passwordMismatch = computed(() => password.value !== passwordConfirm.value);

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
    profilePicture: profilePicture.value,
  });
  var signupData = {
    email: email.value,
    password: password.value,
    passwordConfirm: passwordConfirm.value,
    username: username.value,
    termsAccepted: termsAccepted.value,
    profilePicture: profilePicture.value,
  };

  fetch('/auth/register', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(signupData)
  })
  .then(response => response.json())
  .then(data => {
    // Handle successful signup
    console.log('Signup successful:', data);
  })
  .catch(error => {
    // Handle signup error
    console.error('Signup error:', error);
  });
};

// Function to preview the image
const previewImage = () => {
  const file = profilePicture.value?.[0]; // Get the first file from the array
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      imageUrl.value = e.target.result; // Set the result as the image URL
    };
    reader.readAsDataURL(file); // Convert the file to a base64 string
  }
};
</script>
