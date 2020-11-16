import axios from 'axios'


export default {

    fetchCompanyList() {
        return axios.get('/companies')
            .then(response => {
                return response.data
            });
    }
}