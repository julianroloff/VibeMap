
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
            unchecked-icon="build_circle"
            indeterminate-icon="construction"
          />
          <q-checkbox v-if="ratingModel === 3 || ratingModel === 4" class="checkbox sport"
            v-model="sport"
            checked-icon="sports_tennis"
            unchecked-icon="sports_tennis"
            indeterminate-icon="sports_tennis"
          />
          <q-checkbox v-if="ratingModel === 3 || ratingModel === 4" class="checkbox nature"
            v-model="nature"
            checked-icon="nature"
            unchecked-icon="nature"
            indeterminate-icon="nature"
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
      this.loadSportFacilities(); // Load sport facilities when the map is initialized
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
            path: "M264.693,326.845h-38.079c-4.418,0-8-3.582-8-8v-30.464H108.231v30.464c0,4.418-3.582,8-8,8H62.152c-4.418,0-8-3.582-8-8  v-6.939H24.074c-4.418,0-8-3.582-8-8V224.03c0-4.418,3.582-8,8-8h30.077v-6.938c0-4.418,3.582-8,8-8h38.079c4.418,0,8,3.582,8,8  v30.464h110.384v-30.464c0-4.418,3.582-8,8-8h38.079c4.418,0,8,3.582,8,8v6.938h30.077c4.418,0,8,3.582,8,8v79.875  c0,4.418-3.582,8-8,8h-30.077v6.939C272.693,323.263,269.112,326.845,264.693,326.845z M234.615,310.845h22.079v-93.753h-22.079  V310.845z M70.152,310.845h22.079v-93.753H70.152V310.845z M272.693,295.905h22.077V232.03h-22.077V295.905z M32.074,295.905h22.077  V232.03H32.074V295.905z M108.231,272.381h110.384v-16.825H108.231V272.381z M145.443,223.376c-1.331,0-2.68-0.332-3.922-1.032  c-3.849-2.17-5.209-7.05-3.04-10.898c14.273-25.312,33.543-46.712,56.214-63.181c-9.894-13.703-21.197-26.173-33.681-37.227  c-31.019,33.403-73.355,55.896-120.395,61.599c1.042,4.209,2.303,8.368,3.784,12.468c1.501,4.155-0.65,8.741-4.806,10.242  c-4.158,1.502-8.741-0.651-10.242-4.807c-5.571-15.424-8.396-31.599-8.396-48.077C20.959,63.908,84.868,0,163.423,0  c78.554,0,142.462,63.908,142.462,142.463c0,14.179-2.104,28.201-6.255,41.68c-1.301,4.223-5.78,6.589-10,5.291  c-4.223-1.3-6.591-5.777-5.291-10c3.68-11.951,5.546-24.39,5.546-36.971c0-4.869-0.276-9.673-0.814-14.4  c-25.871,2.997-50.403,11.521-72.172,24.662c4.713,7.504,9.017,15.253,12.873,23.202c1.928,3.975,0.269,8.761-3.706,10.689  c-3.975,1.925-8.762,0.269-10.689-3.707c-3.573-7.366-7.501-14.486-11.761-21.341c-20.629,15.091-38.175,34.642-51.196,57.736  C150.948,221.911,148.236,223.376,145.443,223.376z M66.601,61.193c-18.492,21.994-29.642,50.354-29.642,81.27  c0,4.834,0.274,9.639,0.819,14.399c43.257-5.019,82.233-25.484,110.873-56.012C124.555,82.391,96.76,68.814,66.601,61.193z   M171.329,98.998c13.625,12.048,25.936,25.664,36.611,40.442c23.598-14.378,50.218-23.758,78.307-27.155  c-9.987-40.635-39.667-73.615-78.299-88.194C201.125,51.937,188.433,77.333,171.329,98.998z M79.321,48.096  c28.682,8.458,55.914,22.357,79.681,40.709c15.771-20.065,27.435-43.606,33.62-69.402C183.248,17.179,173.468,16,163.423,16  C131.162,16,101.686,28.14,79.321,48.096z", // Base shape for the marker
            scale: 1, // Size of the base shape
            fillColor: "#9C27B0", // Purple color for sport facilities
            fillOpacity: 1,
            strokeWeight: 2,
            strokeColor: "#ffffff",
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
      ratingColors: [ 'red', 'orange', 'green', 'green-9'],
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