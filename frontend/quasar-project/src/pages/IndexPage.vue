
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
    <div class="intro-cont p-5 pt-5 bg-primary" v-if="!isLoggedIn && showIntro">
      <q-card v-if="currentCard === 1">
        <div class="text-h4 font-atkinson-bold">Welcome to VibeMap</div>
        <div class="text-body1">
          <p>Find your calm in the urban jungle. VibeMap is a community‐driven guide that shows you where to find relaxing spots and avoid stress in your city.</p>
          <p>By rating places on a 1–4 scale using smileys and sharing feedback on ambiance, noise, and environment – along with your personal comments – you help build a living map that reflects the true vibe of your urban surroundings.</p>
          <p>Your input helps everyone navigate towards more relaxing experiences.</p>
        </div>
        <div class="btn-cnt">
          <q-btn label="Skip" color="secondary" @click="closeCards" class="radius-10 left-btn" />
          <q-btn label="Next" color="primary" @click="nextCard" class="radius-10 right-btn" />
        </div>
      </q-card>
      <q-card v-if="currentCard === 2">
        <div class="text-h4 font-atkinson-bold">How to use VibeMap</div>
        <div class="text-body1">
          <p>1. Rate your current location by selecting a smiley that best represents your stress level.</p>
          <p>2. Add a comment to share your thoughts on the location.</p>
          <p>3. Your rating will be added to the map and shared with the community.</p>
          <p>4. Use the map to find relaxing spots and avoid stress in your city.</p>
        </div>
        <div class="btn-cnt">
          <q-btn label="Previous" color="secondary" @click="previousCard" class="radius-10 left-btn" />
          <q-btn label="Next" color="primary" @click="nextCard" class="radius-10 right-btn" />
        </div>
      </q-card>
      <q-card v-if="currentCard === 3">
        <div class="text-h4 font-atkinson-bold">Get started</div>
        <div class="text-body1">
          <p>Sign up or log in to start rating your location and help others find their calm.</p>
        </div>
        <div>
          <q-item class="q-gutter-sm w-100">
            <q-btn label="Login" color="primary" class="col-6" to="/profile" />
            <q-btn label="Signup" color="secondary" outline class="col-6" to="./signup" />
          </q-item>
        </div>
        <div class="btn-cnt">
          <q-btn label="Previous" color="secondary" @click="previousCard" class="radius-10 left-btn" />
          <q-btn label="Next" color="primary" @click="nextCard" class="radius-10 right-btn" />
        </div>
      </q-card>
      <q-card v-if="currentCard === 4">
        <div class="text-h4 font-atkinson-bold">About VibeMap</div>
        <div class="text-body1">
          <p>VibeMap is a project by the students of the University of Amsterdam. It is a part of the Social Complexity and Designing with Data course, which aims to promote and increase urban mental health.</p>
        </div>
        <div class="btn-cnt">
          <q-btn label="Previous" color="secondary" @click="previousCard" class="radius-10 left-btn" />
          <q-btn label="Next" color="primary" @click="nextCard" class="radius-10 right-btn" />
        </div>
      </q-card>
      <q-card v-if="currentCard === 5">
        <div class="text-h4 font-atkinson-bold">Contact us</div>
        <div class="text-body1">
          <p>For questions or feedback, please contact us at <a href="mailto:agoston.reischl@student.uva.nl">agoston.reischl@student.uva.nl</a>.</p>
        </div>
        <div class="btn-cnt">
          <q-btn label="Previous" color="secondary" @click="previousCard" class="radius-10 left-btn" />
          <q-btn label="Close" color="primary" @click="closeCards" class="radius-10 right-btn" />
        </div>
      </q-card>
    </div>
  </q-page>
</template>

<script>
import { ref, onMounted } from 'vue'
//import { inject } from 'vue'
//import { getModuleURL } from 'workbox-build';


export default {
  data() {
    return {
      map: null,
      userMarker: null,
      currentCard: 1,
      showIntro: true,
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
    nextCard() {
      if (this.currentCard < 5) {
        this.currentCard++;
      }
    },
    previousCard() {
      if (this.currentCard < 6) {
        this.currentCard--;
      }
    },
    closeCards() {
      this.currentCard = 1;
      this.showIntro = false;
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

    async loadHeatmap() {
      //const globalresponse = [inject('response')];
      //console.log(globalresponse[0]._rawValue);
      //const response = globalresponse[0]._rawValue;
      var response = [];

      try {
        // Fetch data from the API
        response = await fetch("https://vibemapbe.com/location/location/locations/");
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const apiData = await response.json(); // Parse the JSON response
        response = apiData;
        console.log(response);
      }
      catch (error) {
        console.error('Error fetching data:', error);
        //response = localStorage.getItem("response") ? JSON.parse(localStorage.getItem("response")) : [];
      }

      console.log(response);
      const stressLevel1 = [];
      const stressLevel2 = [];
      const stressLevel3 = [];
      const stressLevel4 = [];

      response.forEach(item => {
        const data ={ 
          location: new window.google.maps.LatLng(item.latitude, item.longitude), 
          weight: item.stress_level 
        };
        
        // Categorize data based on stress level ranges
        if (item.stress_level >= 0.5 && item.stress_level < 1.5) {
          stressLevel1.push(data);
        } else if (item.stress_level >= 1.5 && item.stress_level < 2.5) {
          stressLevel2.push(data);
        } else if (item.stress_level >= 2.5 && item.stress_level < 3.5) {
          stressLevel3.push(data);
        } else if (item.stress_level >= 3.5 && item.stress_level <= 4.5) {
          stressLevel4.push(data);
        } else {
          console.error("Invalid stress level:", item.stress_level);
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
    async submitRating() {
      //console.log("Rating:", this.ratingModel);
      //console.log("Reason:", this.reason);
      //console.log("Location:", this.map.getCenter().toJSON());
      //var response = localStorage.getItem("response") ? JSON.parse(localStorage.getItem("response")) : [];
      //console.log(response);
      //const lastRowId = response._rawValue.length;
      //response._rawValue.unshift({
      //  id: lastRowId+1,
      //  userId: Number(localStorage.getItem("loggedInId")),
      //  latitude: this.map.getCenter().lat(),
      //  longitude: this.map.getCenter().lng(),
      //  stress_level: this.ratingModel,
      //  comment: this.reason,
      //  geom: '{"type":"Point","coordinates":['+ this.map.getCenter().lng() + ',' + this.map.getCenter().lat() +']}'
      //});
      //response._value.unshift({
      //  id: lastRowId,
      //  userId: localStorage.getItem("loggedInId"),
      //  latitude: this.map.getCenter().lat(),
      //  longitude: this.map.getCenter().lng(),
      //  stress_level: this.ratingModel,
      //  comment: this.reason,
      //  geom: '{"type":"Point","coordinates":['+ this.map.getCenter().lng() + ',' + this.map.getCenter().lat() +']}'
      //});
      //localStorage.setItem("response", JSON.stringify(response));
      //console.log(response);
      /*const refreshPage = () => {
        location.reload(); // Reloads the current page
      };
      refreshPage();*/
      //this.loadHeatmap();
      // Prepare the data for the POST request
      const token = localStorage.getItem("usertoken");
      /*if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            const userLocation = {
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            };
            this.map.setCenter(userLocation);
          }
        );
      }*/

      const ratingData = {
        latitude: this.map.getCenter().lat(), // Use the map's center latitude
        longitude: this.map.getCenter().lng(), // Use the map's center longitude
        comment: this.reason, // Use the reason entered by the user
        stress_level: this.ratingModel, // Use the selected rating
      };
      try {
        // Send the POST request to the API
        const response = await fetch("https://vibemapbe.com/location/location/locations/", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify(ratingData),
        });

        // Check if the request was successful
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // Parse the response
        const data = await response.json();
        console.log("Review submitted successfully:", data);

        // Optionally, update the local storage or reload the heatmap
        this.loadHeatmap(); // Reload the heatmap to reflect the new review
      } catch (error) {
        console.error("Error submitting review:", error);
        alert("Failed to submit review. Please try again.");
      } finally {
        // Reset the form
        this.ratingModel = 0;
        this.reason = "";
      }
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
      constructionMarkings.value = JSON.parse(localStorage.getItem("constructionMarkings")) || true;
      sportFacilities.value = JSON.parse(localStorage.getItem("sportFacilities")) || true;
      highstress.value = JSON.parse(localStorage.getItem("highstress")) || true;
      mediumstress.value = JSON.parse(localStorage.getItem("mediumstress")) || true;
      nostress.value = JSON.parse(localStorage.getItem("nostress")) || true;
      absnostress.value = JSON.parse(localStorage.getItem("absnostress")) || true;
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