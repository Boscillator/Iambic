<template>
    <div class="post">
        <div>{{post.body}}</div>
        <div class="created-at">{{post.created_at}}</div>
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

    .created-at {
        margin-top: $margin;
        text-align: right;
        font-size: 12pt;
    }
</style>