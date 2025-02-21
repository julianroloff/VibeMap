<template>
  <q-page class="flex flex-center">
    <q-card class="q-pa-md shadow-2" style="max-width: 400px; width: 100%">
      <q-card-section>
        <div class="text-h6 text-center">Feedback Form</div>
      </q-card-section>

      <q-card-section>
        <q-input v-model="name" label="Your Name" outlined dense />
        <q-input v-model="email" label="Your Email" type="email" outlined dense class="q-mt-md" />
        
        <div class="q-mt-md">
          <span class="text-subtitle1">Rate Us:</span>
          <q-rating v-model="rating" size="2em" :max="5" color="yellow" class="q-mb-sm" />
        </div>

        <q-input v-model="feedback" label="Your Feedback" outlined dense type="textarea" class="q-mt-md" />

        <q-btn label="Submit" color="primary" class="full-width q-mt-md" @click="submitFeedback" />
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { ref } from "vue";

export default {
  setup() {
    const name = ref("");
    const email = ref("");
    const rating = ref(0);
    const feedback = ref("");

    const submitFeedback = () => {
      if (!name.value || !email.value || !feedback.value) {
        alert("Please fill in all fields!");
        return;
      }

      console.log("Feedback submitted:", {
        name: name.value,
        email: email.value,
        rating: rating.value,
        feedback: feedback.value,
      });

      alert("Thank you for your feedback! 😊");
      
      // Clear form
      name.value = "";
      email.value = "";
      rating.value = 0;
      feedback.value = "";
    };

    return { name, email, rating, feedback, submitFeedback };
  }
};
</script>
