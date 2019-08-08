<template>
    <div>
        <TextBox v-model="body" rows="10"/>
        <Button label="Post!" />
    </div>
</template>

<script>
    import TextBox from "../TextBox";
    import Button from "../Button";
    export default {
        components: {Button, TextBox},
        data() {
            return {
                body:''
            }
        }
    }
</script>

<style scoped lang="scss">
    @import "@/assets/vars.scss";
</style>