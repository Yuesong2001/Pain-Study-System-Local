<template>
  <div class="welcome-container">
    <div v-if="!hasSubmitted" class="input-row">
      <input v-model="username" placeholder="Enter your username" />
      <button @click="submitUsername">Submit</button>
    </div>
    <h2 v-if="hasSubmitted" class="welcome-message">{{ message }}</h2>
    <div v-if="hasSubmitted" class="start-button-row">
      <button @click="$emit('changePage', 'questions')">Start the test</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      message: '',
      showStartButton: false,
      hasSubmitted: false
    };
  },
  methods: {
    async submitUsername() {
      try {
        const response = await fetch('http://localhost:8000/welcome/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: this.username })
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        this.message = data.message;
        this.showStartButton = true;
        this.hasSubmitted = true;

        localStorage.setItem("username", this.username);
      } catch (error) {
        console.error('Error:', error);
        this.message = 'There was an error processing your request.';
        this.showStartButton = false;
      }
    }
  }
};

</script>

<style scoped>
.welcome-container {
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

.input-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

input {
  padding: 8px;
  height: 40px;
  width: 200px;
  font-size: 18px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

button {
  margin-left: 10px;
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

.welcome-message {
  margin-top: 40px;
  color: #333;
  font-size: 32px;
  font-weight: bold;
  text-align: center;
  max-width: 1000px;
  background-color: #e9ecef;
  padding: 10px;
  border-radius: 8px;
}

.start-button-row {
  display: flex;
  justify-content: center;
  width: 100%;
  margin-top: 20px;
}
</style>