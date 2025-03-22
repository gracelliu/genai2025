import { createRouter, createWebHistory } from 'vue-router';
import WelcomePage from './components/WelcomePage.vue';
import LecturePage from './components/LecturePage.vue';
import CoursePage from './components/CoursePage.vue'; // you'll make this soon

const routes = [
  { path: '/', name: 'Home', component: WelcomePage },
  { path: '/lecture/:course/:lectureId', name: 'Lecture', component: LecturePage },
  { path: '/course/:courseCode', name: 'Course', component: CoursePage },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
