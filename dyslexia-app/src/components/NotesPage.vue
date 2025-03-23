<template>
    <div class="notes-page">
      <section id="up"></section>
      <section id="down"></section>
  
      <div class="overlay">
        <div class="code">
          <h1>{{ matchedDocument?.group ?? '...' }}</h1>
        </div>
  
        <div class="page">
          <p>This is the notes page for <strong>{{ matchedDocument?.title ?? "Error" }}</strong> in <strong>{{ matchedDocument?.group ?? '' }}</strong>.</p>
        </div>
  
        <div class="notes-container">
          <h2 class="notes-title">Notes</h2>
          <button @click="toggleFont" class="font-toggle">
            Use {{ currentFont === 'opendyslexic' ? 'Lexend' : 'OpenDyslexic' }} Font
          </button>
  
          <div class="notes-content" :class="currentFont === 'lexend' ? 'lexend-font' : 'opendyslexic-font'">
            <div v-if="!matchedDocument">
              <p>No matching document found.</p>
            </div>
            <div v-else>
              <h3>{{ matchedDocument.title }}</h3>
              <p><strong>Group:</strong> {{ matchedDocument.group }}</p>
              <div v-html="renderMarkdown(matchedDocument.content)"></div>
  
              <!-- 🔴 Delete Button -->
              <button class="delete-button" @click="deleteDocument">
                Delete Lecture
              </button>
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
        matchedDocument: null
      };
    },
    computed: {
      docId() {
        return this.$route.params.docId;
      }
    },
    methods: {
      speakText() {
        const text = "Write your notes here...";
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1;
        utterance.pitch = 1;
        speechSynthesis.speak(utterance);
      },
      toggleFont() {
        this.currentFont = this.currentFont === 'opendyslexic' ? 'lexend' : 'opendyslexic';
      },
      async fetchDocument() {
        try {
          const response = await axios.get('https://api-clarify.midnightsky.net/api/document/list');
          const documents = response.data;
          this.matchedDocument = documents.find(doc => doc.id === parseInt(this.docId));
  
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
      async deleteDocument() {
        const confirmDelete = confirm("Are you sure you want to delete this lecture?");
        if (!confirmDelete) return;
  
        try {
          await axios.delete("https://api-clarify.midnightsky.net/api/document/delete", {
            data: { id: this.docId }
          });
          this.$router.push("/");
        } catch (error) {
          console.error("Failed to delete lecture:", error);
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
  
  .font-toggle:hover {
    background-color: #ffd65a;
  }
  
  .delete-button {
    background-color: #ff6b6b;
    color: white;
    border: none;
    padding: 10px 16px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 20px;
    transition: background-color 0.3s ease;
  }
  
  .delete-button:hover {
    background-color: #d9534f;
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
    align-items: center;
    gap: 8px;
    background-color: #d0f0c0;
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
  