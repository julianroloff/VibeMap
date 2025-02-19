<template>
  <div class="text-primary text-center q-pa-md flex flex-center w-100">
    <div class="text-h6">My ratings</div>

    <q-card v-for="(rating, index) in ratings" :key="index" class="myratings-card">
      <q-card-section class="myratings-card-inner">
        <div class="map-elem" :ref="el => mapElements[index] = el"></div>
        <div class="rate-details">
          <div class="rate-date">{{ rating.date }}</div>
          <div class="rate"><span class="material-icons" :style="{ color: getRatingColor(rating.value) }">{{ getRatingIcon(rating.value) }}</span></div>
          <div class="rate-reason">{{ rating.reason }}</div>
        </div>
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

    const mapElements = ref([]);

    onMounted(() => {
      loadGoogleMaps();
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
        const rating = ratings.value[index]; // Get corresponding rating data

        const map = new window.google.maps.Map(mapElement, {
          center: { lat: rating.lat, lng: rating.long },
          zoom: 14,
          mapTypeControl: false,
          zoomControl: false,
          streetViewControl: false,
          fullscreenControl: false
        });

        new window.google.maps.Marker({
          position: { lat: rating.lat, lng: rating.long },
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

    return {
      ratings,
      mapElements,
      getRatingIcon,
      getRatingColor
    };
  }
};
</script>
