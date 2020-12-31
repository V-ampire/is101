<template>
    <v-snackbar v-model="show" :top="top" :color="color">
        {{ message }}
        <v-btn text color="accent" @click.native="show = false">
            <v-icon>close</v-icon>
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
    message: 'message
}

Для событий используется шина событий.
*/
import EventBus from '@/eventBus'

export default {
    data() {
        return {
            show: false,
            top: true,
            message: "",
            color: "",
            timeout: 5000,
            colors: {
                success: 'success',
                error: 'red'
            }
        };
    },
    mounted: function() {
        var self = this;

        EventBus.$on('OPEN_STATUS_ALERT', (params) => {
            self.show = true;
            self.message = params.message;
            self.color = colors[params.status];
        });

    }
};
</script>