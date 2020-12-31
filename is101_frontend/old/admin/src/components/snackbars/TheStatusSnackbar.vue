<template>
    <v-snackbar 
        v-model="snackbar" 
        :top="top" 
    >
        <v-alert
            dense
            outlined
            type="error"
        >
            {{ message }}
    </v-alert>
        <v-btn text color="accent" @click="snackbar = false">
            <v-icon>mdi-close-circle</v-icon>
        </v-btn>
    </v-snackbar>
</template>

<script>
/*
Главное выпадающее окно с уведомлениями об успешноси действий.
Слушает событие OPEN_STATUS_ALERT, которое сигнализирует об открытии уведомления.
Обработчик события принимает объект с параметрами
{
    status: 'success/error',
    message: 'message'
}

Для событий используется шина событий.
*/
import {OPEN_STATUS_ALERT} from '@/events/eventsList'
import EventBus from '@/events/eventBus'

export default {
    data () {
        return {
            snackbar: false,
            top: true,
            message: "",
            color: "",
            colors: {
                success: 'success',
                error: 'red'
            },
        }
    },
    mounted: function() {
        var self = this;

        EventBus.$on(OPEN_STATUS_ALERT, (params) => {
            console.log(params);
            self.snackbar = true;
            self.message = params.message;
            self.color = self.colors[params.status];
        });
    }
}
</script>