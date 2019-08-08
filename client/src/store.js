import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
        workingPost: {
            body: ""
        }
    },
    mutations: {
        updateWorkingBody(state, message) {
            state.workingPost.body = message;
        }
    },
    actions: {
    }
})
