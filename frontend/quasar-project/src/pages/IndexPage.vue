
<template>
  <q-page class="q-pa-none main-page">
    <div class="map-cont p-5 pb-5">
      <div id="map" class="google-map q-card"></div>
      <!--div id="recenter-btn" @click="trackUserLocation()">Recenter</div-->
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
      var heatMapData1 = [
        { location: new window.google.maps.LatLng(52.354, 4.954), weight: 1 },
        { location: new window.google.maps.LatLng(52.355, 4.956), weight: 1 },
        { location: new window.google.maps.LatLng(52.356, 4.958), weight: 1 },
        { location: new window.google.maps.LatLng(52.357, 4.960), weight: 1 },
        { location: new window.google.maps.LatLng(52.358, 4.962), weight: 1 },
        { location: new window.google.maps.LatLng(52.353, 4.950), weight: 1 },
        { location: new window.google.maps.LatLng(52.354, 4.952), weight: 1 },
        { location: new window.google.maps.LatLng(52.355, 4.954), weight: 1 },
        { location: new window.google.maps.LatLng(52.356, 4.956), weight: 1 },
        { location: new window.google.maps.LatLng(52.357, 4.958), weight: 1 },
        { location: new window.google.maps.LatLng(52.361, 4.970), weight: 1 },
        { location: new window.google.maps.LatLng(52.362, 4.972), weight: 1 },
        { location: new window.google.maps.LatLng(52.363, 4.974), weight: 1 },
      ];
      var heatMapData2 = [
        { location: new window.google.maps.LatLng(52.376, 4.889), weight: 2 },
        { location: new window.google.maps.LatLng(52.369, 4.846), weight: 2 },
        { location: new window.google.maps.LatLng(52.369, 4.846), weight: 2 },
        { location: new window.google.maps.LatLng(52.346, 4.896), weight: 2 },
        { location: new window.google.maps.LatLng(52.366, 4.936), weight: 2 },
        { location: new window.google.maps.LatLng(52.394, 4.914), weight: 2 },
        { location: new window.google.maps.LatLng(52.356913, 4.865376), weight: 2 },
        { location: new window.google.maps.LatLng(52.356913, 4.865376), weight: 2 },
        { location: new window.google.maps.LatLng(52.358793, 4.867782), weight: 2 },
        { location: new window.google.maps.LatLng(52.357832, 4.869069), weight: 2 },
        { location: new window.google.maps.LatLng(52.364, 4.976), weight: 2 },
        { location: new window.google.maps.LatLng(52.365, 4.978), weight: 2 },
        { location: new window.google.maps.LatLng(52.378, 4.887), weight: 2 },
        { location: new window.google.maps.LatLng(52.371, 4.844), weight: 2 },
        { location: new window.google.maps.LatLng(52.348, 4.898), weight: 2 },
        { location: new window.google.maps.LatLng(52.368, 4.938), weight: 2 },
        { location: new window.google.maps.LatLng(52.396, 4.916), weight: 2 },
      ];
      var heatMapData3 = [
        { location: new window.google.maps.LatLng(52.364, 4.934), weight: 3 },
        { location: new window.google.maps.LatLng(52.340, 4.890), weight: 3 },
        { location: new window.google.maps.LatLng(52.374, 4.891), weight: 3 },
        { location: new window.google.maps.LatLng(52.367, 4.848), weight: 3 },
        { location: new window.google.maps.LatLng(52.392, 4.912), weight: 3 },
        { location: new window.google.maps.LatLng(52.355379, 4.856230), weight: 3 },
        { location: new window.google.maps.LatLng(52.356381, 4.861177), weight: 3 },
        { location: new window.google.maps.LatLng(52.357528, 4.863913), weight: 3 },
        { location: new window.google.maps.LatLng(52.357528, 4.863913), weight: 3 },
      ];
      var heatMapData4 =[
        { location: new window.google.maps.LatLng(52.358, 4.868), weight: 4 }, // High weight
        { location: new window.google.maps.LatLng(52.358638, 4.870776), weight: 4 },
        { location: new window.google.maps.LatLng(52.359758, 4.873774), weight: 4 },
        { location: new window.google.maps.LatLng(52.359470, 4.875362), weight: 4 },
        { location: new window.google.maps.LatLng(52.360223, 4.871586), weight: 4 },
        { location: new window.google.maps.LatLng(52.359473, 4.875700), weight: 4 },
        { location: new window.google.maps.LatLng(52.360603, 4.876070), weight: 4 },
        { location: new window.google.maps.LatLng(52.358533, 4.874794), weight: 4 },
        { location: new window.google.maps.LatLng(52.355172, 4.866809), weight: 4 },
        { location: new window.google.maps.LatLng(52.355919, 4.858136), weight: 4 },
        { location: new window.google.maps.LatLng(52.354709, 4.855900), weight: 4 },
        { location: new window.google.maps.LatLng(52.390, 4.910), weight: 4 },
        { location: new window.google.maps.LatLng(52.398, 4.918), weight: 4 },
        { location: new window.google.maps.LatLng(52.360, 4.930), weight: 4 },
        { location: new window.google.maps.LatLng(52.362, 4.932), weight: 4 },
        { location: new window.google.maps.LatLng(52.342, 4.892), weight: 4 },
        { location: new window.google.maps.LatLng(52.344, 4.894), weight: 4 },
        { location: new window.google.maps.LatLng(52.373, 4.842), weight: 4 },
        { location: new window.google.maps.LatLng(52.365, 4.850), weight: 4 },
        { location: new window.google.maps.LatLng(52.370, 4.895), weight: 4 },
        { location: new window.google.maps.LatLng(52.372, 4.893), weight: 4 },
        { location: new window.google.maps.LatLng(52.357, 4.958), weight: 4 },
        { location: new window.google.maps.LatLng(52.357, 4.958), weight: 4 },
        { location: new window.google.maps.LatLng(52.357, 4.958), weight: 4 },
        { location: new window.google.maps.LatLng(52.357, 4.958), weight: 4 },
        { location: new window.google.maps.LatLng(52.361230, 4.880370), weight: 4 }

      ];

      var heatmap1 = new window.google.maps.visualization.HeatmapLayer({
        data: heatMapData1,
        //dissipating: false,
        radius: 50, // Adjust this value to make the heat points bigger or smaller
        gradient: [
          'rgba(255, 0, 0, 0)', // Transparent for no rating
          'rgba(255, 0, 0, 0.8)',   // Red for low weight (rating 1)
        ]
      });
      var heatmap2 = new window.google.maps.visualization.HeatmapLayer({
        data: heatMapData2,
        //dissipating: false,
        radius: 50, // Adjust this value to make the heat points bigger or smaller
        gradient: [
          'rgba(255, 100, 0, 0)', // Transparent for no rating
          'rgba(255, 100, 0, 0.8)', // Orange for weight 2
        ]
      });
      var heatmap3 = new window.google.maps.visualization.HeatmapLayer({
        data: heatMapData3,
        //dissipating: false,
        radius: 50, // Adjust this value to make the heat points bigger or smaller
        gradient: [
          'rgba(100, 255, 0, 0)', // Transparent for no rating
          'rgba(100, 255, 0, 0.8)', // Light green for weight 3
        ]
      });
      var heatmap4 = new window.google.maps.visualization.HeatmapLayer({
        data: heatMapData4,
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