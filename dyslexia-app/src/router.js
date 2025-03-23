import { createRouter, createWebHistory } from 'vue-router';
import OnboardPage from './components/OnboardPage.vue';
import WelcomePage from './components/WelcomePage.vue';
import CoursePage from './components/CoursePage.vue';
import LecturePage from './components/LecturePage.vue';
import NotesPage from './components/NotesPage.vue'; 

const routes = [
  { path: '/', name: 'Onboarding', component: OnboardPage }, // default route
  { path: '/home', name: 'Home', component: WelcomePage },
  { path: '/course/:courseCode', name: 'Course', component: CoursePage },
  { path: '/lecture', name: 'Lecture', component: LecturePage },
  { path: '/notes/:docId', name: 'Notes', component: NotesPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
