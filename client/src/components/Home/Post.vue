<template>
    <div class="post">
        <div class="body">{{post.body}}</div>
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

    .body {
        word-wrap: break-word; /* IE>=5.5 */
        white-space: pre; /* IE>=6 */
        white-space: -moz-pre-wrap; /* For Fx<=2 */
        white-space: pre-wrap; /* Fx>3, Opera>8, Safari>3*/
    }

    .created-at {
        margin-top: $margin;
        text-align: right;
        font-size: $font-size-small;
    }
</style>