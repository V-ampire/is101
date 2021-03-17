<template>
  <v-container>
    <v-row class="mb-4">
      <v-col cols="12">
        <h1 class="title">Филиал юрлица {{ branchInfo.company }}</h1>
        <h2 class="subtitle-2">
          Адрес филила: {{ branchInfo.city }}, {{ branchInfo.address }}
        </h2>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="5">
        <div class="d-flex flex-column">
          <v-card class="mb-3">
            <v-card-title class="subtitle-1">Статус филиала</v-card-title>
            <v-card-text>
              <BranchStatusForm
                v-if="!!branchInfo.status" 
                :currentStatus="branchInfo.status"
                :branchUuid="branchUuid"
                :companyUuid="companyUuid"
                @onReload="reloadData()"
              ></BranchStatusForm>
            </v-card-text>
          </v-card>
          <v-card>
            <v-card-title class="subtitle-1">Удалить филиал</v-card-title>
            <v-card-subtitle class="body-2 text-wrap-normal">
              При удалении фмлиала одновременно будет удалена вся информация о работниках этого филиала.
            </v-card-subtitle>
            <v-card-text>
              <v-btn 
                color="error"
                small
                block
                @click="deleteBranch()"
              >
                Удалить филиал
              </v-btn>
            </v-card-text>
          </v-card>
        </div>
      </v-col>
      <v-col cols="7">
        <v-card>
          <v-card-title class="subtitle-1">Редактировать информацию о филиале</v-card-title>
          <v-card-text>
            <EditBranchForm
              v-if="!!branchInfo"
              :companyUuid="companyUuid"
              :branchUuid="branchUuid"
              ref="editBranchForm"
            ></EditBranchForm>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12"></v-col>
    </v-row>
  </v-container>
</template>

<script>
import branchesApi from '@/core/services/http/branches';
import eventUtils from '@/core/services/events/utils';
import BranchStatusForm from '@/core/components/branches/BranchStatusForm';
import EditBranchForm from '@/core/components/branches/EditBranchForm';

export default {
  components: {
    BranchStatusForm: BranchStatusForm,
    EditBranchForm: EditBranchForm
  },
  data() {
    return {
      branchInfo: null,
    }
  },
  async mounted() {
    this.branchInfo = await this.getBranchInfo();
    await this.$nextTick(() => {
      this.$refs.editBranchForm.setInitial(this.branchInfo);
    });
  },
  computed: {
    branchUuid() {
      return this.$route.params.branchUuid;
    },
    companyUuid() {
      return this.$route.params.companyUuid;
    },
    api() {
      return branchesApi(this.companyUuid)
    }
  },
  methods: {
    async getBranchInfo() {
      let response;
      try {
        response = await this.api.detail(this.branchUuid);
      } catch (err) {
        eventUtils.showErrorAlert(err.message);
        throw err
      }
      if (response.data.uuid == this.branchUuid) {
        return response.data
      } else {
        eventUtils.showErrorAlert('Не удалось загрузить данные с сервера.');
        console.log(`Не удалось информацию о филиале. Получен ответ ${response}`);
      }
    },
    async reloadData() {
      this.branchInfo = await this.getBranchInfo();
      this.$refs.editBranchForm.setInitial(this.branchInfo);
    },
    deleteBranch() {
      const confirmParams = {
        message: `Вы действительно хотите удалить филиал ${this.companyInfo.title}?`
      }
      eventUtils.onConfirmAction(confirmParams, async (result) => {
        if (result) {
          try {
            await this.api.delete(this.companyUuid);
          } catch (err) {
            eventUtils.showErrorAlert(err.message);
            throw err
          }
          eventUtils.showSuccessEvent('Филиал удален!');
          eventUtils.offReloadEvent(this.reloadData);
          this.$router.push({name: 'CompanyDetail', params: {companyUuid: this.companyUuid}});
        }
      });
    }
  },
}
</script>