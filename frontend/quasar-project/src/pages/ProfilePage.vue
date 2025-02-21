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
              <img :src=userInfo.picture alt="User Avatar" />
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
      { username: "Ágoston", userId: 1, email: "agoston@email.com", picture: "src/assets/agos-profile.jpeg", token: "password"},
      //{ username: "Julian", userId: 2, email: "julian@email.com", picture: "src/assets/julian_profile.jpeg", token: "pass"}
    ]);
    const isLoggedIn = ref(true)
    const loggedInId = ref("")
    const profileEdit = ref(false)
    const email = ref("")
    const password = ref("")
    const storedEmail = userInfo.value[0].email
    const storedPassword = userInfo.value[0].token

    // Check if the user is logged in by reading localStorage
    onMounted(() => {
      isLoggedIn.value = localStorage.getItem("isLoggedIn") === "true";
      loggedInId.value = localStorage.getItem("loggedInId");
      //localStorage.setItem("isLoggedIn", "true") 
      //console.log(isLoggedIn.value);
      //console.log(profileEdit.value)
    })

    const login = async () => {
      if (email.value && password.value) {

        //Remove the following check and enable the commented section when backend is connected!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if (email.value == storedEmail) {
          if (password.value == storedPassword) {
            isLoggedIn.value = true;
            localStorage.setItem('isLoggedIn', 'true')
            localStorage.setItem('loggedInId', Number(userInfo.value[0].userId))
          }
          else {
            alert("Wrong password or email address Try again.")
          }
        }
        /*const requestBody = {
          email: email.value,
          password: password.value
        };
        try {
          const response = await fetch("http://localhost:8001/auth/register", {
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
          } else {
            console.error("Login failed", response.statusText);
          }
        } catch (error) {
          console.error("Error during login", error);
        }*/
      } else {
        console.error("Email and password are required");
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
