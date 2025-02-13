<template>
  <q-layout view="hHh lpR fFf">

    <q-header elevated class="bg-transparent text-primary overflow-hidden m-5 pb-5">
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

    <q-drawer show-if-above v-model="leftDrawerOpen" side="left" bordered>
      <q-scroll-area class="fit">
          <q-list>
            <template v-for="(menuItem, index) in menuList" :key="index">
              <q-item clickable :active="menuItem.label === 'Map'" v-ripple>
                <q-item-section avatar>
                  <q-icon :name="menuItem.icon" />
                </q-item-section>
                <q-item-section>
                  {{ menuItem.label }}
                </q-item-section>
              </q-item>
              <q-separator :key="'sep' + index"  v-if="menuItem.separator" />
            </template>

          </q-list>
        </q-scroll-area>
        <div class="version-info text-caption text-grey text-center">
          vibemap v0.1.1
        </div>
    </q-drawer>

    <q-drawer show-if-above v-model="rightDrawerOpen" side="right" bordered>
      <q-scroll-area class="fit">
        <q-list>
          <!-- Profile Header -->
          <q-item class="q-pa-md column items-center">
            <q-avatar size="72px">
              <img src="../assets/agos-profile.jpeg" alt="User Avatar" />
            </q-avatar>
            <div class="q-mt-md text-h6">Agoston</div>
            <div class="text-caption text-grey">agoston@email.com</div>
          </q-item>

          <q-separator />

          <!-- Menu Options -->
          <q-item clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="settings" />
            </q-item-section>
            <q-item-section>Settings</q-item-section>
          </q-item>

          <q-item clickable v-ripple>
            <q-item-section avatar>
              <q-icon name="help_outline" />
            </q-item-section>
            <q-item-section>Help</q-item-section>
          </q-item>

          <q-separator />

          <!-- Logout -->
          <q-item clickable v-ripple class="text-red">
            <q-item-section avatar>
              <q-icon name="logout" color="red" />
            </q-item-section>
            <q-item-section>Logout</q-item-section>
          </q-item>
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
import { ref } from 'vue'

export default {
  setup () {
    const leftDrawerOpen = ref(false)
    const rightDrawerOpen = ref(false)

    return {
      leftDrawerOpen,
      toggleLeftDrawer () {
        leftDrawerOpen.value = !leftDrawerOpen.value
      },

      rightDrawerOpen,
      toggleRightDrawer () {
        rightDrawerOpen.value = !rightDrawerOpen.value
      },

      drawer: ref(false),
      menuList
    }
  }
}
const menuList = [
  {
    icon: 'map',
    label: 'Map',
    separator: false
  },
  {
    icon: 'thumbs_up_down',
    label: 'My ratings',
    separator: true
  },
  {
    icon: 'settings',
    label: 'Settings',
    separator: false
  },
  {
    icon: 'feedback',
    label: 'Send Feedback',
    separator: false
  },
  {
    icon: 'help',
    iconColor: 'primary',
    label: 'Help',
    separator: false
  }
]
</script>