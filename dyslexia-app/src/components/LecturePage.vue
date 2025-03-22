<template>
    <div class="lecture-page">
      <!-- Top Bar -->
      <div class="header">
        <h1>{{ courseCode }}: {{ courseTitle }}</h1>
      </div>
  
      <!-- Main Content -->
      <div class="content">
        <!-- Webcam Feed -->
        <div class="webcam">
          <h2>Your Webcam</h2>
          <video ref="webcam" autoplay playsinline muted></video>
        </div>
  
        <!-- Transcript Section -->
        <div class="transcript">
          <div class="transcript-header">
            <h2>Live Transcript</h2>
            <button @click="openInGoogleDocs">Open in Google Docs</button>
          </div>
          <div class="transcript-body">
            <p v-for="(line, index) in transcriptLines" :key="index">
              {{ line }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "LecturePage",
    data() {
      return {
        courseCode: "CSC100",
        courseTitle: "Introduction to Programming",
        transcriptLines: [
          "Welcome to today's lecture on variables...",
          "We will start with understanding data types...",
          "Let’s take a look at how to declare a variable in Python..."
        ]
      };
    },
    mounted() {
      this.startWebcam();
    },
    methods: {
      startWebcam() {
        navigator.mediaDevices.getUserMedia({ video: true })
          .then(stream => {
            this.$refs.webcam.srcObject = stream;
          })
          .catch(err => {
            console.error("Webcam error:", err);
          });
      },
      openInGoogleDocs() {
        // Placeholder: Replace with real link or function
        window.open("https://docs.google.com/", "_blank");
      }
    }
  };
  </script>
  
  <style scoped>
  .lecture-page {
    font-family: Arial, sans-serif;
    padding: 20px;
    background-color: #f9fafa;
  }
  
  .header {
    text-align: left;
    margin-bottom: 20px;
  }
  
  .content {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
  }
  
  .webcam, .transcript {
    flex: 1;
    min-width: 300px;
    background: white;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
  }
  
  video {
    width: 100%;
    height: auto;
    border-radius: 10px;
    margin-top: 8px;
  }
  
  .transcript-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  
  .transcript-body {
    margin-top: 10px;
    max-height: 400px;
    overflow-y: auto;
    line-height: 1.6;
  }
  
  button {
    background-color: #3b82f6;
    color: white;
    border: none;
    padding: 8px 12px;
    border-radius: 6px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #2563eb;
  }
  </style>
  