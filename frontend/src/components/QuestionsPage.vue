<template>
  <div class="avatar-layout">
    <!-- 过渡动画：切换题目时做左右滑动 -->
    <transition name="slide" mode="out-in">
      <!-- 这里的 :key="question.id" 用于触发过渡动画 -->
      <div :key="question.id" class="content-wrap">
        <!-- 左侧：气泡区域 -->
        <div class="speech-bubble">
          <!-- 问题标题（排除结束页: ID=100 & 已提交） -->
          <h1 v-if="question.id !== 100 && question.id!==4 && !submittedAnswer" class="question-text">
            {{ question.text }}
          </h1>

          <!--  Question4 : replace the figure with Duke Activity Status Index  -->
          <div
            v-if="question.id === 4 && !submittedAnswer"
            class="dasi-question"
          >
            <h2>Duke Activity Status Index</h2>
            <div class="dasi-container">
              <div v-for="(activity, index) in dasiActivities" :key="index" class="dasi-item">
                <input
                  type="checkbox"
                  :value="activity.points"
                  v-model="selectedActivities"
               />
                <label class="option-text">{{ activity.text }}</label>
              </div>
            </div>
            <p class="label-large">VO₂peak : {{ calculatedVO2Peak }} mL/kg/min</p>
          </div>



          <!-- 多选题 -->
          <div
            v-if="
              question.id !== 100 &&
              !submittedAnswer &&
              question.type === 'multiple_choice'
            "
            class="options-container"
          >
            <div v-for="option in question.options" :key="option" class="option">
              <label>
                <input type="checkbox" :value="option" v-model="selectedOptions" />
                <span class="option-text">{{ option }}</span>
              </label>
            </div>
          </div>

          <!-- 单选题 -->
          <div
            v-if="
              question.id !== 100 &&
              !submittedAnswer &&
              question.type === 'single_choice'
            "
            class="options-container"
          >
            <div v-for="option in question.options" :key="option" class="option">
              <label>
                <input type="radio" :value="option" v-model="selectedOption" />
                <span class="option-text">{{ option }}</span>
              </label>
            </div>
          </div>

          <!-- 文本题 (question.id = 25) - 计算BMI -->
          <div
            v-if="
              question.id !== 100 &&
              !submittedAnswer &&
              question.type === 'text' &&
              question.id === 25
            "
            class="bmi-container"
          >
            <div class="bmi-row">
              <label class="label-large">Height:</label>
              <input
                type="text"
                v-model="heightFeet"
                placeholder="Feet"
                class="bmi-input"
              />
              <span>ft</span>
              <input
                type="text"
                v-model="heightInches"
                placeholder="Inches"
                class="bmi-input"
              />
              <span>in</span>
            </div>
            <div class="bmi-row">
              <label class="label-large">Weight:</label>
              <input
                type="text"
                v-model="weightLbs"
                placeholder="Pounds"
                class="bmi-input"
              />
              <span>lbs</span>
            </div>
            <div>
              <p class="label-large">BMI: {{ calculatedBMI }}</p>
            </div>
          </div>

          <!-- 普通文本题 (id != 25) -->
          <div
            v-if="
              question.id !== 100 &&
              !submittedAnswer &&
              question.type === 'text' &&
              question.id !== 25
            "
          >
            <input
              type="text"
              v-model="textResponse"
              placeholder="Enter your answer here"
              class="text-input"
            />
          </div>

          <!-- VAS 量表题 -->
          <div
            v-if="
              question.id !== 100 &&
              !submittedAnswer &&
              question.type === 'VAS'
            "
            class="vas-container"
          >
            <input
              type="range"
              min="1"
              max="10"
              v-model="VASToScore"
              class="vas-slider"
            />
            <label class="option-text">{{ VASToScore }}</label>
          </div>

          <!-- 结束页: question.id = 100 -->
          <p v-if="question.id === 100" class="message">
            Thanks for your participation!
          </p>

          <div class="button-group" v-if="question.id === 100">
          <button @click="closeSurvey">Close Survey</button>
          </div>

          <!-- 提交后显示的信息（如果不是结束页） -->
          <p v-if="submittedAnswer && question.id !== 100" class="message">
            {{ message }}
          </p>

          <!-- 底部按钮组（非结束页才显示） -->
          <div class="button-group" v-if="question.id !== 100">
            <button @click="goBack">Back</button>
            <button v-if="!submittedAnswer" @click="submitAnswer">Submit</button>
            <button v-if="submittedAnswer" @click="goNext">Next</button>
          </div>
        </div>
      </div>
    </transition>
    <!--医生图片 -->
          <div >
          <img class="doctor-image" src="@/assets/images/doctor.png" alt="Doctor" />
          </div>
    </div>
</template>

<script>
export default {
  data() {
    return {
      question: {},
      selectedActivities: [],
      selectedOptions: [],
      VASToScore: '5',
      textResponse: '', 
      message: '',
      nextQuestionId: 0,
      submittedAnswer: false,
      heightFeet: '',
      heightInches: '',
      weightLbs: '',
      selectedOption: '',
      questionHistory: [],
      dasiActivities: [
        { text: "Take care of yourself, such as eating, dressing, bathing, or using the toilet", points: 2.75 },
        { text: "Walk indoors, such as around your house", points: 1.75 },
        { text: "Walk a block or two on level ground", points: 2.75 },
        { text: "Climb a flight of stairs or walk up a hill", points: 5.50 },
        { text: "Run a short distance", points: 8.00 },
        { text: "Do light work around the house, such as dusting or washing dishes", points: 2.70 },
        { text: "Do moderate work around the house, such as vacuuming, sweeping floors, or carrying groceries", points: 3.50 },
        { text: "Do heavy work around the house, such as scrubbing floors or lifting and moving heavy objects", points: 8.00 },
        { text: "Do yard work, such as raking leaves, weeding, or pushing a power mower", points: 4.50 },
        { text: "Have sexual relations", points: 5.25 },
        { text: "Participate in moderate recreational activities, such as golf, bowling, dancing, doubles tennis, or throwing a baseball or football", points: 6.00 },
        { text: "Participate in strenuous sports, such as swimming, singles tennis, football, basketball, or skiing", points: 7.50 },
      ]
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
    },
    calculatedVO2Peak() {
    const totalScore = this.selectedActivities.reduce((sum, points) => sum + points, 0);
    return (0.43 * totalScore + 9).toFixed(2);
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
        if (this.questionHistory.length === 0 || this.questionHistory[this.questionHistory.length - 1] !== id) {
        this.questionHistory.push(id);
        }
        this.selectedOptions = [];
        this.selectedOption = '';
        this.VASToScore = '5';
        this.textResponse = '';
        this.message = '';
        this.submittedAnswer = false;
      } catch (error) {
        console.error(error);
        this.message = "Error fetching question";
      }
    },
    closeSurvey() {
    // 直接切回 Welcome 页
    this.$emit('changePage', 'welcome');
    },
    goBack() {
      if (this.questionHistory.length > 1) {
        this.questionHistory.pop();
        const previousQuestionId = this.questionHistory[this.questionHistory.length - 1];
        this.fetchQuestion(previousQuestionId);
      } else {
        this.$emit('changePage', 'welcome');
      }
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
        }
        else if (this.question.id === 4) {
          response = await fetch('http://localhost:8000/submit-answer/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              question_id: this.question.id,
              response: this.selectedActivities,
              calculatedVO2: this.calculatedVO2Peak,
            }),
          })
        }
        else if (this.question.type === 'multiple_choice') {
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
        }
            else if (this.question.type === 'VAS') {
            console.log("Submitting VAS value: ", this.VASToScore);
            response = await fetch('http://localhost:8000/submit-answer/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
            question_id: this.question.id,
            response: [this.VASToScore]
          })
      });
    }

        else if (this.question.type === 'text') {
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
.avatar-layout {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 1528px;
  height: 738.4px;
  background-color: #e7f8f7;
  box-sizing: border-box;
  position: relative;
  overflow: hidden; /* 避免动画中出现滚动条 */
  transition: opacity 0.6s ease;
}

/* 进场离场动画可保留不变 */
.slide-enter-from {
  transform: translateX(100%);
}
.slide-enter-to {
  transform: translateX(0);
}
.slide-enter-active {
  transition: transform 0.6s ease;
}
.slide-leave-from {
  transform: translateX(0);
}
.slide-leave-to {
  transform: translateX(-100%);
}
.slide-leave-active {
  transition: transform 0.6s ease;
}

/* 气泡容器 - 固定高度，使其大小不随内容变动 */
.speech-bubble {
  position: relative;
  width: 1300px;
  min-height: 640.36px;
  max-height: 680px;
  background: #fff;
  border-radius: 20px;
  padding: 50px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  box-sizing: border-box;
}

/* 医生图片 */
.doctor-image {
  position: absolute;
  bottom: 20px;
  right: 20px;
  max-width: 180px;
  border-radius: 12px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}
.doctor-image:hover {
  transform: scale(1.05);
}

/* 问题文本 */
.question-text {
  text-align: center;
  color: #333;
  font-size: 1.8rem;
  font-weight: bold;
  margin-bottom: 20px;
}

/* 多/单选的选项容器 */
.options-container {
  margin: 20px 0;
  width: 100%;         /* 占满气泡容器宽度 */
  padding: 0 10px;
}

/* 单个选项（多选/单选） */
.option {
  display: flex;
  align-items: center;
  margin: 15px 0;
  text-align: left;   /* 左对齐 */
}
.option-text {
  font-size: 1.6rem;
  margin-left: 8px;
  color: #333;
}
input[type="checkbox"],
input[type="radio"] {
  transform: scale(1.4);
  cursor: pointer;
}

/* BMI容器等也左对齐 */
.bmi-container {
  text-align: left;
  max-width: 600px;
  margin: 20px 0;
}
.bmi-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
.label-large {
  font-size: 1.2rem;
  font-weight: bold;
  margin-right: 10px;
}
.bmi-input {
  width: 60px;
  margin: 0 8px;
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 文本题输入 */
.text-input {
  display: block;
  width: 80%;
  max-width: 600px;
  height: 40px;
  margin: 0 auto;
  padding: 8px;
  font-size: 1.1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

/* 提示消息 */
.message {
  margin-top: 24px;
  font-size: 30px;
  font-weight: bold;
  color: #333;
  display: inline-block;
  padding: 10px 20px;
  border-radius: 8px;

}

/* 按钮组 */
.button-group {
  align-self: center;
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}
button {
  padding: 12px 24px;
  font-size: 1.2rem;
  font-weight: bold;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 8px;
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

.vas-container {
  display: flex;           /* 让内部子元素水平排布 */
  justify-content: center;
  align-self: center;/* 水平居中 */
  align-items: center;     /* 垂直居中 */
  gap: 20px;               /* 滑条与数字之间空隙 */
  margin-top: 20px;
}

/* 让滑条本身更宽一些 */
.vas-slider {
  width: 300px;   /* 你可以调到400、500，看自己需求 */
  height: 6px;    /* 轨道高度 */
  outline: none;  /* 移除聚焦边框 */
  cursor: pointer;
}

.dasi-container {
  max-height: 250px;      /* 你可以根据实际情况调整高度 */
  overflow-y: auto;       /* 当内容超出时出现垂直滚动条 */
  margin-bottom: 20px;    /* 让它和 VO2peak文字稍微留点空隙 */
  padding-right: 8px;     /* 预留一些空间避免滚动条覆盖文字 */
}

.dasi-question .option-text {
  font-size: 1.2rem; /* 比你原先 1.8rem 小一点 */
  line-height: 1.4em; /* 若想更紧凑，可以适当调小行高 */
}


/* 响应式 */
@media (max-width: 768px) {
  .speech-bubble {
    width: 95%;
    height: auto;  /* 小屏可让它自适应 */
    padding: 30px;
  }
  .doctor-image {
    max-width: 120px;
  }
}
</style>


