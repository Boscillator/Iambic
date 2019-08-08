import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
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
        }
    },
    actions: {
        async postMessage(context) {
            context.commit("setSendingPost");
            setTimeout(function(){
                context.commit("receivedConformationOfLoadingPostSent");
            }, 500);
        }
    }
})
