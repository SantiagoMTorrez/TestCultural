<template>
    <canvas ref="canvas" id="canvas"></canvas>
</template>

<script>
    import { ref, onMounted } from 'vue';
export default {
    name: "ClusterFuck",
    setup(){
        const canvas = ref(null);
        const context = ref(null);
        onMounted(() => {
            context.value = canvas.value.getContext("2d")
        })
        return {canvas}
    }
}
</script>

<style>
    *, *::after, ::before{
        box-sizing: content-box;
        padding: 0px;
        margin: 0px;
    }

    #canvas{
        height: 100vh;
        width: 1000vw;
    }
</style>