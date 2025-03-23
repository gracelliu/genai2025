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
              <router-link :to="`/course/${course}`"
                >🎓 {{ course }}</router-link
              >
            </li>
          </ul>
        </div>

        <div class="left-column">
          <h2>Recently Added Lectures</h2>
          <ul>
            <li v-for="(lecture, index) in recentLectures" :key="index">
                <router-link :to="`/live`">
              >
                📘 Lecture {{ lecture.number }}: {{ lecture.title }} -
                {{ lecture.course }}
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
#up, #down {
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
  font-size: 40px;
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
  padding: 20px 40px;
  font-size: 20px;
  font-weight: 600;
  border-radius: 10px;
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

a:hover {
  text-decoration: underline;
}

@keyframes down {
  0%, 100% {
    top: -100px;
  }
  70% {
    top: 700px; 
  }
}

@keyframes up {
  0%, 100% {
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
      recentLectures: [
        { number: 9, title: "Loops", course: "CSC100" },
        { number: 4, title: "Derivatives", course: "MAT100" },
        { number: 6, title: "Probability", course: "STA100" },
        { number: 2, title: "Logical Statements", course: "CSC100" },
        { number: 5, title: "Mendelian Genetics", course: "BIO100" },
        { number: 3, title: "Chemical Bonding", course: "CHM100" },
        { number: 7, title: "Newton’s Laws", course: "PHY100" },
        { number: 8, title: "Hypothesis Testing", course: "STA100" },
        { number: 6, title: "Functions and Graphs", course: "MAT100" },
        { number: 10, title: "Python Functions", course: "CSC100" },
        { number: 1, title: "Introduction to Biology", course: "BIO100" },
        { number: 11, title: "Acid-Base Reactions", course: "CHM100" },
      ],
      courses: []
    };
  },
  methods: {
    async fetchCoursesFromDB() {
      try {
        const res = await axios.get("https://api-clarify.midnightsky.net/api/document/list");
        const documents = res.data;

        // Extract unique group codes (i.e., course codes)
        this.courses = [
          ...new Set(documents.map(doc => doc.group?.trim()).filter(Boolean))
        ];
      } catch (err) {
        console.error("Failed to load courses:", err);
      }
    }
  },
  mounted() {
    this.fetchCoursesFromDB();
  }
};
</script>
