<template>
  <div id="app">
    <header>
      <nav id="nav">
        <h1>Iambic</h1>
      </nav>
    </header>
    <main>
      <router-view/>
    </main>
  </div>
</template>

<style lang="scss">
  @import "assets/vars.scss";
  header {
    h1 {
      display: inline-block;
      margin-top: $margin;
      margin-bottom: $margin;
      margin-left: $margin;
      margin-right: $wide-margin;
    }
  }
  main {
    margin: auto;
    max-width: 720px;
  }

  nav {
    margin: 0;
    padding: $padding;
  }

  #app {
    font-family: $fonts;
  }
</style>
