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
                type: Number,
                default: 4
            },
            cols: {
                type: Number,
                default: 30
            }
        },
        methods: {
            input(event) {
                this.$emit('input', event.target.parameters)
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