import { createRouter, createWebHistory } from 'vue-router';
import OnboardPage from './components/OnboardPage.vue';
import WelcomePage from './components/WelcomePage.vue';
import CoursePage from './components/CoursePage.vue';
import LecturePage from './components/LecturePage.vue';

const routes = [
  { path: '/', name: 'Onboarding', component: OnboardPage }, // default route
  { path: '/home', name: 'Home', component: WelcomePage },
  { path: '/course/:courseCode', name: 'Course', component: CoursePage },
  { path: '/lecture/:course/:lectureId', name: 'Lecture', component: LecturePage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
