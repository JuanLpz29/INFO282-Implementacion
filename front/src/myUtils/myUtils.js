// let axios = require('axios');

import axios from 'axios';
const apiUrl = 'http://146.83.216.218:8008/'
const localUrl = 'http://127.0.0.1:5000/'
const testing = false
const TIMEOUT = 10000;
var xd = {
    getUrl(isDebug) {
        let url
        if (isDebug || testing) {
            url = localUrl
        }
        else {
            url = apiUrl
        }
        return url
    }
}

var rqts = {
    async get(endpoint, timeout = TIMEOUT, debug = false) {
        let items
        const url = xd.getUrl(debug)
        items = await axios.get(url + endpoint, { timeout: timeout })
            .then(r => r.data)
            .catch(e => console.log(e))
        console.log('UTILSXD', items)
        return items
    },
    async post(endpoint, formdata, timeout = TIMEOUT, debug = false) {
        let items
        const url = xd.getUrl(debug)
        items = await axios.post(url + endpoint, formdata, { timeout: timeout })
            .then(r => r.data)
            .catch(e => console.log(e))
        console.log('UTILSXD', items)
        return items
    },
    async postjson(endpoint, jsondata, timeout = TIMEOUT, debug = false) {
        let response
        const url = xd.getUrl(debug)
        response = await axios.post(url + endpoint, jsondata, { timeout: timeout })
            .then(r => r.data)
            .catch(e => console.log(e))
        console.log('postjson', response)
        return response
    },
}
export default rqts
