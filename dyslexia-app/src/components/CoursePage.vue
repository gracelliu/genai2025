<template>
    <div class="course-page">
      <h1>{{ courseCode }}</h1>
      <p>This is the course page for {{ courseCode }}.</p>
  
      <div class="lectures">
        <h2>Lectures</h2>
        <ul>
          <li v-for="n in 12" :key="n">
            <router-link :to="`/lecture/${courseCode}/lecture-${n}`">
              Lecture {{ n }}
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "CoursePage",
    data() {
      return {
        courseCode: ''
      };
    },
    mounted() {
      this.courseCode = this.$route.params.courseCode;
    }
  };
  </script>
  
  <style scoped>
  .course-page {
    padding: 20px;
    background-color: #f4f6f8;
  }
  
  .lectures {
    margin-top: 20px;
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  }
  
  ul {
    list-style: none;
    padding: 0;
  }
  
  li {
    font-size: 18px;
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
  