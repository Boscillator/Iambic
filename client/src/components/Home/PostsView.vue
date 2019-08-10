<template>
    <div>
        <div v-if="!empty">
            <Post v-for="post in posts" :post="post" />
        </div>
        <div v-else class="empty">
            Nothing here yet...
        </div>
    </div>
</template>

<script>
    import {mapState} from "vuex";
    import Post from "./Post";

    export default {
        name: "PostsView",
        components: {Post},
        mounted() {
            this.$store.dispatch('fetchPosts');
        },
        computed: {
            ...mapState({
                posts: state => state.posts
            }),
            empty() {
                return this.posts.length === 0;
            }
        }
    }
</script>

<style scoped>
    @import '../../assets/vars.scss';
    .empty {
        text-align: center;
        font-style: italic;
    }
</style>