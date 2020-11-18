<template>
    <v-list-item>
        <v-list-item-avatar>
            <v-img
                :src="logo"
                :alt="title"
            >
        </v-list-item-avatar>
        <v-list-item-content>
            <v-list-item-title v-text="title"></v-list-item-title>
            <v-list-item-subtitle v-text="fullAddres"></v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
            <v-btn icon><v-icon>mdi-domain</v-icon></v-btn>
            <v-btn icon><v-icon>mdi-domain</v-icon></v-btn>
        </v-list-item-action>
    </v-list-item>
</template>


<script>
export default {
    props: {
        uuid: String,
        url: String,
        city: String,
        address: String,
        title: String,
        logo: String,
        status: Number
    },
    computed: {
        fullAddres: function() {
            return `${this.city}, ${this.address}`
        }
    }
}
</script>