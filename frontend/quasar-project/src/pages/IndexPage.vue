
<template>
  <q-page class="q-pa-none main-page">
    <div class="map-cont p-5 pb-5">
      <div id="map" class="google-map q-card"></div>
      <q-btn 
        class="recenter-btn" 
        color="primary" 
        icon="my_location" 
        @click="recenterMap"
      />
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
import { ref, onMounted, inject } from 'vue'
//import { getModuleURL } from 'workbox-build';


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
        fullscreenControl: false,
        gestureHandling: 'greedy'
      });
      this.loadHeatmap();
      this.trackUserLocation();
    },

    trackUserLocation() {
      let firstUpdate = true;
      navigator.geolocation.watchPosition(
        (position) => {
          const userLocation = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          };

          // Move map to user's location
          if (firstUpdate) {
            this.map.setCenter(userLocation);
            this.map.setZoom(15);
            firstUpdate = false; // Disable further automatic recentering
          }

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
    recenterMap() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const userLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            };
            this.map.setCenter(userLocation);
            this.map.setZoom(15);
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
            }
          },
          () => {
            console.error("Unable to retrieve location.");
          }
        );
      } else {
        console.error("Geolocation is not supported.");
      }
    },

    loadHeatmap() {
      const globalresponse = [inject('response')];
      console.log(globalresponse[0]._rawValue);
      //const response = globalresponse[0]._rawValue;
      const response = localStorage.getItem("response") ? JSON.parse(localStorage.getItem("response")) : [];
      console.log(response);
      const stressLevel1 = [];
      const stressLevel2 = [];
      const stressLevel3 = [];
      const stressLevel4 = [];

      response._rawValue.forEach(item => {
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
      if  (this.highstress){
        heatmap1.setMap(this.map);
      }
      if  (this.mediumstress){
        heatmap2.setMap(this.map);
      }
      if  (this.nostress){
        heatmap3.setMap(this.map);
      }
      if  (this.absnostress){
        heatmap4.setMap(this.map);
      }
    },

    loadDefaultLocation() {
      const defaultLocation = { lat: 52.377956, lng: 	4.897070 }; // Amsterdam fallback
      this.map.setCenter(defaultLocation);
      this.map.setZoom(12);
    },
    submitRating() {
      //console.log("Rating:", this.ratingModel);
      //console.log("Reason:", this.reason);
      //console.log("Location:", this.map.getCenter().toJSON());
      var response = localStorage.getItem("response") ? JSON.parse(localStorage.getItem("response")) : [];
      console.log(response);
      const lastRowId = response._rawValue.length;
      response._rawValue.unshift({
        id: lastRowId+1,
        userId: Number(localStorage.getItem("loggedInId")),
        latitude: this.map.getCenter().lat(),
        longitude: this.map.getCenter().lng(),
        stress_level: this.ratingModel,
        comment: this.reason,
        geom: '{"type":"Point","coordinates":['+ this.map.getCenter().lng() + ',' + this.map.getCenter().lat() +']}'
      });
      response._value.unshift({
        id: lastRowId,
        userId: localStorage.getItem("loggedInId"),
        latitude: this.map.getCenter().lat(),
        longitude: this.map.getCenter().lng(),
        stress_level: this.ratingModel,
        comment: this.reason,
        geom: '{"type":"Point","coordinates":['+ this.map.getCenter().lng() + ',' + this.map.getCenter().lat() +']}'
      });
      localStorage.setItem("response", JSON.stringify(response));
      console.log(response);
      /*const refreshPage = () => {
        location.reload(); // Reloads the current page
      };
      refreshPage();*/
      //this.loadHeatmap();
      this.ratingModel = 0;
      this.reason = "";

    }
  },
  setup () {
    const isLoggedIn = ref(true)
    const constructionMarkings = ref(true);
    const sportFacilities = ref(true);
    const highstress = ref(true);
    const mediumstress = ref(true);
    const nostress = ref(true);
    const absnostress = ref(true);
    const nightMode = ref(false);
    // Check if the user is logged in by reading localStorage
    onMounted(() => {
      isLoggedIn.value = localStorage.getItem("isLoggedIn") === "true";
      //localStorage.setItem("isLoggedIn", "true") 
      //console.log(isLoggedIn.value);
      //console.log(profileEdit.value)
      constructionMarkings.value = JSON.parse(localStorage.getItem("constructionMarkings")) || false;
      sportFacilities.value = JSON.parse(localStorage.getItem("sportFacilities")) || false;
      highstress.value = JSON.parse(localStorage.getItem("highstress")) || false;
      mediumstress.value = JSON.parse(localStorage.getItem("mediumstress")) || false;
      nostress.value = JSON.parse(localStorage.getItem("nostress")) || false;
      absnostress.value = JSON.parse(localStorage.getItem("absnostress")) || false;
      nightMode.value = JSON.parse(localStorage.getItem("nightMode")) || false;
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
      isLoggedIn,
      constructionMarkings,
      sportFacilities,
      nightMode,
      highstress,
      mediumstress,
      nostress,
      absnostress
    }
  }
};
</script>