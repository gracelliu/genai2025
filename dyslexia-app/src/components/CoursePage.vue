<template>
  <div class="course-page">


    <section id="up"></section>
    <section id="down"></section>

    <div class="overlay">

    <div class="code">
    <h1>{{ courseCode }}</h1></div>

    <div class="page"> 
    <p>This is the course page for {{ courseCode }}.</p> </div>

    <div class="lectures">
      <div class="lecture-size">
      <h2>Lectures</h2></div>
      <div class="lecture-grid">
        <div
          class="lecture-card"
          v-for="n in lectureCount"
          :key="n"
        >
          <router-link :to="`/notes/${courseCode}/lecture-${n}`">
            Lecture {{ n }}
          </router-link>
        </div>
      </div>
      <div class="button-container">
      <button @click="handleAddLecture">Add New Lecture</button>
      
    </div>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: "CoursePage",
  data() {
    return {
      courseCode: '',
      lectureCount: 1, // start with one lecture
    };
  },
  mounted() {
    this.courseCode = this.$route.params.courseCode;
  },
  methods: {
    handleAddLecture() {
      this.lectureCount += 1;
    }
  }


};
</script>

<style scoped>
.course-page {
  padding: 20px;
  background-color: #f4f6f8;
}

.button-container {
  text-align: center;
}

.code {
  font-size: 24px;
}

.lecture-size {
  margin-left: 50px; 
}

.page {
  font-size: 20px; 
}

.lectures {
  margin-top: 20px;
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.lecture-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(200px, 1fr));
  gap: 32px;
  margin-top: 12px;
  margin-bottom: 20px;
}

.lecture-card {
  background-color: #f0f4ff;
  border: 1px solid #c3dafe;
  border-radius: 16px;
  padding: 12px;
  text-align: center;
  transition: box-shadow 0.2s ease;
  margin-left: 50px;
  margin-right: 50px;
}

.lecture-card:hover {
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12);
}

.lecture-card a {
  color: #2563eb;
  font-weight: 500;
  text-decoration: none;
  display: block;
}

.lecture-card a:hover {
  text-decoration: underline;
}

button {
  background-color: #3a86ff;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #265ecf;
}

/* 🧊 Background blob animation setup */
#up, #down {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 0;
  animation-duration: 20s;
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

.overlay {
  position: relative;
  z-index: 1;
  padding: 60px 40px;
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
