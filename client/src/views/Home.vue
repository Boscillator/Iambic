<template>
    <div>
        <PostBox />
        <hr />
        <PostsView />
    </div>
</template>

<script>
    import PostBox from '@/components/Home/PostBox.vue'
    import PostsView from "../components/Home/PostsView";
    export default {
        components: {
            PostsView,
            PostBox
        }
    }
</script>
