<template>
    <div class="notes-page">
      <section id="up"></section>
      <section id="down"></section>
  
      <div class="overlay">
        <div class="code">
          <h1>{{ courseCode }}</h1>
        </div>
  
        <div class="page">
          <p>This is the notes page for <strong>{{ lectureId }}</strong> in <strong>{{ courseCode }}</strong>.</p>
        </div>
  
        <div class="notes-container">
          <h2 class="notes-title">Notes</h2>
          <button @click="toggleFont" class="font-toggle">
            Use {{ currentFont === 'opendyslexic' ? 'Lexend' : 'OpenDyslexic' }} Font
          </button>

          <div class="notes-content" :class="currentFont === 'lexend' ? 'lexend-font' : 'opendyslexic-font'">

            <p>Write your notes here...</p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'NotesPage',
    data() {
      return {
        currentFont: 'opendyslexic'
      };
    },

    computed: {
      courseCode() {
        return this.$route.params.courseCode;
      },
      lectureId() {
        return this.$route.params.lectureId;
      }
    },
    methods: {
    toggleFont() {
      this.currentFont = this.currentFont === 'opendyslexic' ? 'lexend' : 'opendyslexic';
    }
  }
  };
  </script>
  
  <style scoped>
  .notes-page {
    padding: 20px;
    background-color: #f4f6f8;
  }
  
  .code {
    font-size: 24px;
  }
  
  .page {
    font-size: 20px;
    margin-bottom: 20px;
  }
  
  .notes-container {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }
  
  .notes-title {
    margin-bottom: 16px;
    font-size: 22px;
    margin-left: 8px;
  }
  
  .notes-content {
    background-color: #f0f4ff;
    border: 1px solid #c3dafe;
    border-radius: 16px;
    padding: 16px;
    min-height: 200px;
    font-size: 16px;
    color: #1e1e1e;
  }
  
  /* 🔵 Background blob animation */
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
  
  .overlay {
    position: relative;
    z-index: 1;
    padding: 60px 40px;
  }
  .lexend-font {
  font-family: 'Lexend', sans-serif;
}

.opendyslexic-font {
  font-family: 'OpenDyslexic', sans-serif;
}

.font-toggle {
  background-color: #ffe28a;
  color: #000;
  border: none;
  border-radius: 6px;
  padding: 8px 16px;
  cursor: pointer;
  font-weight: bold;
  font-size: 14px;
  transition: background-color 0.3s ease;
  margin-bottom: 16px;
}
.font-toggle:hover {
  background-color: #ffd65a;
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
  