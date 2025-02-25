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
