<template>
  <q-page class="q-pa-md">
    <q-card class="shadow-2" style="max-width: 500px; margin: auto;">
      <q-card-section>
        <div class="text-h6 text-center">Settings</div>
      </q-card-section>

      <q-separator />

      <q-card-section>
        <q-toggle v-model="constructionMarkings" label="Enable Construction Markings" @update:model-value="saveSetting('constructionMarkings', constructionMarkings)" />
        <q-toggle v-model="sportFacilities" label="Enable Sport Facility Markings" @update:model-value="saveSetting('sportFacilities', sportFacilities)" />
        <q-toggle v-model="highstress" label="Show High-Stress areas" @update:model-value="saveSetting('highstress', highstress)" />
        <q-toggle v-model="mediumstress" label="Show Medium-Stress areas" @update:model-value="saveSetting('mediumstress', mediumstress)" />
        <q-toggle v-model="nostress" label="Show No-Stress areas" @update:model-value="saveSetting('nostress', nostress)" />
        <q-toggle v-model="absnostress" label="Show Absolutely No-Stress areas" @update:model-value="saveSetting('absnostress', absnostress)" />
        <q-toggle v-model="nightMode" label="Enable Dark Mode" @update:model-value="saveSetting('nightMode', nightMode)" />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { ref, onMounted } from "vue";

export default {
  setup() {
    const constructionMarkings = ref(true);
    const sportFacilities = ref(true);
    const highstress = ref(true);
    const mediumstress = ref(true);
    const nostress = ref(true);
    const absnostress = ref(true);
    const nightMode = ref(false);

    // Load saved settings from localStorage
    onMounted(() => {
      constructionMarkings.value = JSON.parse(localStorage.getItem("constructionMarkings")) || false;
      sportFacilities.value = JSON.parse(localStorage.getItem("sportFacilities")) || false;
      highstress.value = JSON.parse(localStorage.getItem("highstress")) || false;
      mediumstress.value = JSON.parse(localStorage.getItem("mediumstress")) || false;
      nostress.value = JSON.parse(localStorage.getItem("nostress")) || false;
      absnostress.value = JSON.parse(localStorage.getItem("absnostress")) || false;
      nightMode.value = JSON.parse(localStorage.getItem("nightMode")) || false;
    });

    const saveSetting = (key, value) => {
      localStorage.setItem(key, JSON.stringify(value));
    };

    return {
      constructionMarkings,
      sportFacilities,
      nightMode,
      highstress,
      mediumstress,
      nostress,
      absnostress,
      saveSetting
    };
  }
};
</script>
