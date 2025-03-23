<template>
  <div class="lecture-page">
    <!-- Background blobs -->
    <section id="up"></section>
    <section id="down"></section>

    <!-- Foreground content -->
    <div class="overlay">
      <div class="header">
        <h1>Clarify Mode</h1>
      </div>

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
            <div class="meta-inputs">
              <input v-model="customTitle" placeholder="Lecture Title" />
              <input v-model="customGroup" placeholder="Course Code" />
              <button @click="saveTranscriptToDatabase">Save</button>
            </div>
          </div>
            <div class="transcript-body" ref="transcriptBody" :key="fadeKey">
              <div
                v-for="(section, sIndex) in sections"
                :key="sIndex"
                class="transcript-section"
              >
                <div v-html="renderMarkdown(section)"></div>
                <hr v-if="sIndex < sections.length - 1" />
              </div>
            </div>
        </div>
      </div>
    </div>

    <!-- Toast notification -->
    <div v-if="showToast" class="toast">
      Transcript saved to the database ✅
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useRoute } from 'vue-router';
import { marked } from 'marked';

const route = useRoute();

const customTitle = ref('');
const customGroup = ref('');
const sections = ref([]);
const webcam = ref(null);
const transcriptBody = ref(null);
const showToast = ref(false);

const startWebcam = () => {
  navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
      if (webcam.value) {
        webcam.value.srcObject = stream;
      }
    })
    .catch(err => {
      console.error("Webcam error:", err);
    });
};

const saveTranscriptToDatabase = async () => {
  const joinedMarkdown = sections.value.join('\n\n---\n\n');
  const payload = {
    title: customTitle.value || route.params.lectureId,
    group: customGroup.value || route.params.course,
    content: joinedMarkdown
  };

  try {
    const response = await fetch('https://api-clarify.midnightsky.net/api/document/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    const result = await response.json();
    console.log('Saved to database:', result);
    showToast.value = true;
    setTimeout(() => {
      showToast.value = false;
    }, 3000);
  } catch (err) {
    console.error('Save failed:', err);
    alert('Error saving transcript.');
  }
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
      formData.append('current_section', sections.value.at(-1) || '');

      fetch('https://api-clarify.midnightsky.net/api/new_image', {
        method: 'POST',
        body: formData
      })
        .then(res => res.json())
        .then(data => {
          const updatedSection = data.current_section;
          const prevScrollTop = transcriptBody.value?.scrollTop ?? 0;

          if (data.new_section) {
            sections.value.push(updatedSection);
          } else if (sections.value.length > 0) {
            const currSection = sections.value.at(-1);
            if (updatedSection !== currSection) {
              sections.value[sections.value.length - 1] = updatedSection;
            }
          } else {
            sections.value.push(updatedSection);
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
  }, 2000);
};

onMounted(() => {
  startWebcam();
  startImageCapture();
});

const renderMarkdown = (text) => {
  return marked.parse(text || '');
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Lexend&display=swap');

.lecture-page {
  padding: 20px;
  background-color: #f5f7f9;
  color: #1e1e1e;
  position: relative;
  overflow: hidden;
  min-height: 100vh;
}

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

.header {
  text-align: left;
  margin-bottom: 20px;
}

.content {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.webcam,
.transcript {
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
  flex-direction: column;
  gap: 8px;
  margin-bottom: 10px;
}

.meta-inputs {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}

.meta-inputs input {
  padding: 6px 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  flex-grow: 1;
  min-width: 120px;
}

button {
  background-color: #3a86ff;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
  font-size: 14px;
}

button:hover {
  background-color: #265ecf;
}

.transcript-body {
  max-height: 400px;
  overflow-y: auto;
  line-height: 1.8;
  letter-spacing: 0.02em;
  font-size: 18px;
}

.transcript-section {
  margin-bottom: 20px;
}

.toast {
  position: fixed;
  top: 20px;
  right: 30px;
  background-color: #4caf50;
  color: white;
  padding: 14px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 9999;
  animation: fadeInOut 3s ease forwards;
  font-weight: bold;
}

@keyframes fadeInOut {
  0% { opacity: 0; transform: translateY(-10px); }
  10% { opacity: 1; transform: translateY(0); }
  90% { opacity: 1; transform: translateY(0); }
  100% { opacity: 0; transform: translateY(-10px); }
}
</style>
