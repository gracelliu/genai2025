<template>
    <div class="welcome-page">
      <!-- Welcome Header -->
      <h1>Welcome, Grace</h1>
  
      <!-- Content Section -->
      <div class="content">
        <!-- Recently Added Lectures -->
        <div class="left-column">
          <h2>Recently Added Lectures</h2>
          <ul>
            <li v-for="(lecture, index) in recentLectures" :key="index">
              📘 {{ lecture.title }} - {{ lecture.course }}
            </li>
          </ul>
        </div>
  
        <!-- Courses List -->
        <div class="right-column">
          <h2>Your Courses</h2>
          <ul>
            <!-- Replace <li> with this for courses -->
            <li v-for="course in courses" :key="course">
                <router-link :to="`/course/${course}`">🎓 {{ course }}</router-link>
                    </li>

                    <!-- And this for recently added lectures -->
                    <li v-for="lecture in recentLectures" :key="lecture.title">
                <router-link :to="`/lecture/${lecture.course}/${lecture.title}`">
                    📘 {{ lecture.title }} - {{ lecture.course }}
                </router-link>
            </li>

          </ul>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "WelcomePage",
    data() {
      return {
        recentLectures: [
          { title: "Lecture 9: Loops", course: "CSC100" },
          { title: "Lecture 4: Derivatives", course: "MAT100" },
          { title: "Lecture 6: Probability", course: "STA100" }
        ],
        courses: ["CSC100", "MAT100", "STA100", "BIO100", "CHM100", "PHY100"]
      };
    }
  };
  </script>
  
  <style scoped>
  .welcome-page {
    font-family: Arial, sans-serif;
    padding: 20px;
    background-color: #f4f6f8;
  }
  
  h1 {
    margin-bottom: 24px;
  }
  
  .content {
    display: flex;
    gap: 40px;
    flex-wrap: wrap;
  }
  
  .left-column, .right-column {
    flex: 1;
    min-width: 280px;
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  }
  
  h2 {
    margin-bottom: 12px;
  }
  
  ul {
    list-style: none;
    padding-left: 0;
  }
  
  li {
    margin-bottom: 10px;
    font-size: 16px;
  }
  </style>
  