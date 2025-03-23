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
  padding: 20px;
  background-color: #f4f6f8;
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
</style>


  <script>
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
            { number: 11, title: "Acid-Base Reactions", course: "CHM100" }
        ],
        courses: ["CSC100", "MAT100", "STA100", "BIO100", "CHM100", "PHY100"]
      };
    }
  };
  </script>
  

