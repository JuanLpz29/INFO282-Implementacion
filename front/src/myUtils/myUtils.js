// let axios = require('axios');

import axios from 'axios';

const apiUrl = 'http://146.83.216.218:8008/'

var rqts = {
    async get(endpoint) {
        let items
        items = await axios.get(apiUrl + endpoint, { timeout: 3000 })
            .then(r => r.data)
            .catch(e => console.log(e))
        console.log('UTILSXD', items)
        return items
    },
    async post(endpoint, formdata) {
        let items
        items = await axios.post(apiUrl + endpoint, formdata, { timeout: 3000 })
            .then(r => r.data)
            .catch(e => console.log(e))
        console.log('UTILSXD', items)
        return items
    },
}
export default rqts
