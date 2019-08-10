<template>
    <div class="post">
        {{post.body}}
    </div>
</template>

<script>
    export default {
        name: "Post",
        props: ['post']
    }
</script>

<style scoped lang="scss">
    @import "../../assets/vars.scss";
    .post {
        @extend %block-base;
        padding: $padding;
        text-align: center;
        max-width: $max-width/2;
        margin: $margin auto;

        box-shadow: 1px 1px 1px 1px $shadow;
    }
</style>