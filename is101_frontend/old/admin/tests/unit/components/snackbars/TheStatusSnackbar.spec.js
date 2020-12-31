import Vue from 'vue'
import Vuetify from 'vuetify'

import StatusSnackbar from '@/components/snackbars/TheStatusSnackbar'
import EventBus from '@/events/eventBus'
import {OPEN_STATUS_ALERT} from '@/events/eventsList'

import {
    mount,
    createLocalVue
} from '@vue/test-utils'
Vue.use(Vuetify);

const localVue = createLocalVue();

describe('TheStatusSnackbar.vue', () => {
    let vuetify

    beforeEach(() => {
        vuetify = new Vuetify()
    })

    it('Должен активироваться TheStatusSnackbar со статусом success', () => {
        const wrapper = mount(StatusSnackbar, {
            localVue,
            vuetify,
        })

        const eventParams = {
            status: 'success',
            message: 'Успешно!'
        }

        EventBus.$emit(OPEN_STATUS_ALERT, eventParams)

        const bar = wrapper.findComponent(StatusSnackbar)

        expect(bar.exists()).toBe(true)
        expect(bar.vm.color).toBe(eventParams.status)
        expect(bar.vm.message).toBe(eventParams.message)
    })

    it('Должен активироваться TheStatusSnackbar со статусом error', () => {
        const wrapper = mount(StatusSnackbar, {
            localVue,
            vuetify,
        })

        const eventParams = {
            status: 'error',
            message: 'Ошибка!'
        }

        EventBus.$emit(OPEN_STATUS_ALERT, eventParams)

        const bar = wrapper.findComponent(StatusSnackbar)

        expect(bar.exists()).toBe(true)
        expect(bar.vm.color).toBe('red')
        expect(bar.vm.message).toBe(eventParams.message)

    })
})