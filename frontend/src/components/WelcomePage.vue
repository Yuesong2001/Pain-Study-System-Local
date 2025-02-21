<template>
  <div>
    <!-- 顶部导航部分 -->
    <div class="banner_section">
      <div class="container">
        <nav class="navbar">
          <div class="logo">Northeastern University</div>
          <ul class="nav-links">
            <li><a href="#">About</a></li>
          </ul>
        </nav>

        <div class="row">
          <div class="col-md-6">
            <h1 class="banner_title">
              <span class="pain">Pain</span> <br />
              <span class="survey">Survey</span> <br />
              <span class="system">System</span>
            </h1>
            <div class="btn_main">
              <input
                type="text"
                placeholder="Enter your name"
                class="name-input"
                v-model="username"
              />
              <div class="contact_btn">
                <a href="#" @click.prevent="startSurvey">Get Started</a>
              </div>
            </div>
            <p v-if="hasSubmitted" class="welcome-message">{{ message }}</p>
          </div>
          <div class="col-md-6">
            <div class="image_1">
              <img :src="require('@/assets/images/img-1.png')" alt="Doctor" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
    mounted() {
        document.title = "Pain Study  System";
  },

  data() {
    return {
      username: '',
      message: '',
      showStartButton: false,
      hasSubmitted: false
    };
  },
  methods: {
    async startSurvey() {
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

        localStorage.setItem('username', this.username);

        this.$router.push({
          path: '/welcome-message',
          query: { message: this.message }
        });
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
.banner_section {
  background: linear-gradient(to right, #e7f8f7, rgba(231, 248, 247, 0.7));
  padding: 40px 20px;
  min-height: 90vh;
  display: flex;
  align-items: center; /* 保持垂直居中，如需顶部对齐可改成 flex-start */
}

.container {
  max-width: 1300px;
  margin: 0 auto;
  padding: 0 20px;
}

.navbar {
  display: flex;
  align-items: center; /* 垂直居中 */
  /* 原本是 justify-content: space-between; 这里可以去掉或改为默认 */
}

.logo {
  font-size: 30px;
  font-weight: bold;
  color: #007bff;
  /* 如果想更靠左，可以给它去掉多余 margin */
  margin: 0;
  /* 如果需要它固定左边，可以再让 nav-links 自动推到右边 */
  margin-right: auto;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 30px;
  margin-left: auto; /* 推到右侧 */
}

.nav-links li a {
  text-decoration: none;
  color: #007bff;
  font-size: 30px;
  font-weight: bold;
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  /* 如果想让文字更贴左，图片贴右，可以保持这样 */
}

.col-md-6:last-of-type {
  display: flex;
  justify-content: flex-end;
}

.banner_title {
  font-size: 70px;
  font-weight: bold;
  margin-bottom: 10px;
  text-align: left;  /* 左对齐 */
}

.pain {
  color: #000; /* 黑色 */
}

.survey {
  color: #007bff; /* 蓝色 */
}

.system {
  color: #151515; /* 默认深色 */
}

.banner_text {
  font-size: 22px;
  color: #666;
  margin-bottom: 20px;
}

.btn_main {
  display: flex;
  gap: 15px;
}

.name-input {
  padding: 0 12px;
  height: 48px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.contact_btn a {
  display: inline-flex;
  justify-content: center;
  align-items: center;
  height: 48px;
  padding: 0 24px;
  font-size: 16px;
  font-weight: bold;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  transition: background-color 0.3s ease;
}

.contact_btn a:hover {
  background-color: #0056b3;
}

.image_1 img {
  max-width: 90%;
  display: block;
  margin-right: 0; /* 无需额外间距 */
  margin-left: auto; /* 若要完全贴右，可用 auto 左间距 */
}

</style>