<template>
  <div class="questions-container">
    <h1 v-if="question.id !== 100 && !submittedAnswer" class="question-text">{{ question.text }}</h1>

    <!-- Table for Question 4 -->
    <img v-if="question.id === 4 && !submittedAnswer" src="./table.jpg" alt="Physical Activity Intensity Levels by METs" class="question-image" />

    <!-- Different Question Types -->
    <div v-if="question.id !== 100 && !submittedAnswer && question.type === 'multiple_choice'">
      <div v-for="option in question.options" :key="option" class="option">
        <input type="checkbox" :value="option" v-model="selectedOptions" />
        <label class="option-text">{{ option }}</label>
      </div>
    </div>
    <div v-if="question.id !== 100 && !submittedAnswer && question.type === 'single_choice'">
      <div v-for="option in question.options" :key="option" class="option">
        <input type="radio" :value="option" v-model="selectedOption" />
        <label class="option-text">{{ option }}</label>
      </div>
    </div>
    <div v-if="question.id !== 100 && !submittedAnswer && question.type === 'text' && question.id === 25">
      <div>
        <label class="label-large">Height: </label>
        <input type="text" v-model="heightFeet" placeholder="Feet" class="bmi-input" /> feet
        <input type="text" v-model="heightInches" placeholder="Inches" class="bmi-input" /> inches
      </div>
      <div>
        <label class="label-large">Weight: </label>
        <input type="text" v-model="weightLbs" placeholder="Pounds" class="bmi-input" /> lbs
      </div>
      <div>
        <p class="label-large">BMI: {{ calculatedBMI }}</p>
      </div>
    </div>
    <div v-if="question.id !== 100 && !submittedAnswer && question.type === 'text' && question.id !== 25">
      <input type="text" v-model="textResponse" placeholder="Enter your answer here" class="text-input" />
    </div>
    <div v-if="question.id !== 100 && !submittedAnswer && question.type === 'VAS'">
      <input type="range" min="1" max="10" v-model="VASToScore" />
      <label class="option-text">{{ VASToScore }}</label>
    </div>

    <!-- End Page -->
    <p v-if="question.id === 100" class="message">Thanks for your participation! </p>
    
    <!-- Show Message -->
    <p v-if="submittedAnswer && question.id !== 100" class="message">{{ message }}</p>

    <!-- Next Button -->
    <div class="button-group" v-if="question.id !== 100">
      <button @click="goBack">Back</button>
      <button v-if="!submittedAnswer" @click="submitAnswer">Submit</button>
      <button v-if="submittedAnswer" @click="goNext">Next</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      question: {},
      selectedOptions: [],
      VASToScore: 5,
      textResponse: '', 
      message: '',
      nextQuestionId: 0,
      submittedAnswer: false,
      heightFeet: '',
      heightInches: '',
      weightLbs: '',
      selectedOption: ''
    };
  },
  computed: {
  calculatedBMI() {
    const heightInchesTotal = (parseFloat(this.heightFeet) * 12) + parseFloat(this.heightInches);
    const weight = parseFloat(this.weightLbs);
    if (heightInchesTotal && weight) {
      return ((weight / (heightInchesTotal * heightInchesTotal)) * 703).toFixed(2);
    }
    return '';
  }
  },
  methods: {
    async fetchQuestion(id) {
      try {
        const response = await fetch(`http://localhost:8000/get-question/${id}`);
        if (!response.ok) {
          throw new Error("Failed to fetch question");
        }
        const questionData = await response.json();
        this.question = questionData;
        this.selectedOptions = [];
        this.selectedOption = '';
        this.VASToScore = 5;
        this.textResponse = '';
        this.message = '';
        this.submittedAnswer = false;
      } catch (error) {
        console.error(error);
        this.message = "Error fetching question";
      }
    },
    goBack() {
      this.$emit('changePage', 'welcome');
    },
    async submitAnswer() {
      try {
        let response;
        if (this.question.id === 25) {
        if (!this.heightFeet || !this.heightInches || !this.weightLbs) {
          this.message = "Please fill in height and weight.";
          return;
        }
        response = await fetch('http://localhost:8000/submit-answer/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            question_id: this.question.id,
            response: [`${this.heightFeet} ft`, `${this.heightInches} in`, `${this.weightLbs} lbs`]
          })
        });
        }else if (this.question.type === 'multiple_choice') {
          response = await fetch('http://localhost:8000/submit-answer/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question_id: this.question.id, response: this.selectedOptions})
          });
        } else if (this.question.type === 'single_choice') {
          response = await fetch('http://localhost:8000/submit-answer/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question_id: this.question.id, response: [this.selectedOption] })
          });
        } else if (this.question.type === 'VAS') {
          response = await fetch('http://localhost:8000/submit-answer/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question_id: this.question.id, response: [this.VASToScore] })
          });
        } else if (this.question.type === 'text') {
          if (!this.textResponse.trim()) {
            this.message = "Please enter a response.";
            return;
          }
          response = await fetch('http://localhost:8000/submit-answer/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ question_id: this.question.id, response: [this.textResponse] })
          });
        }

        if (!response.ok) {
          throw new Error("Failed to submit answer");
        }

        const data = await response.json();
        if (data.message && data.next_question_id !== undefined) {
          this.message = data.message;
          this.nextQuestionId = data.next_question_id;
          this.submittedAnswer = true;
        } else {
          throw new Error("Received unexpected data");
        }
      } catch (error) {
        console.error(error);
        this.message = "Error submitting answer. Please try again.";
      }
    },
    goNext() {
      if (!this.message) {
        this.message = "Please submit the answer";
      } else {
        this.fetchQuestion(this.nextQuestionId);
      }
    }
  },
  mounted() {
    this.fetchQuestion(1);  
  }
};
</script>
<style scoped>
.questions-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 92vh;
  background-color: #f0f2f5;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}
.label-large {
  font-size: 18px; 
  font-weight: bold; 
}
.question-text {
  margin-bottom: 38px;
  color: #333;
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  max-width: 1000px;
}
.question-image {
  max-width: 60%; /* Ensures the image doesn't overflow the container */
  margin: 20px 0; /* Adds some space above and below the image */
}
.options-group, .bmi-group, .vas-group {
  margin-bottom: 20px;
  width: 100%;
  max-width: 600px;
}

.option {
  margin: 5px 0;
  display: flex;
  align-items: center;
}

.option-text {
  font-size: 25px;
  margin-left: 12px;
  margin-top: 3px;
}

.input[type="checkbox"], input[type="radio"] {
  transform: scale(1.2);
}

.vas-slider {
  width: 100%;
}

.message {
  margin-top: 24px;
  font-size: 32px;
  font-weight: bold;
  color: #333;
  text-align: center;
  max-width: 1000px;
  background-color: #e9ecef;
  padding: 10px;
  border-radius: 8px;
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 15px; /* Space between buttons */
  margin-top: 40px; /* Margin above the buttons */
}

.bmi-input {
  width: 20%; /* Make the input box take full width within its container */
  max-width: 600px; /* Maximum width for larger screens */
  height: 40px; /* Height of the input box */
  margin: 5px 0;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

.text-input {
  width: 100%; /* Make the input box take full width within its container */
  max-width: 1000px; /* Maximum width for larger screens */
  height: 40px; /* Height of the input box */
  margin: 5px 0;
  padding: 5px;
  font-size: 18px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

button {
  padding: 12px 24px;
  font-size: 18px;
  font-weight: bold;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

button:active {
  background-color: #004494;
  transform: translateY(0);
}


</style>


