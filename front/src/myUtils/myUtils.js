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
    },
}

var rqts = {
    async get(endpoint, timeout = TIMEOUT, debug = false) {
        console.log(endpoint)
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
        const url = xd.getUrl(debug)
        try {
            const items = await axios.post(url + endpoint, jsondata, { timeout: timeout })
            return items.data
        }
        catch (error) {
            console.log(error.response.data)
            return error.response.data.message
        }

    },

    async putjson(endpoint, jsondata, timeout = TIMEOUT, debug = false) {
        const url = xd.getUrl(debug)
        try {
            const items = await axios.put(url + endpoint, jsondata, { timeout: timeout })
            return items.data
        }
        catch (error) {
            console.log(error.response)
            //console.log(error.response.data)
            return error.response.data.message
        }
    },
    async loginxd(user, pass) {
        const login_info = {
            nombre: user,
            contraseña: pass,
        };
        const response = await rqts
            .postjson(`usuarios/login/`, login_info)
            .catch((e) => {
                console.log(e);
            });
        console.log(response);
        console.log(typeof response);
        if (typeof response == String) {
            console.log(response)
            return null;
        } else {
            return response;
        }
    }
}
export default rqts
