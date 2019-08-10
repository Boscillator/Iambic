import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex);

const ERROR_DISPLAY_TIME = 3000;

export default new Vuex.Store({
    state: {
        error: "",
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
        }
    },
    actions: {
        async postMessage(context) {
            context.commit("setSendingPost");
            try {
                console.log(context.state.workingPost.body)
                let resp = await axios.post('/posts', {
                    'body': context.state.workingPost.body
                });
            } catch(error) {
                context.dispatch('displayError', error.response.data.message);
            }
            context.commit("receivedConformationOfLoadingPostSent");
        },

        displayError(context, error) {
            context.commit('setError', error);
            setTimeout(() => context.commit('clearError'), ERROR_DISPLAY_TIME);
        }
    }
})
