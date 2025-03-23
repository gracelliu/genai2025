<template>
  <div class="welcome-page">

    <section id="up"></section>
    <section id="down"></section>

    <div class="overlay">


      <h1>Welcome, Grace</h1>
      <div class="center-button">
        <router-link :to="`/live`" class="shimmer-button">
          CLARIFY ✦˚˖⁺
        </router-link>
      </div>

      <div class="content">
        <!-- LEFT COLUMN: Recently Added Lectures -->

        <!-- RIGHT COLUMN: Courses -->
        <div class="right-column">
          <h2>Your Courses</h2>
          <ul>
            <li v-for="(course, index) in courses" :key="index">
              <router-link class="course-link" :to="`/course/${course}`">🎓 {{ course }}</router-link>
            </li>
          </ul>
        </div>

        <div class="left-column">
          <h2>Recently Added Lectures</h2>
          <ul>
            <li v-for="lecture in recentLectures" :key="lecture.id">
              <router-link class="lecture-link" :to="`/notes/${lecture.id}`">
                📘 Lecture {{ lecture.id }}: {{ lecture.title }}
              </router-link>
            </li>
          </ul>

        </div>

      </div>
    </div>
  </div>
</template>


<style scoped>
.welcome-page {
  position: relative;
  min-height: 100vh;
  padding: 0;
  overflow: hidden;
  background-color: #f4f6f8;
}

/* 🧊 Background blob animation setup */
#up,
#down {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 0;
  animation-duration: 10s;
  animation-iteration-count: infinite;
  animation-timing-function: ease-in-out;
}

#up {
  height: 800px;
  width: 800px;
  background-image: linear-gradient(80deg, rgb(173, 218, 236), rgb(222, 97, 233));
  top: -200px;
  left: -200px;
  animation-name: down;
}

#down {
  height: 500px;
  width: 500px;
  background-image: linear-gradient(80deg, rgba(245, 207, 82, 0.8), rgba(199, 10, 114));
  bottom: -150px;
  right: -150px;
  animation-name: up;
}

/* 🧩 Overlay content styling */
.overlay {
  position: relative;
  z-index: 1;
  padding: 60px 40px;
}


h1 {
  font-size: 45px;
  margin-bottom: 24px;
}

h2 {
  font-size: 30px;
}

.content {
  display: flex;
  gap: 40px;
  flex-wrap: wrap;
}

.center-button {
  display: flex;
  justify-content: center;
  margin: 20px 0 40px 0;
}

.shimmer-button {
  display: inline-block;
  text-align: center;
  padding: 30px 60px;
  margin-top: -30px;
  /* margin-bottom: 20px; */
  font-size: 25px;
  font-weight: 600;
  border-radius: 30px;
  color: white;
  background: linear-gradient(120deg, #b57af1, #734af0, #e2c7ff);
  background-size: 300% 300%;
  animation: shimmer 3s ease infinite;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
  text-decoration: none;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
}

.shimmer-button:hover {
  text-decoration: none !important;
  transform: scale(1.05);
}

@keyframes shimmer {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

.left-column,
.right-column {
  flex: 1;
  min-width: 280px;
  background: white;
  padding: 30px;
  padding-left: 40px;
  padding-bottom: 50px;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

ul {
  list-style: none;
  padding-left: 0;
}

li {
  font-size: 25px;
  letter-spacing: 0.03em;
  line-height: 1.6;
}

a {
  text-decoration: none;
  color: #2563eb;
}

@keyframes down {

  0%,
  100% {
    top: -100px;
  }

  70% {
    top: 700px;
  }
}

.course-link,
.lecture-link {
  display: block;
  text-decoration: none;
  color: #333;
  background-color: #ffffff;
  border-radius: 10px;
  padding: 16px 20px;
  margin-bottom: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transition: box-shadow 0.2s ease, transform 0.2s ease, background-color 0.3s ease;
  font-weight: 500;
  font-size: 20px;
}

.course-link:hover,
.lecture-link:hover {
  background-color: #734af0;
  color: #ffffff;
  transform: translateY(-3px);
  box-shadow: 0 8px 16px rgba(115, 74, 240, 0.4);
}

@keyframes up {

  0%,
  100% {
    bottom: -100px;
  }

  70% {
    bottom: 700px;
  }
}
</style>

<script>
import axios from 'axios';

export default {
  name: "WelcomePage",
  data() {
    return {
      recentLectures: [],
      courses: []
    };
  },
  methods: {
    async fetchCoursesFromDB() {
      try {
        const res = await axios.get("https://api-clarify.midnightsky.net/api/document/list");
        const documents = res.data;

        // Get unique courses for right column
        this.courses = [
          ...new Set(documents.map(doc => doc.group?.trim()).filter(Boolean))
        ];

        // Sort documents by timestamp (assuming ISO string or numeric)
        const sortedDocs = documents
            .sort((a, b) => new Date(b.time_created) - new Date(a.time_created));

        // Pick top 10 most recent lectures
        this.recentLectures = sortedDocs.slice(0, 10);

      } catch (err) {
        console.error("Failed to load courses and recent lectures:", err);
      }
    }

  },
  mounted() {
    this.fetchCoursesFromDB();
  }
};
</script>
