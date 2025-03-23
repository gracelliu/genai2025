<template>
  <div class="notes-page">
    <section id="up"></section>
    <section id="down"></section>

    <div class="overlay">
      <div class="code">
        <h1>{{ matchedDocument?.group ?? '...' }}</h1>
      </div>

      <div class="page">
        <p>This is the notes page for <strong>{{ matchedDocument?.title ?? "Error" }}</strong> in <strong>{{
          matchedDocument?.group ?? '' }}</strong>.</p>
      </div>

      <div class="notes-container">
        <h2 class="notes-title">Notes</h2>


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
            <button class="tts-button" :class="{ playing: isPlaying }" @click="speakText">
            <i class="fas fa-volume-up"></i> {{ isPlaying ? 'Playing' : 'Listen' }}
            </button>
          </div>
          <div>
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
  </div>
</template>




<script>
import axios from 'axios';
import { marked } from 'marked';

export default {
  name: 'NotesPage',
  data() {
    return {
      currentFont: 'opendyslexic',
      contrastMode: "default",
      matchedDocument: null,
      isPlaying: false
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
      utterance.rate = 1; // normal speed
      utterance.pitch = 1; // normal tone

      this.isPlaying = true;
      // Reset back to "not playing" once audio ends
      utterance.onend = () => {
        this.isPlaying = false;
      };

      speechSynthesis.speak(utterance);
    },
    toggleFont() {
      this.currentFont = this.currentFont === 'opendyslexic' ? 'lexend' : 'opendyslexic';
    },
    async fetchDocument() {
      try {
        const response = await axios.get('https://api-clarify.midnightsky.net/api/document/list');
        const documents = response.data;

        // Match only by group (case + whitespace insensitive)
        this.matchedDocument = documents.find(doc => doc.id === parseInt(this.docId));
        console.log("Matched document:", this.matchedDocument);
        console.log(documents)

        if (!this.matchedDocument) {
          console.warn("No document found with id:", this.docId);
        }
      } catch (error) {
        console.error("Failed to fetch documents:", error);
        this.matchedDocument = {
          title: 'Error',
          group: '',
          content: 'Failed to fetch or match documents.'
        };
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

.document-block {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #ddd;
}

#up,
#down {
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


.tts-button {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #e69dee; /* purple default */
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

.tts-button.playing {
  background-color: #b9e6a4; /* green when playing */
}

.tts-button:hover {
  /* Disable hover effect */
  background-color: inherit;
}


/* Contrast Modes */
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

/* Dropdown styling */
.contrast-selector {
  margin-top: 16px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 10px;
}

#contrastMode {
  padding: 6px 10px;
  font-size: 14px;
  border-radius: 4px;
  border: 1px solid #ccc;
  outline: none;
}

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

.tts-button i {
  font-size: 16px;
}

@keyframes down {

  0%,
  100% {
    top: -100px;
  }

  70% {
    top: 700px;
  }
}

@keyframes up {

  0%,
  100% {
    bottom: -100px;
  }

  70% {
    bottom: 700px;
  }
}
</style>