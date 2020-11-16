<template>
    <ul>
        <li><button @click="ready">Первый</button></li>
        <li><button @click="ready">Второй</button></li>
    </ul>
</template>


<script>
export default {
    methods: {
        ready() {
            console.log('Ready!')
        }
    }
}
</script>
