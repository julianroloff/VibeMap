<template>
  <div class="text-primary text-center q-pa-md flex flex-center w-100" v-if="isLoggedIn">
    <div class="text-h6">My ratings</div>

    <q-card v-for="(response, index) in responses.filter(r => r.userId === loggedInId)" :key="index" class="myratings-card">
      <q-card-section class="myratings-card-inner">
        <div class="map-elem" :ref="el => mapElements[index] = el"></div>
        <div class="rate-details">
          <div class="rate-date"> Rating ID: {{ response.id }}</div>
          <div class="rate"><span class="material-icons" :style="{ color: getRatingColor(response.stress_level) }">{{ getRatingIcon(response.stress_level) }}</span></div>
          <div class="rate-reason">{{ response.comment }}</div>
        </div>
      </q-card-section>
    </q-card>
  </div>
  <div class="text-primary text-center q-pa-md flex flex-center w-100" v-if="!isLoggedIn">
    <q-card>
        <q-card-section>
          <div class="text-h7">Please sign up or log in to be able to rate your location.</div>
          <q-item class="q-gutter-sm w-100">
            <q-btn label="Login" color="primary" class="col-6" to="/profile" />
            <q-btn label="Signup" color="secondary" outline class="col-6" to="./signup" />
          </q-item>
        </q-card-section>
      </q-card>
    <q-btn class="q-mt-xl text-primary" unelevated to="/" label="Go Home" no-caps />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const ratings = ref([
      { date: '19-02-2025', value: 4, reason: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', lat: 52.477956, long: 4.797070 },
      { date: '18-02-2025', value: 2, reason: 'Lot of constructions nearby, can\'t relax.', lat: 52.277956, long: 4.997070 },
      { date: '17-02-2025', value: 1, reason: 'I just hate life.', lat: 52.377956, long: 4.997070 },
      { date: '17-02-2025', value: 3, reason: 'meh.', lat: 52.377956, long: 4.897070 }
    ]);
    const responses = ref([
      { id: 40, userId: 1, latitude: 52.358, longitude: 4.868, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.868,52.358]}' },
      { id: 2, userId: 2, latitude: 52.355, longitude: 4.956, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.956,52.355]}' },
      { id: 15, userId: 2, latitude: 52.369, longitude: 4.846, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.846,52.369]}' },
      { id: 31, userId: 1, latitude: 52.364, longitude: 4.934, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.934,52.364]}' },
      { id: 5, userId: 5, latitude: 52.358, longitude: 4.962, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.962,52.358]}' },
      { id: 22, userId: 4, latitude: 52.358793, longitude: 4.867782, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.867782,52.358793]}' },
      { id: 50, userId: 1, latitude: 52.354709, longitude: 4.855900, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.855900,52.354709]}' },
      { id: 10, userId: 5, latitude: 52.357, longitude: 4.958, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
      { id: 33, userId: 3, latitude: 52.374, longitude: 4.891, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.891,52.374]}' },
      { id: 27, userId: 4, latitude: 52.371, longitude: 4.844, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.844,52.371]}' },
      { id: 45, userId: 1, latitude: 52.359473, longitude: 4.875700, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.875700,52.359473]}' },
      { id: 18, userId: 5, latitude: 52.366, longitude: 4.936, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.936,52.366]}' },
      { id: 7, userId: 2, latitude: 52.354, longitude: 4.952, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.952,52.354]}' },
      { id: 55, userId: 1, latitude: 52.342, longitude: 4.892, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.892,52.342]}' },
      { id: 36, userId: 1, latitude: 52.355379, longitude: 4.856230, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.856230,52.355379]}' },
      { id: 60, userId: 1, latitude: 52.372, longitude: 4.893, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.893,52.372]}' },
      { id: 14, userId: 1, latitude: 52.376, longitude: 4.889, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.889,52.376]}' },
      { id: 49, userId: 5, latitude: 52.355919, longitude: 4.858136, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.858136,52.355919]}' },
      { id: 3, userId: 3, latitude: 52.356, longitude: 4.958, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.958,52.356]}' },
      { id: 58, userId: 4, latitude: 52.365, longitude: 4.850, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.850,52.365]}' },
      { id: 25, userId: 2, latitude: 52.365, longitude: 4.978, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.978,52.365]}' },
      { id: 42, userId: 3, latitude: 52.359758, longitude: 4.873774, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.873774,52.359758]}' },
      { id: 6, userId: 1, latitude: 52.353, longitude: 4.950, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.950,52.353]}' },
      { id: 51, userId: 2, latitude: 52.390, longitude: 4.910, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.910,52.390]}' },
      { id: 29, userId: 1, latitude: 52.368, longitude: 4.938, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.938,52.368]}' },
      { id: 37, userId: 2, latitude: 52.356381, longitude: 4.861177, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.861177,52.356381]}' },
      { id: 64, userId: 5, latitude: 52.357, longitude: 4.958, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
      { id: 12, userId: 2, latitude: 52.362, longitude: 4.972, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.972,52.362]}' },
      { id: 21, userId: 3, latitude: 52.356913, longitude: 4.865376, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.865376,52.356913]}' },
      { id: 48, userId: 4, latitude: 52.355172, longitude: 4.866809, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.866809,52.355172]}' },
      { id: 17, userId: 4, latitude: 52.346, longitude: 4.896, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.896,52.346]}' },
      { id: 54, userId: 5, latitude: 52.362, longitude: 4.932, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.932,52.362]}' },
      { id: 35, userId: 5, latitude: 52.392, longitude: 4.912, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.912,52.392]}' },
      { id: 1, userId: 1, latitude: 52.354, longitude: 4.954, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.954,52.354]}' },
      { id: 43, userId: 4, latitude: 52.359470, longitude: 4.875362, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.875362,52.359470]}' },
      { id: 24, userId: 1, latitude: 52.364, longitude: 4.976, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.976,52.364]}' },
      { id: 59, userId: 5, latitude: 52.370, longitude: 4.895, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.895,52.370]}' },
      { id: 8, userId: 3, latitude: 52.355, longitude: 4.954, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.954,52.355]}' },
      { id: 46, userId: 2, latitude: 52.360603, longitude: 4.876070, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.876070,52.360603]}' },
      { id: 32, userId: 2, latitude: 52.340, longitude: 4.890, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.890,52.340]}' },
      { id: 53, userId: 4, latitude: 52.360, longitude: 4.930, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.930,52.360]}' },
      { id: 19, userId: 1, latitude: 52.394, longitude: 4.914, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.914,52.394]}' },
      { id: 56, userId: 2, latitude: 52.344, longitude: 4.894, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.894,52.344]}' },
      { id: 38, userId: 3, latitude: 52.357528, longitude: 4.863913, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.863913,52.357528]}' },
      { id: 4, userId: 4, latitude: 52.357, longitude: 4.960, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.960,52.357]}' },
      { id: 61, userId: 2, latitude: 52.357, longitude: 4.958, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
      { id: 13, userId: 3, latitude: 52.363, longitude: 4.974, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.974,52.363]}' },
      { id: 52, userId: 3, latitude: 52.398, longitude: 4.918, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.918,52.398]}' },
      { id: 23, userId: 5, latitude: 52.357832, longitude: 4.869069, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.869069,52.357832]}' },
      { id: 34, userId: 4, latitude: 52.367, longitude: 4.848, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.848,52.367]}' },
      { id: 41, userId: 2, latitude: 52.358638, longitude: 4.870776, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.870776,52.358638]}' },
      { id: 16, userId: 3, latitude: 52.369, longitude: 4.846, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.846,52.369]}' },
      { id: 57, userId: 3, latitude: 52.373, longitude: 4.842, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.842,52.373]}' },
      { id: 39, userId: 4, latitude: 52.357528, longitude: 4.863913, stress_level: 3, comment: 'meh.', geom: '{"type":"Point","coordinates":[4.863913,52.357528]}' },
      { id: 62, userId: 3, latitude: 52.357, longitude: 4.958, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
      { id: 9, userId: 4, latitude: 52.356, longitude: 4.956, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.956,52.356]}' },
      { id: 63, userId: 4, latitude: 52.357, longitude: 4.958, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
      { id: 20, userId: 2, latitude: 52.356913, longitude: 4.865376, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.865376,52.356913]}' },
      { id: 65, userId: 1, latitude: 52.361230, longitude: 4.880370, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.880370,52.361230]}' },
      { id: 44, userId: 5, latitude: 52.360223, longitude: 4.871586, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.871586,52.360223]}' },
      { id: 26, userId: 3, latitude: 52.378, longitude: 4.887, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.887,52.378]}' },
      { id: 47, userId: 3, latitude: 52.358533, longitude: 4.874794, stress_level: 4, comment: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', geom: '{"type":"Point","coordinates":[4.874794,52.358533]}' },
      { id: 28, userId: 5, latitude: 52.348, longitude: 4.898, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.898,52.348]}' },
      { id: 30, userId: 2, latitude: 52.396, longitude: 4.916, stress_level: 2, comment: 'Lot of constructions nearby, can\'t relax.', geom: '{"type":"Point","coordinates":[4.916,52.396]}' },
      { id: 11, userId: 1, latitude: 52.361, longitude: 4.970, stress_level: 1, comment: 'I just hate life.', geom: '{"type":"Point","coordinates":[4.970,52.361]}' }
    ]);
    const loggedInId = ref("")
    const mapElements = ref([]);

    onMounted(() => {
      loggedInId.value = Number(localStorage.getItem("loggedInId"));
      setTimeout(() => {
        loadGoogleMaps();
      }, 1);
    });

    function loadGoogleMaps() {
      if (window.google && window.google.maps) {
        initMaps();
        return;
      }

      const script = document.createElement("script");
      script.src = `https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY`;
      script.async = true;
      script.defer = true;
      script.onload = initMaps;
      document.head.appendChild(script);
    }

    function initMaps() {
      mapElements.value.forEach((mapElement, index) => {
        const response = responses.value[index]; // Get corresponding rating data

        const map = new window.google.maps.Map(mapElement, {
          center: { lat: response.latitude, lng: response.longitude },
          zoom: 14,
          mapTypeControl: false,
          zoomControl: false,
          streetViewControl: false,
          fullscreenControl: false
        });

        new window.google.maps.Marker({
          position: { lat: response.latitude, lng: response.longitude },
          map: map,
          icon: {
                path: window.google.maps.SymbolPath.CIRCLE,
                scale: 7, // Size of the dot
                fillColor: "#2C6E49",
                fillOpacity: 1,
                strokeWeight: 2,
                strokeColor: "#ffffff",
              },
        });
      });
    }
    // Function to return the corresponding icon for the rating value
    function getRatingIcon(value) {
      const icons = [
        'sentiment_very_dissatisfied',
        'sentiment_dissatisfied',
        'sentiment_satisfied',
        'sentiment_very_satisfied'
      ];
      return icons[value - 1] || ''; // Default to an empty string if value is out of range
    }
    // Function to return the corresponding color for the rating value
    function getRatingColor(value) {
      const colors = [
        'red',       // for 'sentiment_very_dissatisfied'
        'orange',    // for 'sentiment_dissatisfied'
        'green',     // for 'sentiment_satisfied'
        'green-9'    // for 'sentiment_very_satisfied'
      ];
      return colors[value - 1] || ''; // Default to an empty string if value is out of range
    }

    const isLoggedIn = ref(true)
    
    // Check if the user is logged in by reading localStorage
    onMounted(() => {
      isLoggedIn.value = localStorage.getItem("isLoggedIn") === "true";
      //localStorage.setItem("isLoggedIn", "true") 
      //console.log(isLoggedIn.value);
      //console.log(profileEdit.value)
    });

    return {
      ratings,
      responses,
      mapElements,
      getRatingIcon,
      getRatingColor,
      isLoggedIn,
      loggedInId
    };
  }
};
</script>
