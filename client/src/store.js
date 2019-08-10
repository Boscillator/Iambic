import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex);

const ERROR_DISPLAY_TIME = 3000;

export default new Vuex.Store({
    state: {
        error: "",
        posts: [],
        workingPost: {
            body: "",   //The body of the post currently being composed
            loading: false  //True if a post is currently being sent to the server
        }
    },
    mutations: {
        setSendingPost(state) {
            state.workingPost.loading = true;
        },
        receivedConformationOfLoadingPostSent(state) {
            state.workingPost.loading = false;
            state.workingPost.body = "";
        },
        updateWorkingBody(state, message) {
            // Update the stores knowledge of the post the user is currently composing.
            state.workingPost.body = message;
        },
        setError(state, message) {
            state.error = message;
        },
        clearError(state) {
            state.error = "";
        },
        receivedPosts(state, posts) {
            state.posts = posts;
        }
    },
    actions: {
        async postMessage(context) {
            context.commit("setSendingPost");
            try {
                let resp = await axios.post('/posts', {
                    'body': context.state.workingPost.body
                });
            } catch(error) {
                context.dispatch('displayError', error.response.data.message);
            }
            context.commit("receivedConformationOfLoadingPostSent");
        },

        displayError(context, error) {
            console.error(error);
            context.commit('setError', error);
            setTimeout(() => context.commit('clearError'), ERROR_DISPLAY_TIME);
        },

        async fetchPosts(context) {
            try {
                let resp = await axios.get('/posts');
                context.commit("receivedPosts", resp.data);
            } catch (error) {
                context.dispatch('displayError', error.response.data.message);
            }
        }
    }
})
