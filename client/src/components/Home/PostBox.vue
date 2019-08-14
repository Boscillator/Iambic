<template>
    <div>
        <TextBox v-model="body" :errors="errors" rows="10"/>
        <Button :disabled="loading" @click="post" label="Post!"/>
    </div>
</template>

<script>
    import TextBox from "../TextBox";
    import Button from "../Button";
    import {mapState} from "vuex";

    export default {
        components: {Button, TextBox},
        data() {
            return {
            }
        },
        computed: {
            body: {
                get() {
                    return this.$store.state.workingPost.body
                },
                set(value) {
                    this.$store.commit('updateWorkingBody', value)
                }
            },
            ...mapState({
                loading: state => state.workingPost.loading,
                errors: state => state.workingPost.validationErrors,
            })
    },
    methods: {
        post() {
            this.$store.dispatch("postMessage");
        }
    }
    }
</script>

<style scoped lang="scss">
    @import "@/assets/vars.scss";
</style>