<template>
  <q-layout view="hHh lpR fFf" >

    <q-header elevated class="bg-transparent text-primary overflow-hidden p-5 pb-5">
      <q-toolbar class="q-card">
        <q-btn dense flat round icon="menu" @click="toggleLeftDrawer"/>

        <q-toolbar-title class="text-center font-karla fw-600" @click="goHome">
          <q-avatar>
            <img src="../assets/vibemap-logo.svg" alt="VibeMap Logo" @click="goHome"/>
          </q-avatar>
          <q-btn dense flat round @click="goHome" class="font-karla logotext">vibemap</q-btn>
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
        vibemap v0.2.1
      </div>
    </q-drawer>

    <q-drawer v-model="rightDrawerOpen" side="right" bordered>
      <ProfilePage />
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import ProfilePage from 'pages/ProfilePage.vue' // Adjust the path as necessary

export default {
  components: {
    ProfilePage
  },
  setup () {
    const leftDrawerOpen = ref(false)
    const rightDrawerOpen = ref(false)
    const isLoggedIn = ref(false)
    const loggedInId = ref("")
    const email = ref("")
    const password = ref("")
    const route = useRoute()  // Access the current route
    const router = useRouter() 
    const nightMode = ref(false);

    const menuList = [
      { icon: "map", label: "Map", separator: false, to: "/" },
      { icon: "thumbs_up_down", label: "Ratings", separator: false, to: "/myratings" },
      { icon: "person", label: "Profile", separator: true, to: "/profile" },
      { icon: "settings", label: "Settings", separator: false, to: "/settings" },
      { icon: "feedback", label: "Send Feedback", separator: false, to: "/feedback" },
      { icon: "help", label: "Help", separator: false, to: "/help" },
    ]

    

    // Check if the user is logged in by reading localStorage
    onMounted(() => {
      isLoggedIn.value = localStorage.getItem("isLoggedIn") === "true";
      nightMode.value = JSON.parse(localStorage.getItem("nightMode")) || false;
      loggedInId.value = localStorage.getItem("loggedInId");
      //localStorage.setItem("isLoggedIn", "true") 
      //console.log(isLoggedIn.value);
    })

    const goHome = () => {
        router.push("/")
    }

    // Function to determine if a menu item is active
    const isActive = (menuItem) => {
      return route.path === menuItem.to
    }


    return {
      leftDrawerOpen,
      rightDrawerOpen,
      menuList,
      isActive,  // Add this to template to use the active state
      email,
      password,
      isLoggedIn,  // Ensure this is reactive
      loggedInId,
      nightMode,
      toggleLeftDrawer() {
        leftDrawerOpen.value = !leftDrawerOpen.value
      },
      toggleRightDrawer() {
        rightDrawerOpen.value = !rightDrawerOpen.value
      },
      goHome
    }
  }
}
</script>