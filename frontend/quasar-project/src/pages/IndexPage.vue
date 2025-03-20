
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
          <q-item-label v-if="ratingModel" class="reason-label">Reason</q-item-label>
          <q-checkbox v-if="ratingModel === 1 || ratingModel === 2" class="checkbox noise"
            v-model="noise"
            checked-icon="campaign"
            unchecked-icon="volume_down_alt"
            indeterminate-icon="sound_detection_loud_sound"
          />
          <q-checkbox v-if="ratingModel === 1 || ratingModel === 2" class="checkbox crowd"
            v-model="crowd"
            checked-icon="groups"
            unchecked-icon="group_off"
            indeterminate-icon="groups_2"
          />
          <q-checkbox v-if="ratingModel === 1 || ratingModel === 2" class="checkbox construction"
            v-model="construction"
            checked-icon="construction"
            unchecked-icon="engineering"
            indeterminate-icon="construction"
          />
          <q-checkbox v-if="ratingModel === 3 || ratingModel === 4" class="checkbox sport"
            v-model="sport"
            checked-icon="sports_handball"
            unchecked-icon="sports_tennis"
            indeterminate-icon="sports_tennis"
          />
          <q-checkbox v-if="ratingModel === 3 || ratingModel === 4" class="checkbox nature"
            v-model="nature"
            checked-icon="forest"
            unchecked-icon="park"
            indeterminate-icon="landscape"
          />
          <q-input v-if="ratingModel"
            v-model="reason"
            label="Comment"
            placeholder="Why did you give this rating?"
            type="textarea"
            rows="1"
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
        <div class="text-h5 font-atkinson-bold">Welcome to VibeMap</div>
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
        <div class="text-h5 font-atkinson-bold">Understanding Urban Stress</div>
        <div class="text-body1">
          <p>City life is full of contrasts. For some, the hum of construction or crowded streets can be overwhelming, while for others, a touch of nature or active leisure can provide much-needed relief.</p>
          <p>We want to understand how these factors affect you personally – so that VibeMap can better guide you to the environments that match your unique needs.</p>
          <p>VibeMap is a project by the students of the University of Amsterdam. It is a part of the Social Complexity and Designing with Data course, which aims to promote and increase urban mental health.</p>
        </div>
        <div class="btn-cnt">
          <q-btn label="Previous" color="secondary" @click="previousCard" class="radius-10 left-btn" />
          <q-btn label="Next" color="primary" @click="nextCard" class="radius-10 right-btn" />
        </div>
      </q-card>
      <q-card v-if="currentCard === 3">
        <div class="text-h5 font-atkinson-bold">Preferences</div>
        <div class="text-body1">
          <p>You can select what you would like to see on your map. You can modify these later in the Settings page.</p>
        </div>
        <div class="pref-cont">
          <q-toggle v-model="constructionMarkings" label="Enable Construction Markings" @update:model-value="saveSetting('constructionMarkings', constructionMarkings)" />
          <q-toggle v-model="sportFacilities" label="Enable Sport Facility Markings" @update:model-value="saveSetting('sportFacilities', sportFacilities)" />
          <q-toggle v-model="colorswitch" label="Enable Color Switch for accessibility" @update:model-value="saveSetting('colorswitch', colorswitch)" />
          <q-toggle v-model="highstress" label="Show High-Stress areas" @update:model-value="saveSetting('highstress', highstress)" />
          <q-toggle v-model="mediumstress" label="Show Medium-Stress areas" @update:model-value="saveSetting('mediumstress', mediumstress)" />
          <q-toggle v-model="nostress" label="Show No-Stress areas" @update:model-value="saveSetting('nostress', nostress)" />
          <q-toggle v-model="absnostress" label="Show Absolutely No-Stress areas" @update:model-value="saveSetting('absnostress', absnostress)" />
        </div>
        <div class="btn-cnt">
          <q-btn label="Previous" color="secondary" @click="previousCard" class="radius-10 left-btn" />
          <q-btn label="Next" color="primary" @click="nextCard" class="radius-10 right-btn" />
        </div>
      </q-card>
      <!--q-card v-if="currentCard === 4">
        <div class="text-h5 font-atkinson-bold">About You!</div>
        <div class="text-body1">
          <p>Please rate the personal impact of the following factors on you.</p>
        </div>
        <div class="btn-cnt">
          <q-btn label="Previous" color="secondary" @click="previousCard" class="radius-10 left-btn" />
          <q-btn label="Next" color="primary" @click="nextCard" class="radius-10 right-btn" />
        </div>
      </q-card-->
      <q-card v-if="currentCard === 4">
        <div class="text-h5 font-atkinson-bold">How VibeMap Works</div>
        <div class="text-body1">
          <p>1. Rate your current location by selecting a smiley that best represents your stress level.</p>
          <p>2. Add a comment to share your thoughts on the location. Optionally, select the cause of your rating using the available options.</p>
          <p>3. Use the map to find relaxing spots and avoid stress in your city.</p>
          <p>Every rating and comment builds a detailed, crowdsourced map to help everyone navigate toward a more relaxed city.</p>
        </div>
        <div class="btn-cnt">
          <q-btn label="Previous" color="secondary" @click="previousCard" class="radius-10 left-btn" />
          <q-btn label="Next" color="primary" @click="nextCard" class="radius-10 right-btn" />
        </div>
      </q-card>
      <q-card v-if="currentCard === 5">
        <div class="text-h5 font-atkinson-bold">Contact us</div>
        <div class="text-body1">
          <p>For questions or feedback, please contact us at using the <q-btn to="/feedback" label="Feedback" flat color="primary"/> page.</p>
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
          <q-btn label="Get started!" color="primary" @click="closeCards" class="radius-10 right-btn" />
        </div>
      </q-card>
    </div>
  </q-page>
</template>

<script>
//import { latLng } from 'leaflet';
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
      sportFacilitiesMarkers: [], // Array to store sport facilities markers
    };
  },
  mounted() {
    this.loadGoogleMaps();
  },
  methods: {
    async loadGoogleMaps() {
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
      if (this.currentCard < 6) {
        this.currentCard++;
      }
    },
    previousCard() {
      if (this.currentCard < 7) {
        this.currentCard--;
      }
    },
    closeCards() {
      this.currentCard = 1;
      this.showIntro = false;
    },

    async initMap() {
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
      await this.trackUserLocation();
      //if (this.constructionMarkings) {
      //  this.loadConstructionMarkings();
      //}
      if (this.sportFacilities) {
        await this.loadSportFacilities(); // Load sport facilities when the map is initialized
      }
      if (this.colorswitch) {
        await this.loadAccessibleHeatmap();
      }
      if (!this.colorswitch || this.colorswitch == null)
      await this.loadHeatmap();
    },
    
    async loadSportFacilities() {
      try {
        const response = await fetch("https://vibemapbe.com/external/external/sport");
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const sportFacilitiesData = await response.json();
        this.addSportFacilitiesMarkers(sportFacilitiesData.sport_parks);
      } catch (error) {
        console.error('Error fetching sport facilities data:', error);
      }
    },

    addSportFacilitiesMarkers(sportFacilities) {
      sportFacilities.forEach(facility => {
        const marker = new window.google.maps.Marker({
          position: { lat: facility.latitude, lng: facility.longitude },
          map: this.map,
          icon: {
            path: "M 25.914062 32 L 22.1875 32 C 21.753906 32 21.402344 31.648438 21.402344 31.214844 L 21.402344 28.234375 L 10.597656 28.234375 L 10.597656 31.214844 C 10.597656 31.648438 10.246094 32 9.8125 32 L 6.085938 32 C 5.652344 32 5.300781 31.648438 5.300781 31.214844 L 5.300781 30.539062 L 2.355469 30.539062 C 1.925781 30.539062 1.574219 30.1875 1.574219 29.753906 L 1.574219 21.933594 C 1.574219 21.5 1.925781 21.152344 2.355469 21.152344 L 5.300781 21.152344 L 5.300781 20.472656 C 5.300781 20.039062 5.652344 19.6875 6.085938 19.6875 L 9.8125 19.6875 C 10.246094 19.6875 10.597656 20.039062 10.597656 20.472656 L 10.597656 23.453125 L 21.402344 23.453125 L 21.402344 20.472656 C 21.402344 20.039062 21.753906 19.6875 22.1875 19.6875 L 25.914062 19.6875 C 26.347656 19.6875 26.699219 20.039062 26.699219 20.472656 L 26.699219 21.152344 L 29.644531 21.152344 C 30.074219 21.152344 30.425781 21.5 30.425781 21.933594 L 30.425781 29.753906 C 30.425781 30.1875 30.074219 30.539062 29.644531 30.539062 L 26.699219 30.539062 L 26.699219 31.214844 C 26.699219 31.648438 26.347656 32 25.914062 32 Z M 22.96875 30.433594 L 25.132812 30.433594 L 25.132812 21.253906 L 22.96875 21.253906 Z M 6.867188 30.433594 L 9.03125 30.433594 L 9.03125 21.253906 L 6.867188 21.253906 Z M 26.699219 28.972656 L 28.859375 28.972656 L 28.859375 22.71875 L 26.699219 22.71875 Z M 3.140625 28.972656 L 5.300781 28.972656 L 5.300781 22.71875 L 3.140625 22.71875 Z M 10.597656 26.667969 L 21.402344 26.667969 L 21.402344 25.019531 L 10.597656 25.019531 Z M 14.238281 21.871094 C 14.109375 21.871094 13.976562 21.835938 13.855469 21.769531 C 13.480469 21.554688 13.347656 21.078125 13.558594 20.703125 C 14.957031 18.222656 16.84375 16.128906 19.0625 14.515625 C 18.09375 13.175781 16.988281 11.953125 15.765625 10.871094 C 12.726562 14.140625 8.582031 16.34375 3.976562 16.902344 C 4.078125 17.3125 4.203125 17.722656 4.347656 18.121094 C 4.496094 18.53125 4.285156 18.980469 3.875 19.125 C 3.46875 19.273438 3.019531 19.0625 2.875 18.65625 C 2.328125 17.144531 2.050781 15.5625 2.050781 13.949219 C 2.050781 6.257812 8.308594 0 16 0 C 23.691406 0 29.949219 6.257812 29.949219 13.949219 C 29.949219 15.335938 29.742188 16.707031 29.335938 18.027344 C 29.207031 18.441406 28.769531 18.671875 28.355469 18.546875 C 27.941406 18.417969 27.710938 17.980469 27.839844 17.566406 C 28.199219 16.398438 28.382812 15.179688 28.382812 13.949219 C 28.382812 13.472656 28.355469 13 28.300781 12.539062 C 25.769531 12.832031 23.367188 13.667969 21.234375 14.953125 C 21.695312 15.6875 22.117188 16.445312 22.496094 17.222656 C 22.683594 17.613281 22.523438 18.082031 22.132812 18.269531 C 21.742188 18.460938 21.273438 18.296875 21.085938 17.90625 C 20.738281 17.1875 20.351562 16.488281 19.933594 15.820312 C 17.914062 17.296875 16.199219 19.210938 14.921875 21.472656 C 14.777344 21.726562 14.511719 21.871094 14.238281 21.871094 Z M 6.519531 5.992188 C 4.710938 8.144531 3.617188 10.921875 3.617188 13.949219 C 3.617188 14.421875 3.644531 14.890625 3.699219 15.359375 C 7.933594 14.867188 11.75 12.863281 14.554688 9.875 C 12.195312 8.066406 9.472656 6.738281 6.519531 5.992188 Z M 16.773438 9.691406 C 18.109375 10.871094 19.3125 12.207031 20.359375 13.652344 C 22.667969 12.246094 25.273438 11.324219 28.023438 10.992188 C 27.046875 7.015625 24.140625 3.785156 20.359375 2.359375 C 19.691406 5.085938 18.449219 7.570312 16.773438 9.691406 Z M 7.765625 4.707031 C 10.574219 5.535156 13.242188 6.898438 15.566406 8.695312 C 17.109375 6.730469 18.253906 4.425781 18.859375 1.898438 C 17.941406 1.683594 16.984375 1.566406 16 1.566406 C 12.839844 1.566406 9.957031 2.753906 7.765625 4.707031 Z M 7.765625 4.707031 ", // Base shape for the marker
            scale: 1, // Size of the base shape
            fillColor: "#9C27B0", // Purple color for sport facilities
            fillOpacity: 1,
            strokeWeight: 1,
            strokeColor: "#9C27B0",
          },
          title: facility.name, // Tooltip with the facility name
        });
        this.sportFacilitiesMarkers.push(marker);
      });
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
      var response = localStorage.getItem("response");

      try {
        // Fetch data from the API
        response = await fetch("https://vibemapbe.com/location/location/locations/");
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const apiData = await response.json(); // Parse the JSON response
        if (apiData || apiData.length) {
          response = apiData;
        }
        localStorage.setItem("response", JSON.stringify(response));
        console.log(response);
      }
      catch (error) {
        console.error('Error fetching data:', error);
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
    async loadAccessibleHeatmap() {
      var response = localStorage.getItem("response");

      try {
        // Fetch data from the API
        response = await fetch("https://vibemapbe.com/location/location/locations/");
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const apiData = await response.json(); // Parse the JSON response
        if (apiData || apiData.length) {
          response = apiData;
        }
        localStorage.setItem("response", JSON.stringify(response));
        console.log(response);
      }
      catch (error) {
        console.error('Error fetching data:', error);
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
          'rgba(255, 0, 0, 0)', 
          'rgba(255, 0, 0, 0.8)',   
        ]
      });
      var heatmap2 = new window.google.maps.visualization.HeatmapLayer({
        data: stressLevel2,
        //dissipating: false,
        radius: 50, // Adjust this value to make the heat points bigger or smaller
        gradient: [
          'rgba(248, 157, 9, 0)', 
          'rgba(248, 157, 9, 0.8)', 
        ]
      });
      var heatmap3 = new window.google.maps.visualization.HeatmapLayer({
        data: stressLevel3,
        //dissipating: false,
        radius: 50, // Adjust this value to make the heat points bigger or smaller
        gradient: [
          'rgba(29, 107, 223, 0)',
          'rgba(29, 107, 223, 0.8)', 
        ]
      });
      var heatmap4 = new window.google.maps.visualization.HeatmapLayer({
        data: stressLevel4,
        //dissipating: false,
        radius: 50, // Adjust this value to make the heat points bigger or smaller
        gradient: [
          'rgba(23, 179, 83, 0)', 
          'rgba(23, 179, 83, 0.8)' 
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

    getMarkerLatLng(userMarker) {
      if (!userMarker || !userMarker.getPosition) {
        throw new Error("Invalid marker object provided.");
      }
      const position = userMarker.getPosition(); // Get the LatLng object
      return {
        lat: position.lat(), // Get latitude
        lng: position.lng(), // Get longitude
      };
    },
    
    async submitRating() {
      
      if (!this.userMarker) {
        console.error("User marker is not available.");
        return;
      }

      // Prepare the data for the POST request
      const token = localStorage.getItem("usertoken");
      
      const latLng = this.getMarkerLatLng(this.userMarker);
        console.log("Latitude:", latLng.lat);
        console.log("Longitude:", latLng.lng);

      console.log(latLng);

      const ratingData = {
        latitude: latLng.lat, // Use the map's center latitude
        longitude: latLng.lng, // Use the map's center longitude
        comment: this.reason ? this.reason : null, // Use the reason entered by the user
        stress_level: this.ratingModel, // Use the selected rating
        construction: this.construction,
        noise: this.noise,
        crowd: this.crowd,
        sport: this.sport,
        nature: this.nature,
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
    const isLoggedIn = ref()
    const constructionMarkings = ref();
    const sportFacilities = ref();
    const colorswitch = ref();
    const highstress = ref();
    const mediumstress = ref();
    const nostress = ref();
    const absnostress = ref();
    const nightMode = ref();
    // Check if the user is logged in by reading localStorage
    onMounted(() => {
      isLoggedIn.value = localStorage.getItem("isLoggedIn") === "true";
      //localStorage.setItem("isLoggedIn", "true") 
      //console.log(isLoggedIn.value);
      //console.log(profileEdit.value)
      constructionMarkings.value = JSON.parse(localStorage.getItem("constructionMarkings"));
      sportFacilities.value = JSON.parse(localStorage.getItem("sportFacilities"));
      colorswitch.value = JSON.parse(localStorage.getItem("colorswitch"));
      highstress.value = JSON.parse(localStorage.getItem("highstress"));
      mediumstress.value = JSON.parse(localStorage.getItem("mediumstress"));
      nostress.value = JSON.parse(localStorage.getItem("nostress"));
      absnostress.value = JSON.parse(localStorage.getItem("absnostress"));
      nightMode.value = JSON.parse(localStorage.getItem("nightMode"));
    })
    const saveSetting = (key, value) => {
      localStorage.setItem(key, JSON.stringify(value));
    };
    return {
      ratingModel: ref(0),
      ratingColors: JSON.parse(localStorage.getItem("colorswitch")) 
        ? ['red-7', 'amber-7', 'blue-7', 'green-7']  // Colors when colorswitch is true
        : ['red', 'orange', 'green', 'green-9'], // Default colors when colorswitch is false
      icons: [
        'sentiment_very_dissatisfied',
        'sentiment_dissatisfied',
        'sentiment_satisfied',
        'sentiment_very_satisfied'
      ],
      noise: ref(false),
      crowd: ref(false),
      construction: ref(false),
      nature: ref(false),
      sport: ref(false),
      isLoggedIn,
      constructionMarkings,
      sportFacilities,
      colorswitch,
      nightMode,
      highstress,
      mediumstress,
      nostress,
      absnostress,
      saveSetting
    }
  }
};
</script>