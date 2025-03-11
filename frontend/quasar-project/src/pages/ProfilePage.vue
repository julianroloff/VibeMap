<template>
  <div class=" text-primary text-center q-pa-md flex flex-center w-100">
    <q-list class="w-100">
      <!-- Show Profile Section if NOT logged in -->
      <template v-if="!isLoggedIn">
        <q-item class="q-pa-md column items-center w-100">
          <q-avatar size="72px">
            <img src="../assets/vibemap-logo.svg" alt="User Avatar" />
          </q-avatar>
          <div class="q-mt-md text-h6">Welcome</div>
          <div class="text-caption text-grey">Please login or sign up</div>
        </q-item>

        <q-separator />

        <q-item class="w-100">
          <q-input v-model="email" label="Email" type="email" filled  class="full-width"/>
        </q-item>
        <q-item class="w-100">
          <q-input v-model="password" label="Password" type="password" filled  class="full-width"/>
        </q-item>

        <q-item class="q-gutter-sm w-100">
          <q-btn label="Login" color="primary" class="col-6" @click="login" />
          <q-btn label="Signup" color="secondary" outline class="col-6" to="./signup" />
        </q-item>
      </template>

      <!-- Show Profile Section if logged in -->
      <template v-if="isLoggedIn">
          <q-item class="q-pa-md column items-center w-100" v-for="(userInfo, index) in userInfo" :key="index">
            <q-avatar size="160px">
              <img src="{{ userInfo.picture }}" alt="User Avatar" />
              <q-file class="picture-edit" v-model="profilePicture" filled accept="image/*" :max-files="1" @added="previewImage" v-if="profileEdit" />
              <q-icon class="picture-edit-icon" name="edit" v-if="profileEdit"/>
            </q-avatar>
            <div class="q-mt-md text-h6">{{ userInfo.username }}</div>
            <div class="text-caption text-grey">{{ userInfo.email }}</div>
          </q-item>
          <q-separator />
          <q-item clickable v-ripple class="" @click="editProfile" v-if="!profileEdit">
            <q-item-section avatar>
              <q-icon name="edit" />
            </q-item-section>
            <q-item-section>Edit profile</q-item-section>
          </q-item>
          <q-item clickable v-ripple class="" @click="saveProfile" v-if="profileEdit">
            <q-item-section avatar>
              <q-icon name="save" />
            </q-item-section>
            <q-item-section>Save profile</q-item-section>
          </q-item>
          <q-item clickable v-ripple class="text-red" @click="logout">
            <q-item-section avatar>
              <q-icon name="logout" color="red" />
            </q-item-section>
            <q-item-section>Logout</q-item-section>
          </q-item>
      </template>
    </q-list>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'

export default {
  setup () {
    const userInfo = ref([
        { username: "User", userId: 1, email: "email@email.com", picture: "data:image/png;base64,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", token: "password"}
      ]);
    const error = ref(null);
    const isLoggedIn = ref(true)
    const loggedInId = ref("")
    const profileEdit = ref(false)
    const email = ref("")
    const password = ref("")
    const usertoken = ref("")
    //const storedEmail = userInfo.value[0].email
    //const storedPassword = userInfo.value[0].token

    // Check if the user is logged in by reading localStorage
    onMounted(() => {
      isLoggedIn.value = localStorage.getItem("isLoggedIn") === "true";
      loggedInId.value = localStorage.getItem("loggedInId");
      usertoken.value = localStorage.getItem("usertoken");
      //localStorage.setItem("isLoggedIn", "true") 
      console.log(isLoggedIn.value);
      //console.log(profileEdit.value)
      console.log(usertoken.value);
      fetchUserData(usertoken.value);
    })

    const fetchUserData = async (token) => {
      console.log(token)
      try {
        const response = await fetch('https://vibemapbe.com/auth/auth/me', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        userInfo.value[0] = {
          ...userInfo.value[0], // Keep existing fields
          username: data.email, // Update username from API
          email: data.email, // Update email from API
          userId: data.id, // Update userId from API
          token: token, // Update token from API
        };
      } catch (err) {
        error.value = err.message || 'Failed to fetch user data';
      }
    };

    const login = async () => {
      if (email.value && password.value) {
        const requestBody = {
          email: email.value,
          password: password.value
        };
        try {
          const response = await fetch("https://vibemapbe.com/auth/auth/login", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify(requestBody),
          });

          if (response.ok) {
            isLoggedIn.value = true;
            localStorage.setItem('isLoggedIn', 'true')
            const data = await response.json();
            console.log(data); 
            usertoken.value = data.access_token;
            localStorage.setItem('usertoken', data.access_token)
            this.$router.push('/');
            alert("Login successful! Welcome back " + email.value);
          } else {
            console.error("Login failed", response.responseText);
            alert("Login failed", response.responseText);
          }
        } catch (error) {
          console.error("Error during login", error);
        }
      } else {
        console.error("Email and password are required");
        alert("Email and password are required");
      }
    };

    const logout = () => {
      isLoggedIn.value = false;
      localStorage.setItem('isLoggedIn', 'false')
      localStorage.setItem('loggedInId', null)
      email.value = "";
      password.value = "";
      refreshPage();
    };
    const refreshPage = () => {
      location.reload(); // Reloads the current page
    };
    const editProfile = () => {
      profileEdit.value = true;
      console.log(profileEdit.value)
    };
    const saveProfile = () => {
      profileEdit.value = false;
      console.log(profileEdit.value)
    };

    return {
      login,
      logout,
      editProfile,
      saveProfile,
      profileEdit,
      email,
      password,
      isLoggedIn,
      loggedInId,
      userInfo
    }
  }
}
</script>
