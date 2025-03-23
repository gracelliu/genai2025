<template>
  <div class="lexisee">
    <section id="up"></section>
    <section id="down"></section>

    <div class="overlay">
      <h1>LexiSee</h1>
      <p>
        LexiSee is an accessibility-focused tool designed to support individuals with dyslexia by converting handwritten text into clear, simplified course notes using dyslexia-friendly fonts like Lexend. Built to ease comprehension and boost learning confidence.
      </p>
      <a href="https://www.dyslexia.com/about-dyslexia/" target="_blank">Learn more about dyslexia here</a>
      <button @click="goToLogin">Get Started</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "LexiseeComponent",
  methods: {
    goToLogin() {
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background-image: linear-gradient(80deg, rgb(5,124,172), rgb(199,10,114));
  overflow: hidden; 
  font-family: 'Lexend', sans-serif;
  color: white;
}

#up, #down, #left, #right {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  z-index: 0;
}

#up {
  height: 800px; 
  width: 800px; 
  background-image: linear-gradient(80deg, rgb(173, 218, 236), rgb(222, 97, 233));
  animation: down 20s infinite; 
}

#down {
  right: 0;
  height: 500px; 
  width: 500px;
  background-image: linear-gradient(80deg, rgba(245, 207, 82, 0.8), rgba(199, 10, 114));
  animation: up 20s infinite;
}

.overlay {
  position: relative;
  z-index: 1;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0 20px;
}

.overlay h1 {
  font-size: 7rem;
  margin: 0 0 25px 0;
}

.overlay p {
  font-size: 1.3rem;
  max-width: 800px;
  margin: 0 0 25px 0;
  line-height: 1.5;
}

.overlay a {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  margin-bottom: 35px;
}

.overlay a:hover {
  text-decoration: underline;
  color: #fce49d;
}

.overlay button {
  padding: 20px 40px;
  font-size: 1.4rem;
  font-family: 'Lexend', sans-serif;
  border: none;
  border-radius: 8px;
  background-color: #ffe28a;
  color: #000;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.overlay button:hover {
  background-color: #ffcc4d;
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
