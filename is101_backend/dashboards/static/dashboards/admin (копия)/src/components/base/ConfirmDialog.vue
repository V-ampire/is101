<template>
    <v-dialog
        v-model="dialog"
        persistent
        max-width="540"
        content-class="my-custom-dialog"
    >
        <v-card>
            <v-cart-text class="d-flex justify-center my-5">
                <div>{{ description }}</div>
            </v-cart-text>
            <v-spacer></v-spacer>
            <v-card-actions class="d-flex justify-center">
                <v-btn
                    small
                    color="primary"
                    @click="cancelAction"
                >
                    Отмена
                </v-btn>
                <v-btn
                    small
                    color="primary"
                    @click="confirmAction"
                >
                    Подтвердить
                </v-btn>
            </v-card-actions>
        </v-card>

    </v-dialog>
</template>

<script>
/*
Диалог для подтверждения действий.
Слушает событие OPEN_CONFIRM, которое сигнализирует об инициализации диалога.
Обработчик события принимает объект с параметрами:
{
    description: 'Описание действия', // Описание действия которое необходимо подтвердить
    action: someFunction // Вызываемый объект, который будет вызван в случае подтверждения действия
    actionParams: {} // Объект с параметрами, будет передан в вызываемый объект
}

Для событий используется шина событий.
*/
import EventBus from '@/eventBus';

export default {
    data () {
        return {
            dialog: false,
            title: '',
            action: undefined,
            actionParams: {}
        }
    },
    mounted() {
        var self = this;

        EventBus.$on('OPEN_CONFIRM', (params) => {
            console.log()
            self.open();
            self.description = params.description;
            self.action = params.action;
            self.actionParams = params.actionParams;
        });
    },
    methods: {
        open: function() {
            this.dialog = true;
        },
        confirmAction: function() {
            console.log(this.action);
            this.action(this.actionParams);
            this.dialog = false;
        },
        cancelAction: function() {
            this.dialog = false;
        }
    },
}
</script>