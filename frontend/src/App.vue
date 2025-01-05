<template>
  <div id="app">
    <WelcomePage v-if="currentPage === 'welcome'" @changePage="changePage" />
    <QuestionsPage v-if="currentPage === 'questions'" @changePage="changePage" />
  </div>
</template>

<script>
import WelcomePage from './components/WelcomePage.vue';
import QuestionsPage from './components/QuestionsPage.vue';

export default {
  name: 'App',
  components: {
    WelcomePage,
    QuestionsPage,
  },
  data() {
    return {
      currentPage: 'welcome'
    };
  },
  methods: {
    changePage(page) {
      this.currentPage = page
    }
    }
  };
  </script>