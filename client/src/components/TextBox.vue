<template>
    <div class="container">
        <div ref="backdrop" class="backdrop">
            <div class="highlights" v-html="highlight_html"></div>
        </div>
        <textarea class="editor" ref="editor" :value="value" @input="input"></textarea>
    </div>
</template>

<script>
    /*
    Styled textarea component.
     */
    export default {
        name: "TextBox",
        props: {
            value: String,
            errors: Array,
            rows: {
                type: String,
                default: "4"
            },
            cols: {
                type: String,
                default: "30"
            }
        },
        computed: {
            highlight_html: {
                get() {
                    let lines = this.value.split('\n');
                    let result = "";
                    for (let line_idx in lines) {
                        let line = lines[line_idx];
                        let err = this.errors[line_idx];
                        if (typeof err === "undefined") {
                            // There is no matching error for this line, don't change it.
                            result += line + '\n';
                            continue;
                        }

                        // Match the nth word and surround it with <mark>
                        const regex = `^((?:.*?\\s){${err.at}})(.*?)(\\s.*)?$`;
                        const re = RegExp(regex);
                        const new_line = line.replace(re, "$1<mark>$2</mark>$3");
                        result += new_line + '\n';
                    }
                    return result;
                }
            }
        },
        methods: {
            input(event) {
                this.$emit('input', event.target.value)
            }
        }
    }
</script>

<style lang="scss">

    // This cannot be scoped as we are directly generating html
    @import "../assets/vars.scss";

    mark {
        border-radius: 3px;
        color: transparent;
        background-color: $warn;
    }
</style>

<style scoped lang="scss">
    @import "../assets/vars.scss";

    // A lot copied from https://codersblock.com/blog/highlight-text-inside-a-textarea/

    *, *::before, *::after {
        box-sizing: border-box;
    }

    body {
        margin: 30px;
        background-color: #f0f0f0;
    }

    .container, .backdrop, textarea {
        width: 460px;
        height: 180px;
    }

    .highlights, textarea {
        padding: 10px;
        font: 20px/28px $fonts;
        letter-spacing: 1px;
    }

    .container {
        display: block;
        margin: 0 auto;
        transform: translateZ(0);
        -webkit-text-size-adjust: none;
    }

    .backdrop {
        position: absolute;
        z-index: 1;
        border: 2px solid #685972;
        background-color: #fff;
        overflow: auto;
        pointer-events: none;
        transition: transform 1s;
    }

    .highlights {
        white-space: pre-wrap;
        word-wrap: break-word;
        color: transparent;
    }

    textarea {
        display: block;
        position: absolute;
        z-index: 2;
        margin: 0;
        border: 2px solid #74637f;
        border-radius: 0;
        /*color: #444;*/
        background-color: transparent;
        overflow: auto;
        resize: none;
        transition: transform 1s;
    }

    .perspective .backdrop {
        transform: perspective(1500px) translateX(-125px) rotateY(45deg) scale(.9);
    }

    .perspective textarea {
        transform: perspective(1500px) translateX(155px) rotateY(45deg) scale(1.1);
    }

    textarea:focus, button:focus {
        outline: none;
        box-shadow: 0 0 0 2px #c6aada;
    }

</style>