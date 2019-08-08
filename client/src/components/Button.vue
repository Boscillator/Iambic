<template>
    <button @click="clicked">{{label}}</button>
</template>

<script>
    export default {
        name: "Button",
        props: ["label"],
        methods: {
            clicked() {
                this.$emit('click')
            }
        }
    }
</script>

<style scoped lang="scss">
    @import "../assets/vars.scss";

    button {
        @extend %block-base;
    }
</style>