import { createRouter, createWebHistory } from 'vue-router';
import WelcomePage from '@/components/WelcomePage.vue';
import QuestionsPage from '@/components/QuestionsPage.vue';
import WelcomeMessagePage from '@/components/WelcomeMessagePage.vue';

const routes = [
  { path: '/', redirect: '/welcome' },
  { path: '/welcome', name: 'WelcomePage', component: WelcomePage },
  {
    path: '/welcome-message',
    name: 'WelcomeMessagePage',
    component: WelcomeMessagePage,
    props: (route) => ({ message: route.query.message }),
  },
  { path: '/questions', name: 'QuestionsPage', component: QuestionsPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

