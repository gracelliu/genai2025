<template>
    <div class="welcome-page">
      <h1>Welcome, Grace</h1>
  
      <div class="content">
        <!-- LEFT COLUMN: Recently Added Lectures -->
        <div class="left-column">
          <h2>Recently Added Lectures</h2>
          <ul>
            <li v-for="(lecture, index) in recentLectures" :key="index">
              <router-link :to="`/lecture/${lecture.course}/lecture-${lecture.number}`">
                📘 Lecture {{ lecture.number }}: {{ lecture.title }} - {{ lecture.course }}
              </router-link>
            </li>
          </ul>
        </div>
  
        <!-- RIGHT COLUMN: Courses -->
        <div class="right-column">
          <h2>Your Courses</h2>
          <ul>
            <li v-for="(course, index) in courses" :key="index">
              <router-link :to="`/course/${course}`">🎓 {{ course }}</router-link>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </template>
  

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

.left-column,
.right-column {
  flex: 1;
  min-width: 280px;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

ul {
  list-style: none;
  padding-left: 0;
}

li {
  margin-bottom: 10px;
  font-size: 16px;
}

a {
  text-decoration: none;
  color: #2563eb;
}

a:hover {
  text-decoration: underline;
}
</style>


  <script>
  export default {
    name: "WelcomePage",
    data() {
      return {
        recentLectures: [
          { number: 9, title: "Loops", course: "CSC100" },
          { number: 4, title: "Derivatives", course: "MAT100" },
          { number: 6, title: "Probability", course: "STA100" }
        ],
        courses: ["CSC100", "MAT100", "STA100", "BIO100", "CHM100", "PHY100"]
      };
    }
  };
  </script>
  

