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
  line-height: 1.8;
  font-size: 16px;
  letter-spacing: 0.02em;
  font-size: 18px;
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
