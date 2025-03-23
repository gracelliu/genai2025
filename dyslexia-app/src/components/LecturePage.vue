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
        <transition name="fade">
          <div class="transcript-body" ref="transcriptBody" :key="fadeKey">
            <div v-for="(section, sIndex) in sections" :key="sIndex" class="transcript-section">
              <div v-html="renderMarkdown(section)"></div>
              <hr v-if="sIndex < sections.length - 1"/>
            </div>
          </div>
        </transition>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, nextTick} from 'vue';
import {useRoute} from 'vue-router';
import {marked} from 'marked';


const route = useRoute();

const courseCode = ref('');
const courseTitle = ref('');
const sections = ref([]);
const webcam = ref(null);
const fadeKey = ref(0);
const transcriptBody = ref(null);

const startWebcam = () => {
  navigator.mediaDevices.getUserMedia({video: true})
      .then(stream => {
        if (webcam.value) {
          webcam.value.srcObject = stream;
        }
      })
      .catch(err => {
        console.error("Webcam error:", err);
      });
};

const openInGoogleDocs = () => {
  window.open("https://docs.google.com/", "_blank");
};

const startImageCapture = () => {
  setInterval(() => {
    if (!webcam.value) return;

    const video = webcam.value;
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(blob => {
      if (!blob) return;

      const formData = new FormData();
      formData.append('image', blob, 'capture.png');

      fetch('http://localhost:8000/api/new_image', {
        method: 'POST',
        body: formData
      })
          .then(res => res.json())
          .then(data => {
            const updatedSection = data.current_section;
            const prevScrollTop = transcriptBody.value?.scrollTop ?? 0;
            if (data.new_section) {
              sections.value.push(updatedSection);
              fadeKey.value++;
            } else if (sections.value.length > 0) {
              const currSection = sections.value.at(-1);
              if (updatedSection !== currSection) {
                sections.value[sections.value.length - 1] = updatedSection;
                fadeKey.value++;
              }
            } else {
              sections.value.push(updatedSection);
              fadeKey.value++;
            }
            nextTick(() => {
              if (transcriptBody.value) {
                transcriptBody.value.scrollTop = prevScrollTop;
              }
            });
          })
          .catch(err => {
            console.error("Image capture error:", err);
          });
    }, 'image/png');
  }, 4000);
};

onMounted(() => {
  startWebcam();

  const course = route.params.course;
  const lectureId = route.params.lectureId;
  courseCode.value = course;
  courseTitle.value = `${course} Lecture: ${lectureId}`;

  startImageCapture();
});
const renderMarkdown = (text) => {
  return marked.parse(text);
};
renderMarkdown("")
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Lexend&display=swap');

.lecture-page {
  font-family: 'Lexend', sans-serif;
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
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
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
  font-family: 'Lexend', sans-serif;
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

.fade-enter-active {
  transition: opacity 0.6s ease;
}

.fade-enter-from {
  opacity: 0;
}

.transcript-section {
  margin-bottom: 20px;
}
</style>