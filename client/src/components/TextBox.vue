<template>
    <textarea
        :value="value"
        @input="input"
        :rows="rows"
        :cols="cols"
    >
    </textarea>
</template>

<script>
    /*
    Styled textarea component.
     */
    export default {
        name: "TextBox",
        props: {
            value: String,
            rows: {
                type: String,
                default: "4"
            },
            cols: {
                type: String,
                default: "30"
            }
        },
        methods: {
            input(event) {
                this.$emit('input', event.target.value)
            }
        }
    }
</script>

<style scoped lang="scss">
    @import "../assets/vars.scss";
    textarea {
        @extend %block-base;
        width: 100%;
    }
</style>