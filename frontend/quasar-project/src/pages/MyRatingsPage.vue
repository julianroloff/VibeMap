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
import { ref, onMounted, inject } from 'vue';

export default {
  setup() {
    const ratings = ref([
      { date: '19-02-2025', value: 4, reason: 'Very calm neighbourhood, not a lot of people, no constructions nearby.', lat: 52.477956, long: 4.797070 },
      { date: '18-02-2025', value: 2, reason: 'Lot of constructions nearby, can\'t relax.', lat: 52.277956, long: 4.997070 },
      { date: '17-02-2025', value: 1, reason: 'I just hate life.', lat: 52.377956, long: 4.997070 },
      { date: '17-02-2025', value: 3, reason: 'meh.', lat: 52.377956, long: 4.897070 }
    ]);
    const globalresponse = [inject('response')];
    console.log(globalresponse[0]._rawValue);
    //const responses = globalresponse[0]._rawValue;
    const response = localStorage.getItem("response") ? JSON.parse(localStorage.getItem("response")) : [];
    const responses = response._rawValue;
    console.log(responses); 
    const loggedInId = ref("")
    const mapElements = ref([]);
    const userInfo = ref([
        { username: "User", userId: 1, email: "email@email.com", picture: "data:image/png;base64,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", token: "password"}
      ]);
    const error = ref(null);
    const usertoken = ref("")

    onMounted(() => {
      loggedInId.value = Number(localStorage.getItem("loggedInId"));
      setTimeout(() => {
        loadGoogleMaps();
      }, 1);
      usertoken.value = localStorage.getItem("usertoken");
      fetchUserData(usertoken.value);
    });

    const fetchUserData = async (token) => {
      console.log(token)
      try {
        const response = await fetch('https://vibemapbe.com/auth/auth/me', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        userInfo.value[0] = {
          ...userInfo.value[0], // Keep existing fields
          username: data.email, // Update username from API
          email: data.email, // Update email from API
          userId: data.id, // Update userId from API
          token: token, // Update token from API
        };
        console.log(userInfo.value[0]);
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
        const response = responses[index]; // Get corresponding rating data

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
