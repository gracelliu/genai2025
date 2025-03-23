<template>
  <div class="lecture-page">
    <section id="up"></section>
    <section id="down"></section>

    <div class="overlay">
      <!-- Top Bar -->
      <div class="header">
        <h1>Clarifier</h1>
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
  </div>
</template>


<script>
export default {
  name: "LecturePage",
  data() {
    return {
      courseCode: "CSC100",
      courseTitle: "Introduction to Programming",
      transcriptLines: []
    };
  },
  mounted() {
    this.startWebcam();

    const course = this.$route.params.course;
    const lectureId = this.$route.params.lectureId;
    this.courseCode = course;
    this.courseTitle = `${course} Lecture: ${lectureId}`;

    this.startPollingTranscript();
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
      window.open("https://docs.google.com/", "_blank");
    },
    startPollingTranscript() {
      setInterval(() => {
        fetch("http://localhost:5000/api/transcript")
          .then(res => res.json())
          .then(data => {
            this.transcriptLines = data;
          })
          .catch(err => console.error("Polling error:", err));
      }, 2000);
    }
  }
};
</script>

<style scoped>

.lecture-page {
  padding: 20px;
  background-color: #f5f7f9;
  color: #1e1e1e;
  position: relative;
  min-height: 100vh;
  overflow: hidden;
}

/* Background animation blobs */
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

.overlay {
  position: relative;
  z-index: 1;
  padding: 60px 40px;
}

/* Existing styles */
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
  line-height: 1.8;
  font-size: 18px;
  letter-spacing: 0.02em;
}

button {
  background-color: #3a86ff;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background-color: #265ecf;
}
</style>
