import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'
import {ERROR_DISPLAY_TIME} from "./config";

Vue.use(Vuex);

// Show error messages for this long (ms)
// Re validate user text once every VALIDATION_TIME ms

export default new Vuex.Store({
    state: {
        error: "",
        posts: [],
        workingPost: {
            body: "",   //The body of the post currently being composed
            loading: false,  //True if a post is currently being sent to the server
            validationErrors: [],
            lastValidatedMessage: ""
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
        receivedValidation(state, {errors, validatedMessage}) {
            state.workingPost.lastValidatedMessage = validatedMessage;
            state.workingPost.validationErrors = errors;
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
                await axios.post('/posts', {
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
        },

        async validate(context) {
            if(context.state.workingPost.body === context.state.workingPost.lastValidatedMessage) {
                // Don't re-validate unchanged text
                return;
            }
            try {
                console.log('validating')
                let validating = context.state.workingPost.body;
                let resp = await axios.post('/validate', {
                    'body': context.state.workingPost.body
                });
                context.commit('receivedValidation', {errors: resp.data, validatedMessage: validating});
            } catch(error) {
                context.dispatch('displayError', error.response.data.message);
            }
        }
    }
})
