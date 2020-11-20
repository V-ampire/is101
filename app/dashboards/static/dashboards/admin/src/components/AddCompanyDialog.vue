<template>
    <v-dialog
    v-model="dialog"
    max-width="600px"
    >
        <template v-slot:activator="{ on, attrs }">
            <v-btn
            color="primary"
            v-bind="attrs"
            v-on="on"
            >Добавить</v-btn>
        </template>
        <v-card>
            <v-card-title class="headline">Добавить Юр. лицо</v-card-title>
            <v-card-text>
                <company-form></company-form>
            </v-card-text>
            <v-card-actions>
                <v-btn
                    color="primary"
                    text
                    @click="dialog=false"
                >Добавить</v-btn>
                <v-btn
                    color="primary"
                    text
                    @click="dialog=false"
                >Отмена</v-btn>
            </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import CompanyForm from '@/components/CompanyForm'


    export default {
        data: () => ({
        dialog: false,
        }),
        components: {
            'company-form': CompanyForm
        }
    }
</script>