<template>
  <div class="notes-page">
    <section id="up"></section>
    <section id="down"></section>

    <div class="overlay">
      <div class="code">
        <h1>{{ matchedDocument?.group ?? '...' }}</h1>
      </div>

      <div class="page">
        <p>This is the notes page for <strong>{{ matchedDocument?.title ?? "Error" }}</strong> in
          <strong>{{ matchedDocument?.group ?? '' }}</strong>.
        </p>
      </div>

      <div class="notes-container">
        <div class="notes-header-row">
          <h2 class="notes-title">Notes</h2>
          <button class="delete-button" @click="deleteDocument">
            Delete Lecture
          </button>
        </div>


        <div class="notes-content" :class="[currentFont + '-font', contrastMode + '-contrast']">
          <div class="accessibility-controls">
            <div class="selector">
              <label for="fontSelect">Font:</label>
              <select id="fontSelect" v-model="currentFont">
                <option value="lexend">Lexend</option>
                <option value="opendyslexic">OpenDyslexic</option>
              </select>
            </div>

            <div class="selector">
              <label for="contrastMode">Contrast:</label>
              <select id="contrastMode" v-model="contrastMode">
                <option value="default">Default</option>
                <option value="light">Light</option>
                <option value="dark">Dark</option>
                <option value="high">High Contrast</option>
              </select>
            </div>

            <button class="tts-button" @click="toggleSpeech">
              <i class="fas fa-volume-up"></i> {{ isPlaying ? (isPaused ? 'Resume' : 'Pause') : 'Play' }}
            </button>
          </div>

          <!-- Progress Bar -->
          <div v-if="isPlaying" class="progress-container">
            <div class="progress-bar" :style="{ width: progress + '%' }"></div>
          </div>


          <button class="edit-button" @click="toggleEdit">
            {{ isEditing ? 'Cancel' : 'Edit' }}
          </button>

          <div v-if="isEditing">
            <textarea v-model="editedContent" rows="10" class="edit-textarea"></textarea>
            <button class="save-button" @click="saveDocument">Save Changes</button>
          </div>
          <div v-else>
            <div v-if="!matchedDocument">
              <p>No matching document found.</p>
            </div>
            <div v-else>
              <h3>{{ matchedDocument.title }}</h3>
              <p><strong>Group:</strong> {{ matchedDocument.group }}</p>
              <div v-html="renderMarkdown(matchedDocument.content)"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Red toast for deletion -->
    <div v-if="showDeleteToast" class="toast delete-toast">
      Lecture deleted from the database 🗑️
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {marked} from 'marked';

export default {
  name: 'NotesPage',
  data() {
    return {
      currentFont: 'opendyslexic',
      contrastMode: "default",
      matchedDocument: null,
      isPlaying: false,
      isPaused: false,
      progress: 0,
      utterance: null,
      intervalId: null,
      editedContent: '',
      isEditing: false,
      showDeleteToast: false
    };
  },
  computed: {
    docId() {
      return this.$route.params.docId;
    }
  },
  methods: {
    speakText() {
      const text = this.matchedDocument.content;
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 1;
      utterance.pitch = 1;
      this.isPlaying = true;
      utterance.onend = () => {
        this.isPlaying = false;
      };
      speechSynthesis.speak(utterance);
    },
    toggleSpeech() {
      if (!this.matchedDocument) return;

      // Resume
      if (this.isPaused) {
        speechSynthesis.resume();
        this.isPaused = false;
        return;
      }

      // Pause
      if (this.isPlaying) {
        speechSynthesis.pause();
        this.isPaused = true;
        return;
      }

      // Fresh playback
      const text = this.matchedDocument.content;
      this.utterance = new SpeechSynthesisUtterance(text);
      this.utterance.rate = 1;
      this.utterance.pitch = 1;

      this.isPlaying = true;
      this.isPaused = false;
      this.progress = 0;

      const words = text.split(' ');
      let currentWordIndex = 0;

      // Estimate progress based on word count
      this.utterance.onboundary = (event) => {
        if (event.name === 'word') {
          currentWordIndex++;
          this.progress = Math.min(100, (currentWordIndex / words.length) * 100);
        }
      };

      this.utterance.onend = () => {
        this.isPlaying = false;
        this.isPaused = false;
        this.progress = 100;
      };

      speechSynthesis.cancel(); // Stop anything else playing
      speechSynthesis.speak(this.utterance);
    },
    async fetchDocument() {
      try {
        const response = await axios.get('https://api-clarify.midnightsky.net/api/document/list');
        this.matchedDocument = response.data.find(doc => doc.id === parseInt(this.docId));
      } catch (error) {
        console.error("Failed to fetch documents:", error);
        this.matchedDocument = {
          title: 'Error',
          group: '',
          content: 'Failed to fetch or match documents.'
        };
      }
    },
    async deleteDocument() {
      try {
        await axios.delete("https://api-clarify.midnightsky.net/api/document/delete", {
          data: {id: this.docId}
        });

        this.showDeleteToast = true;
        setTimeout(() => {
          window.location.href = "/home";
        }, 2000);
      } catch (error) {
        console.error("Failed to delete lecture:", error);
        window.location.href = "/home";
      }
    },
    toggleEdit() {
      this.isEditing = !this.isEditing;
      if (this.isEditing) {
        this.editedContent = this.matchedDocument.content;
      }
    },
    async saveDocument() {
      try {
        await axios.post("https://api-clarify.midnightsky.net/api/document/update", {
          id: this.docId,
          content: this.editedContent,
          title: this.matchedDocument.title,
          group: this.matchedDocument.group
        });
        this.matchedDocument.content = this.editedContent;
        this.isEditing = false;
      } catch (error) {
        console.error("Failed to update lecture:", error);
      }
    },
    renderMarkdown(text) {
      return marked.parse(text || '');
    }
  },
  mounted() {
    this.fetchDocument();
  }
};
</script>

<style scoped>
/* core layout */
.notes-page {
  padding: 20px;
  background-color: #f4f6f8;
}

/* headers */
.code {
  font-size: 24px;
}

.page {
  font-size: 20px;
  margin-bottom: 20px;
}

/* note container */
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

/* notes styling */
.notes-content {
  background-color: #f0f4ff;
  border: 1px solid #c3dafe;
  border-radius: 16px;
  padding: 16px;
  min-height: 200px;
  font-size: 16px;
  color: #1e1e1e;
}

/* accessibility controls */
.accessibility-controls {
  display: flex;
  gap: 24px;
  margin-bottom: 16px;
  align-items: center;
  justify-content: flex-start;
}

.selector {
  display: flex;
  flex-direction: column;
}

.selector label {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 4px;
}

.selector select {
  padding: 6px 10px;
  font-size: 14px;
  border-radius: 4px;
  border: 1px solid #ccc;
  outline: none;
}

/* fonts and contrast */
.lexend-font {
  font-family: 'Lexend', sans-serif;
}

.opendyslexic-font {
  font-family: 'OpenDyslexic', sans-serif;
}

.default-contrast {
  background-color: #f0f4ff;
  color: #1e1e1e;
}

.light-contrast {
  background-color: #fff9db;
  color: #000;
}

.dark-contrast {
  background-color: #1e1e1e;
  color: #f4f4f4;
}

.high-contrast {
  background-color: #ffff00;
  color: #000;
}

/* speech button */
.tts-button {
  display: inline-flex;
  margin-top: 40px;
  align-items: center;
  gap: 8px;
  background-color: #e69dee;
  color: #000;
  padding: 8px 14px;
  font-size: 14px;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-bottom: 16px;
  transition: background-color 0.3s ease;
}

.tts-button:hover {
  background-color: #b9e6a4;
}

/* delete button */
.delete-button {
  background-color: #f8d7da;
  color: #721c24;
  border: none;
  border-radius: 6px;
  padding: 10px 16px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 20px;
  transition: background-color 0.3s ease;
  margin-bottom: 20px;
}

.delete-button:hover {
  background-color: #f5c6cb;
}

/* edit button */
.edit-button, .save-button {
  padding: 8px 12px;
  margin-top: 12px;
  font-weight: bold;
  cursor: pointer;
  border-radius: 6px;
  border: none;
  transition: background-color 0.3s ease;
}

.edit-button {
  background-color: #cce5ff;
  color: #004085;
}

.edit-button:hover {
  background-color: #b8daff;
}

.save-button {
  background-color: #d4edda;
  color: #155724;
}

.save-button:hover {
  background-color: #c3e6cb;
}

.edit-textarea {
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #ccc;
  font-family: monospace;
  margin-top: 12px;
  resize: vertical;
}


.notes-header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 0 8px;
}

/* animated toast */
.toast {
  position: fixed;
  top: 20px;
  right: 30px;
  padding: 14px 20px;
  border-radius: 8px;
  font-weight: bold;
  z-index: 9999;
  animation: fadeInOut 3s ease forwards;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.delete-toast {
  background-color: #f8d7da;
  color: #721c24;
}

/* fade animation */
@keyframes fadeInOut {
  0% {
    opacity: 0;
    transform: translateY(-10px);
  }
  10% {
    opacity: 1;
    transform: translateY(0);
  }
  90% {
    opacity: 1;
    transform: translateY(0);
  }
  100% {
    opacity: 0;
    transform: translateY(-10px);
  }
}

/* background animation */
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

.progress-container {
  margin-top: 8px;
  background-color: #ddd;
  height: 8px;
  width: 100%;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: #b9e6a4;
  width: 0%;
  transition: width 0.25s ease;
}

</style>