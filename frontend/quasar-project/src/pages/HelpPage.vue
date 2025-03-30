<template>
  <div class=" text-primary text-center q-pa-md flex flex-center">
    <div>
      <div>
        Help page
      </div>

      <div class="intro-cont p-5 pt-5 bg-primary">
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
            <q-btn label="Get started!" color="primary" @click="goHome" to="/" class="radius-10 right-btn" />
          </div>
        </q-card>
      </div>
      <q-btn
        class="q-mt-xl text-primary"
        unelevated
        to="/"
        label="Go Home"
        no-caps
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'


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
  },
  methods: {
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
    goHome() {
      localStorage.setItem("showIntro", "false");
    },
  },
  setup () {
    const isLoggedIn = ref()
    const personalOn = ref()
    const loggedInId = ref("")
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
      personalOn.value = localStorage.getItem("PersonalOn") === "true";
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
      loggedInId.value = localStorage.getItem("loggedInId");
    })
    const saveSetting = (key, value) => {
      localStorage.setItem(key, JSON.stringify(value));
    };
    return {
      isLoggedIn,
      constructionMarkings,
      sportFacilities,
      colorswitch,
      nightMode,
      highstress,
      mediumstress,
      nostress,
      absnostress,
      loggedInId,
      saveSetting
    }
  }
};
</script>
