<template>
  <div class="text-primary text-center q-pa-md flex flex-center w-100" v-if="isLoggedIn">
    <div class="text-h6">Ratings</div>
    
    <!-- Filter Controls -->
    <div class="filter-controls q-mb-md">
      <q-select
        v-model="ratingFilter"
        :options="ratingOptions"
        label="Filter by Rating"
        dense
        outlined
        class="q-mr-sm col-6"
        style="min-width: 150px"
      />
      <q-toggle
        v-model="showOnlyMyRatings"
        label="Show only my ratings"
        class="q-mr-sm col-6"
      />
      <q-item-label class="slider-label col-12">Max distance: {{distanceFilter}} km</q-item-label>
      <q-slider
        v-model.number="distanceFilter"
        :min="0"
        :max="50"
        label="Max Distance (km)"
        dense
        outlined
        class="q-mr-sm"
        style="min-width: 150px"
      />
      <!--q-input
        v-model="currentLocation.lat"
        label="Latitude"
        dense
        outlined
        class="q-mr-sm"
        style="min-width: 150px"
      />
      <q-input 
        v-model="currentLocation.lng"
        label="Longitude"
        dense
        outlined
        class="q-mr-sm"
        style="min-width: 150px"
      /-->
    </div>
    
    <div class="rate-card-cont">
      <q-card v-for="(response, index) in filteredResponses" :key="index" class="myratings-card">
        <q-card-section class="myratings-card-inner">
          <div class="map-elem" :ref="el => mapElements[index] = el"></div>
          <div class="rate-details">
            <!--div class="rate-date">Rating ID: {{ response.id }}</div-->
            <div class="rate">
              <span class="material-icons" :style="{ color: getRatingColor(response.stress_level) }">
                {{ getRatingIcon(response.stress_level) }}
              </span>
              <!--({{ response.stress_level }})-->
            </div>
            <div class="rate-reason">{{ response.comment }}</div>
            <div v-if="distanceFilter > 0" class="distance">
              Distance: {{ calculateDistance(currentLocation.lat, currentLocation.lng, response.latitude, response.longitude).toFixed(2) }} km
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>
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
import { ref, onMounted, computed } from 'vue';

export default {
  setup() {
    const ratings = ref([]);
    const responses = ref([]);
    const loggedInId = ref("");
    const mapElements = ref([]);
    const userInfo = ref([
      { username: "User", userId: loggedInId.value, email: "email@email.com", picture: "data:image/png;base64,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", token: "password"}
    ]);
    const error = ref(null);
    const usertoken = ref("");
    
    // Filter variables
    const ratingFilter = ref(null);
    const distanceFilter = ref(50);
    const showOnlyMyRatings = ref(false);
    const currentLocation = ref({
      lat: 52.377956,
      lng: 4.897070
    });
    
    const ratingOptions = [
      { label: "All Ratings", value: null },
      { label: "Very Dissatisfied", value: 1 },
      { label: "Dissatisfied", value: 2 },
      { label: "Satisfied", value: 3 },
      { label: "Very Satisfied", value: 4 }
    ];
    
    // Computed property for filtered responses
    const filteredResponses = computed(() => {
      return responses.value.filter(response => {
        // Filter by rating if selected
        if (ratingFilter.value !== null && response.stress_level !== ratingFilter.value.value) {
          return false;
        }
        
        // Filter by distance if enabled
        if (distanceFilter.value > 0 && currentLocation.value.lat && currentLocation.value.lng) {
          const distance = calculateDistance(
            currentLocation.value.lat,
            currentLocation.value.lng,
            response.latitude,
            response.longitude
          );
          return distance <= distanceFilter.value;
        }

        // Filter by user ID if toggle is enabled
        if (showOnlyMyRatings.value && Number(response.userId) !== Number(loggedInId.value)) {
          console.log(response.userId, loggedInId.value);
          return false;
        }
        console.log(response.userId, loggedInId.value);
        
        return true;
      });
    });
    
    // Function to calculate distance between two coordinates in km
    function calculateDistance(lat1, lon1, lat2, lon2) {
      const R = 6371; // Radius of the earth in km
      const dLat = deg2rad(lat2 - lat1);
      const dLon = deg2rad(lon2 - lon1);
      const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);
      const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
      return R * c; // Distance in km
    }
    
    function deg2rad(deg) {
      return deg * (Math.PI / 180);
    }
    
    const fetchRatingdata = async () => {
      try {
        // Fetch data from the API
        var response = await fetch("https://vibemapbe.com/location/location/locations/");
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const apiData = await response.json(); // Parse the JSON response
        const processedData = apiData.map(item => ({
          userId: item.userId,
          id: item.id,
          stress_level: Math.round(item.stress_level),
          comment: item.comment,
          latitude: Number(item.latitude),
          longitude: Number(item.longitude),
        }));
        responses.value = processedData;
        console.log(responses.value);
      }
      catch (error) {
        console.error('Error fetching data:', error);
      }
    }
    
    onMounted(async () => {
      usertoken.value = localStorage.getItem("usertoken");
      loggedInId.value = Number(localStorage.getItem("loggedInId"));
      await fetchUserData(usertoken.value);
      await fetchRatingdata();
      
      // Try to get current location if available
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            currentLocation.value = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };
          },
          (error) => {
            console.error("Error getting current location:", error);
          }
        );
      }
      
      setTimeout(() => {
        loadGoogleMaps();
      }, 1);
    });

    const fetchUserData = async (token) => {
      console.log(token)
      try {
        const userDataResponse = await fetch('https://vibemapbe.com/auth/auth/me', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!userDataResponse.ok) {
          throw new Error(`HTTP error! Status: ${userDataResponse.status}`);
        }

        const data = await userDataResponse.json();
        userInfo.value[0] = {
          ...userInfo.value[0], // Keep existing fields
          username: data.email, // Update username from API
          email: data.email, // Update email from API
          userId: data.id, // Update userId from API
          token: token, // Update token from API
        };
      } catch (err) {
        error.value = err.message || 'Failed to fetch user data';
      }
    };

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
        const response = filteredResponses.value[index]; // Get corresponding rating data

        const map = new window.google.maps.Map(mapElement, {
          center: { lat: response.latitude, lng: response.longitude },
          zoom: 14,
          mapTypeControl: false,
          zoomControl: false,
          cameraControl: false,
          scaleControl: false,
          streetViewControl: false,
          rotateControl: false,
          fullscreenControl: false,
          gestureHandling: 'greedy'
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

    function getRatingIcon(value) {
      const icons = [
        'sentiment_very_dissatisfied',
        'sentiment_dissatisfied',
        'sentiment_satisfied',
        'sentiment_very_satisfied'
      ];
      return icons[value - 1] || '';
    }

    function getRatingColor(value) {
      const colors = [
        'red',       // for 'sentiment_very_dissatisfied'
        'orange',    // for 'sentiment_dissatisfied'
        'green',     // for 'sentiment_satisfied'
        'green-9'    // for 'sentiment_very_satisfied'
      ];
      return colors[value - 1] || '';
    }

    const isLoggedIn = ref();
    
    onMounted(() => {
      isLoggedIn.value = localStorage.getItem("isLoggedIn");
    });

    return {
      ratings,
      responses,
      filteredResponses,
      mapElements,
      getRatingIcon,
      getRatingColor,
      isLoggedIn,
      loggedInId,
      ratingFilter,
      distanceFilter,
      currentLocation,
      ratingOptions,
      calculateDistance,
      showOnlyMyRatings
    };
  }
};
</script>
