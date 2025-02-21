
<template>
  <q-page class="q-pa-none main-page">
    <div class="map-cont p-5 pb-5">
      <div id="map" class="google-map q-card"></div>
      <!--div id="recenter-btn" @click="trackUserLocation()">Recenter</div-->
    </div>
    <div class="loadbtn">
      <q-btn label="Load Heat Data" color="primary" @click="loadHeatData" class="radius-10" />
    </div>
    <div class="rate-cont p-5 pt-5">
      <q-card class="rate-card" v-if="isLoggedIn">
        <q-card-section>
          <div class="text-h6">Rate your location</div>
          <q-rating class="rating-icons"
            v-model="ratingModel"
            :max="4"
            color="grey"
            :color-selected="ratingColors"
            :icon="icons"
          />
          <q-input v-if="ratingModel"
            v-model="reason"
            label="Reason"
            placeholder="Why did you give this rating?"
            type="textarea"
            rows="3"
            optional
          />
        </q-card-section>
        <q-card-actions align="right" v-if="ratingModel">
          <q-btn label="Submit" color="primary" @click="submitRating" class="radius-10" />
        </q-card-actions>
      </q-card>
      <q-card v-if="!isLoggedIn">
        <q-card-section>
          <div class="text-h7">Please sign up or log in to be able to rate your location.</div>
          <q-item class="q-gutter-sm w-100">
            <q-btn label="Login" color="primary" class="col-6" to="/profile" />
            <q-btn label="Signup" color="secondary" outline class="col-6" to="./signup" />
          </q-item>
        </q-card-section>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted } from 'vue'


export default {
  data() {
    return {
      map: null,
      userMarker: null,
    };
  },
  mounted() {
    this.loadGoogleMaps();
  },
  methods: {
    loadGoogleMaps() {
      if (window.google && window.google.maps) {
        this.initMap();
        return;
      }

      const script = document.createElement("script");
      script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyCa6szZqcobw9AEf8KiqXUDpAoLgSR6v7A`;
      script.async = true;
      script.defer = true;
      script.onload  = () => this.initMap();
      document.head.appendChild(script);
    },

    initMap() {
      if (!navigator.geolocation) {
        console.error("Geolocation is not supported by this browser.");
        return this.loadDefaultLocation();
      }

      this.map = new window.google.maps.Map(document.getElementById("map"), {
        center: { lat: 52.377956, lng: 	4.897070 }, // Default (Amsterdam)
        zoom: 12,
        mapTypeControl: false,
        zoomControl: false,
        cameraControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        fullscreenControl: false
      });
      this.loadHeatmap();
      this.trackUserLocation();
    },

    trackUserLocation() {
      navigator.geolocation.watchPosition(
        (position) => {
          const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };

          // Move map to user's location
          this.map.setCenter(userLocation);
          this.map.setZoom(15);

          // If first time, create native location marker
          if (!this.userMarker) {
            this.userMarker = new window.google.maps.Marker({
              position: userLocation,
              map: this.map,
              icon: {
                path: window.google.maps.SymbolPath.CIRCLE,
                scale: 8, // Size of the dot
                fillColor: "#4285F4",
                fillOpacity: 1,
                strokeWeight: 2,
                strokeColor: "#ffffff",
              },
            });
          } else {
            // Update position dynamically
            this.userMarker.setPosition(userLocation);
          }
        },
        () => {
          console.error("User denied Geolocation.");
          this.loadDefaultLocation();
        },
        {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 0,
        }
      );
    },

    loadHeatmap() {
      const response = [
        // Data from heatMapData1 (stress_level: 1)
        { id: 1, userId: 1, latitude: 52.354, longitude: 4.954, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.954,52.354]}' },
        { id: 2, userId: 1, latitude: 52.355, longitude: 4.956, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.956,52.355]}' },
        { id: 3, userId: 1, latitude: 52.356, longitude: 4.958, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.958,52.356]}' },
        { id: 4, userId: 1, latitude: 52.357, longitude: 4.960, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.960,52.357]}' },
        { id: 5, userId: 1, latitude: 52.358, longitude: 4.962, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.962,52.358]}' },
        { id: 6, userId: 1, latitude: 52.353, longitude: 4.950, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.950,52.353]}' },
        { id: 7, userId: 1, latitude: 52.354, longitude: 4.952, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.952,52.354]}' },
        { id: 8, userId: 1, latitude: 52.355, longitude: 4.954, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.954,52.355]}' },
        { id: 9, userId: 1, latitude: 52.356, longitude: 4.956, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.956,52.356]}' },
        { id: 10, userId: 1, latitude: 52.357, longitude: 4.958, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
        { id: 11, userId: 1, latitude: 52.361, longitude: 4.970, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.970,52.361]}' },
        { id: 12, userId: 1, latitude: 52.362, longitude: 4.972, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.972,52.362]}' },
        { id: 13, userId: 1, latitude: 52.363, longitude: 4.974, stress_level: 1, comment: null, geom: '{"type":"Point","coordinates":[4.974,52.363]}' },

        // Data from heatMapData2 (stress_level: 2)
        { id: 14, userId: 1, latitude: 52.376, longitude: 4.889, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.889,52.376]}' },
        { id: 15, userId: 1, latitude: 52.369, longitude: 4.846, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.846,52.369]}' },
        { id: 16, userId: 1, latitude: 52.369, longitude: 4.846, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.846,52.369]}' },
        { id: 17, userId: 1, latitude: 52.346, longitude: 4.896, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.896,52.346]}' },
        { id: 18, userId: 1, latitude: 52.366, longitude: 4.936, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.936,52.366]}' },
        { id: 19, userId: 1, latitude: 52.394, longitude: 4.914, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.914,52.394]}' },
        { id: 20, userId: 1, latitude: 52.356913, longitude: 4.865376, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.865376,52.356913]}' },
        { id: 21, userId: 1, latitude: 52.356913, longitude: 4.865376, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.865376,52.356913]}' },
        { id: 22, userId: 1, latitude: 52.358793, longitude: 4.867782, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.867782,52.358793]}' },
        { id: 23, userId: 1, latitude: 52.357832, longitude: 4.869069, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.869069,52.357832]}' },
        { id: 24, userId: 1, latitude: 52.364, longitude: 4.976, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.976,52.364]}' },
        { id: 25, userId: 1, latitude: 52.365, longitude: 4.978, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.978,52.365]}' },
        { id: 26, userId: 1, latitude: 52.378, longitude: 4.887, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.887,52.378]}' },
        { id: 27, userId: 1, latitude: 52.371, longitude: 4.844, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.844,52.371]}' },
        { id: 28, userId: 1, latitude: 52.348, longitude: 4.898, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.898,52.348]}' },
        { id: 29, userId: 1, latitude: 52.368, longitude: 4.938, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.938,52.368]}' },
        { id: 30, userId: 1, latitude: 52.396, longitude: 4.916, stress_level: 2, comment: null, geom: '{"type":"Point","coordinates":[4.916,52.396]}' },

        // Data from heatMapData3 (stress_level: 3)
        { id: 31, userId: 1, latitude: 52.364, longitude: 4.934, stress_level: 3, comment: null, geom: '{"type":"Point","coordinates":[4.934,52.364]}' },
        { id: 32, userId: 1, latitude: 52.340, longitude: 4.890, stress_level: 3, comment: null, geom: '{"type":"Point","coordinates":[4.890,52.340]}' },
        { id: 33, userId: 1, latitude: 52.374, longitude: 4.891, stress_level: 3, comment: null, geom: '{"type":"Point","coordinates":[4.891,52.374]}' },
        { id: 34, userId: 1, latitude: 52.367, longitude: 4.848, stress_level: 3, comment: null, geom: '{"type":"Point","coordinates":[4.848,52.367]}' },
        { id: 35, userId: 1, latitude: 52.392, longitude: 4.912, stress_level: 3, comment: null, geom: '{"type":"Point","coordinates":[4.912,52.392]}' },
        { id: 36, userId: 1, latitude: 52.355379, longitude: 4.856230, stress_level: 3, comment: null, geom: '{"type":"Point","coordinates":[4.856230,52.355379]}' },
        { id: 37, userId: 1, latitude: 52.356381, longitude: 4.861177, stress_level: 3, comment: null, geom: '{"type":"Point","coordinates":[4.861177,52.356381]}' },
        { id: 38, userId: 1, latitude: 52.357528, longitude: 4.863913, stress_level: 3, comment: null, geom: '{"type":"Point","coordinates":[4.863913,52.357528]}' },
        { id: 39, userId: 1, latitude: 52.357528, longitude: 4.863913, stress_level: 3, comment: null, geom: '{"type":"Point","coordinates":[4.863913,52.357528]}' },

        // Data from heatMapData4 (stress_level: 4)
        { id: 40, userId: 1, latitude: 52.358, longitude: 4.868, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.868,52.358]}' },
        { id: 41, userId: 1, latitude: 52.358638, longitude: 4.870776, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.870776,52.358638]}' },
        { id: 42, userId: 1, latitude: 52.359758, longitude: 4.873774, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.873774,52.359758]}' },
        { id: 43, userId: 1, latitude: 52.359470, longitude: 4.875362, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.875362,52.359470]}' },
        { id: 44, userId: 1, latitude: 52.360223, longitude: 4.871586, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.871586,52.360223]}' },
        { id: 45, userId: 1, latitude: 52.359473, longitude: 4.875700, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.875700,52.359473]}' },
        { id: 46, userId: 1, latitude: 52.360603, longitude: 4.876070, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.876070,52.360603]}' },
        { id: 47, userId: 1, latitude: 52.358533, longitude: 4.874794, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.874794,52.358533]}' },
        { id: 48, userId: 1, latitude: 52.355172, longitude: 4.866809, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.866809,52.355172]}' },
        { id: 49, userId: 1, latitude: 52.355919, longitude: 4.858136, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.858136,52.355919]}' },
        { id: 50, userId: 1, latitude: 52.354709, longitude: 4.855900, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.855900,52.354709]}' },
        { id: 51, userId: 1, latitude: 52.390, longitude: 4.910, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.910,52.390]}' },
        { id: 52, userId: 1, latitude: 52.398, longitude: 4.918, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.918,52.398]}' },
        { id: 53, userId: 1, latitude: 52.360, longitude: 4.930, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.930,52.360]}' },
        { id: 54, userId: 1, latitude: 52.362, longitude: 4.932, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.932,52.362]}' },
        { id: 55, userId: 1, latitude: 52.342, longitude: 4.892, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.892,52.342]}' },
        { id: 56, userId: 1, latitude: 52.344, longitude: 4.894, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.894,52.344]}' },
        { id: 57, userId: 1, latitude: 52.373, longitude: 4.842, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.842,52.373]}' },
        { id: 58, userId: 1, latitude: 52.365, longitude: 4.850, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.850,52.365]}' },
        { id: 59, userId: 1, latitude: 52.370, longitude: 4.895, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.895,52.370]}' },
        { id: 60, userId: 1, latitude: 52.372, longitude: 4.893, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.893,52.372]}' },
        { id: 61, userId: 1, latitude: 52.357, longitude: 4.958, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
        { id: 62, userId: 1, latitude: 52.357, longitude: 4.958, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
        { id: 63, userId: 1, latitude: 52.357, longitude: 4.958, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
        { id: 64, userId: 1, latitude: 52.357, longitude: 4.958, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.958,52.357]}' },
        { id: 65, userId: 1, latitude: 52.361230, longitude: 4.880370, stress_level: 4, comment: null, geom: '{"type":"Point","coordinates":[4.880370,52.361230]}' }
      ];
      const stressLevel1 = [];
      const stressLevel2 = [];
      const stressLevel3 = [];
      const stressLevel4 = [];

      response.forEach(item => {
        const data ={ 
          location: new window.google.maps.LatLng(item.latitude, item.longitude), 
          weight: item.stress_level 
        };
        
        switch (item.stress_level) {
          case 1:
            stressLevel1.push(data);
            break;
          case 2:
            stressLevel2.push(data);
            break;
          case 3:
            stressLevel3.push(data);
            break;
          case 4:
            stressLevel4.push(data);
            break;
        }
      });

      var heatmap1 = new window.google.maps.visualization.HeatmapLayer({
        data: stressLevel1,
        //dissipating: false,
        radius: 50, // Adjust this value to make the heat points bigger or smaller
        gradient: [
          'rgba(255, 0, 0, 0)', // Transparent for no rating
          'rgba(255, 0, 0, 0.8)',   // Red for low weight (rating 1)
        ]
      });
      var heatmap2 = new window.google.maps.visualization.HeatmapLayer({
        data: stressLevel2,
        //dissipating: false,
        radius: 50, // Adjust this value to make the heat points bigger or smaller
        gradient: [
          'rgba(255, 100, 0, 0)', // Transparent for no rating
          'rgba(255, 100, 0, 0.8)', // Orange for weight 2
        ]
      });
      var heatmap3 = new window.google.maps.visualization.HeatmapLayer({
        data: stressLevel3,
        //dissipating: false,
        radius: 50, // Adjust this value to make the heat points bigger or smaller
        gradient: [
          'rgba(100, 255, 0, 0)', // Transparent for no rating
          'rgba(100, 255, 0, 0.8)', // Light green for weight 3
        ]
      });
      var heatmap4 = new window.google.maps.visualization.HeatmapLayer({
        data: stressLevel4,
        //dissipating: false,
        radius: 50, // Adjust this value to make the heat points bigger or smaller
        gradient: [
          'rgba(0, 255, 0, 0)', // Transparent for no rating
          'rgba(0, 255, 0, 0.8)'     // Green for high weight (rating 4)
        ]
      });
      heatmap1.setMap(this.map);
      heatmap2.setMap(this.map);
      heatmap3.setMap(this.map);
      heatmap4.setMap(this.map);
    },

    loadDefaultLocation() {
      const defaultLocation = { lat: 52.377956, lng: 	4.897070 }; // Amsterdam fallback
      this.map.setCenter(defaultLocation);
      this.map.setZoom(12);
    },
    submitRating() {
      console.log("Rating:", this.ratingModel);
      console.log("Reason:", this.reason);
    }
  },
  setup () {
    const isLoggedIn = ref(true)
    // Check if the user is logged in by reading localStorage
    onMounted(() => {
      isLoggedIn.value = localStorage.getItem("isLoggedIn") === "true";
      //localStorage.setItem("isLoggedIn", "true") 
      //console.log(isLoggedIn.value);
      //console.log(profileEdit.value)
    })
    return {
      ratingModel: ref(0),
      ratingColors: [ 'red', 'orange', 'green', 'green-9'],
      icons: [
        'sentiment_very_dissatisfied',
        'sentiment_dissatisfied',
        'sentiment_satisfied',
        'sentiment_very_satisfied'
      ],
      isLoggedIn
    }
  }
};
</script>