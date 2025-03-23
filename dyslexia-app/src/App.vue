<template>
  <div id="app">
    <!-- ✅ Fixed Logo -->
    <router-link to="/" class="logo-wrapper">
      <img src="@/assets/logo.png" alt="LexiSee Logo" class="floating-logo" />
    </router-link>

    <!-- All your pages render here -->
    <router-view />
  </div>
</template>

<style>
/* Fixed Logo in top-right */
.logo-wrapper {
  position: fixed;
  top: 40px;
  right: 40px;
  z-index: 999;
}

.floating-logo {
  height: 80px;
  width: 80px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.5);
  transition: transform 0.2s ease;
}

.floating-logo:hover {
  transform: scale(1.05);
  cursor: pointer;
  
}
</style>
