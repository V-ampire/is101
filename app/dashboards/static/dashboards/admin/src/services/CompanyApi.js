import axios from 'axios'


export default {

    fetchAll() {
        return axios.get('/companies')
            .then(response => {
                return response.data
            });
    }
}