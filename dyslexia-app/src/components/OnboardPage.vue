<template>
  <div class="lexisee">
    <section id="up"></section>
    <section id="down"></section>

    <div class="overlay">
      <h1>Clarity</h1>
      <b>
        A Dyslexia Tool
      </b>
      <p>
        Clarify is a smart AI study companion designed to make learning easier, turning notes into dyslexia-friendly text and boosting focus with personalized tools.
      </p>

      <a href="https://www.dyslexia.com/about-dyslexia/" target="_blank">Learn more about dyslexia here</a>
      <a href="https://opendyslexic.org/" target="_blank">Learn more about the OpenDyslexic font</a>
      <button @click="goToHome">Get Started ✦˚˖⁺</button>
    </div>
  </div>
</template>

<script>
export default {
  name: "LexiseeComponent",
  methods: {
  goToHome() {
    this.$router.push("/home");
    }
  }
};
</script>

<style scoped>
body {
  margin: 0;
  padding: 0;
  min-height: 100vh;
  background-image: linear-gradient(80deg, rgb(5,124,172), rgb(199,10,114));
  overflow: hidden; 
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
  margin-top: -20px;
  font-style: italic;
  font-size: 7rem;
  margin-bottom: -10px;
}

.overlay b {
  font-size: 30px;
}

.overlay p {
  font-size: 30px;
  max-width: 800px;
  margin-top: 50px;
  line-height: 1.5;
  margin-bottom: 10px;
}

.overlay a {
  font-size: 20px;
  color: blueviolet;
  text-decoration: underline;
}

.overlay a:hover {
  text-decoration: underline;
  color: #fce49d;
}

.overlay button {
  padding: 20px 40px;
  font-size: 1.5rem;
  margin-top: 60px;
  border: none;
  border-radius: 8px;
  background-color: rgb(222, 97, 233);
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
