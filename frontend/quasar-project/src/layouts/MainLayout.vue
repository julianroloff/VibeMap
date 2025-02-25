<template>
  <q-layout view="hHh lpR fFf" >

    <q-header elevated class="bg-transparent text-primary overflow-hidden p-5 pb-5">
      <q-toolbar class="q-card">
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer" />

        <q-toolbar-title class="text-center font-karla fw-600">
          <q-avatar>
            <img src="../assets/vibemap-logo.svg" alt="VibeMap Logo" />
          </q-avatar>
          vibemap
        </q-toolbar-title>

        <q-btn dense flat round icon="person" @click="toggleRightDrawer" />
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen" side="left" bordered>
      <q-scroll-area class="fit">
        <q-list>
          <template v-for="(menuItem, index) in menuList" :key="index">
            <q-item
              clickable
              :active="isActive(menuItem)"
              v-ripple
              :to="menuItem.to"
            >
              <q-item-section avatar>
                <q-icon :name="menuItem.icon" />
              </q-item-section>
              <q-item-section>
                {{ menuItem.label }}
              </q-item-section>
            </q-item>
            <q-separator :key="'sep' + index" v-if="menuItem.separator" />
          </template>
        </q-list>
      </q-scroll-area>
      <div class="version-info text-caption text-grey text-center">
        vibemap v0.1.2
      </div>
    </q-drawer>

    <q-drawer v-model="rightDrawerOpen" side="right" bordered>
      <q-scroll-area class="fit">
        <q-list>
          <!-- Show Login Form if not logged in -->
          <template v-if="!isLoggedIn">
            <q-item class="q-pa-md column items-center">
              <q-avatar size="72px">
                <img src="../assets/vibemap-logo.svg" alt="User Avatar" />
              </q-avatar>
              <div class="q-mt-md text-h6">Welcome</div>
              <div class="text-caption text-grey">Please login or sign up</div>
            </q-item>

            <q-separator />

            <q-item>
              <q-input v-model="email" label="Email" type="email" filled  class="full-width"/>
            </q-item>
            <q-item>
              <q-input v-model="password" label="Password" type="password" filled  class="full-width"/>
            </q-item>

            <q-item class="q-gutter-sm w-100">
              <q-btn label="Login" color="primary" class="col-6" @click="login" />
              <q-btn label="Signup" color="secondary" outline class="col-6" to="./signup" />
            </q-item>
          </template>

          <!-- Show Profile Section if logged in -->
          <template v-else>
            <q-item class="q-pa-md column items-center">
              <q-avatar size="72px">
                <img src="../assets/agos-profile.jpeg" alt="User Avatar" />
              </q-avatar>
              <div class="q-mt-md text-h6">Agoston</div>
              <div class="text-caption text-grey">agoston@email.com</div>
            </q-item>

            <q-separator />

            <q-item clickable v-ripple to="./profile">
              <q-item-section avatar>
                <q-icon name="person" />
              </q-item-section>
              <q-item-section>Profile</q-item-section>
            </q-item>

            <q-item clickable v-ripple to="./help">
              <q-item-section avatar>
                <q-icon name="help_outline" />
              </q-item-section>
              <q-item-section>Help</q-item-section>
            </q-item>

            <q-separator />

            <q-item clickable v-ripple class="text-red" @click="logout">
              <q-item-section avatar>
                <q-icon name="logout" color="red" />
              </q-item-section>
              <q-item-section>Logout</q-item-section>
            </q-item>
          </template>
        </q-list>
      </q-scroll-area>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>

    <!--q-footer elevated class="bg-grey-8 text-white">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg">
          </q-avatar>
          <div>Title</div>
        </q-toolbar-title>
      </q-toolbar>
    </q-footer-->

  </q-layout>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

export default {
  setup () {
    const leftDrawerOpen = ref(false)
    const rightDrawerOpen = ref(false)
    const isLoggedIn = ref(false)
    const loggedInId = ref("")
    const email = ref("")
    const password = ref("")
    const route = useRoute()  // Access the current route
    const nightMode = ref(false);

    const menuList = [
      { icon: "map", label: "Map", separator: false, to: "/" },
      { icon: "thumbs_up_down", label: "My ratings", separator: false, to: "/myratings" },
      { icon: "person", label: "Profile", separator: true, to: "/profile" },
      { icon: "settings", label: "Settings", separator: false, to: "/settings" },
      { icon: "feedback", label: "Send Feedback", separator: false, to: "/feedback" },
      { icon: "help", label: "Help", separator: false, to: "/help" },
    ]

    const userInfo = ref([
      { username: "Ágoston", email: "agoston@email.com", picture: "src/assets/agos-profile.jpeg", token: "password"},
      { username: "Julian", email: "julian@email.com", picture: "src/assets/julian_profile.jpeg", token: "pass"},
      { username: "Diemer", email: "diemer@email.com", picture: "src/assets/vibemap-logo.svg", token: "pass"},
      { username: "Eduardo", email: "eduardo@email.com", picture: "src/assets/vibemap-logo.svg", token: "pass"},
      { username: "Jippe", email: "jippe@email.com", picture: "src/assets/vibemap-logo.svg", token: "pass"}
    ]);
    const storedEmail = userInfo.value[0].email
    const storedPassword = userInfo.value[0].token

    // Check if the user is logged in by reading localStorage
    onMounted(() => {
      isLoggedIn.value = localStorage.getItem("isLoggedIn") === "true";
      nightMode.value = JSON.parse(localStorage.getItem("nightMode")) || false;
      loggedInId.value = localStorage.getItem("loggedInId");
      //localStorage.setItem("isLoggedIn", "true") 
      //console.log(isLoggedIn.value);
    })

    // Function to determine if a menu item is active
    const isActive = (menuItem) => {
      return route.path === menuItem.to
    }

    const login = async () => {
      if (email.value && password.value) {

        //Remove the following check and enable the commented section when backend is connected!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if (email.value == storedEmail) {
          if (password.value == storedPassword) {
            isLoggedIn.value = true;
            localStorage.setItem('isLoggedIn', 'true')
            localStorage.setItem('loggedInId', Number(userInfo.value[0].userId))
            refreshPage();
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
      localStorage.removeItem("isLoggedIn");
      localStorage.setItem('loggedInId', '')
      email.value = "";
      password.value = "";
      refreshPage();
    };
    const refreshPage = () => {
      location.reload(); // Reloads the current page
    };

    return {
      leftDrawerOpen,
      rightDrawerOpen,
      menuList,
      isActive,  // Add this to template to use the active state
      login,
      logout,
      email,
      password,
      isLoggedIn,  // Ensure this is reactive
      loggedInId,
      userInfo,
      nightMode,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value
      },
      toggleRightDrawer() {
        rightDrawerOpen.value = !rightDrawerOpen.value
      }
    }
  }
}
</script>