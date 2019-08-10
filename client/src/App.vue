<template>
  <div id="app">
    <header>
      <nav id="nav">
        <h1>Iambic</h1>
      </nav>
    </header>
    <main>
      <div id="error-box" v-bind:class="{'hide': !showError}">
        {{error}}
      </div>
      <router-view/>
    </main>
  </div>
</template>

<script>
  import {mapState} from "vuex";

  export default {
    computed: {
      showError() {
        return this.error !== ""
      },
      ...mapState({
        error: state => state.error
      })
    }
  }
</script>

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

  #error-box {
    @extend %block-base;
    border: 1px solid $warn;
  }

  .hide {
    display: none !important;
  }

  nav {
    margin: 0;
    padding: $padding;
  }

  #app {
    font-family: $fonts;
  }
</style>
