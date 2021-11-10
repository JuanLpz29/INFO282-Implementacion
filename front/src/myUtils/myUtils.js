// let axios = require('axios');

import axios from 'axios';

const apiUrl = 'http://127.0.0.1:5000/'

var rqts = {
    async normal(endpoint) {
        let items
        items = await axios.get(apiUrl + endpoint, { timeout: 3000 })
            .then(r => r.data)
            .catch(e => console.log(e))
        console.log('UTILSXD', items)
        return items
    },
}
export default rqts
