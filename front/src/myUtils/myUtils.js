// let axios = require('axios');

import axios from 'axios';
const apiUrl = 'https://hiawvp.pythonanywhere.com/'
const localUrl = 'http://127.0.0.1:5000/'
const testing = false;
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
    async get(endpoint, params = null, timeout = TIMEOUT, debug = false) {
        const url = xd.getUrl(debug)
        try {
            // quizas axios maneje el params null y no sea encesario el ternero
            const items = params ?
                await axios.get(url + endpoint, { params: params }, { timeout: timeout }) :
                await axios.get(url + endpoint, { timeout: timeout })
            return items.data
        }
        catch (error) {
            console.log(error.response)
            return {
                statusText: error.response.statusText,
                message: error.response.data.message
            }
        }
    },
    async post(endpoint, formdata, timeout = TIMEOUT, debug = false) {
        const url = xd.getUrl(debug)
        try {
            const items = await axios.post(url + endpoint, formdata, { timeout: timeout })
            return items.data
        }
        catch (error) {
            console.log(error.response)
            return {
                statusText: error.response.statusText,
                message: error.response.data.message
            }
        }
    },
    async postjson(endpoint, jsondata, timeout = TIMEOUT, debug = false) {
        const url = xd.getUrl(debug)
        try {
            const items = await axios.post(url + endpoint, jsondata, { timeout: timeout })
            return items.data
        }
        catch (error) {
            console.log(error.response)
            return {
                statusText: error.response.statusText,
                message: error.response.data.message
            }
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
            return {
                statusText: error.response.statusText,
                message: error.response.data.message
            }
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
    },

    async getPaginatedResults(resource, page, filter, rowsPerPage, sortBy, order) {

        // Equivalent to `axios.get('https://httpbin.org/get?answer=42')`
        // const res = await axios.get('https://httpbin.org/get', { params: { answer: 42 } });
        const params = {
            page: page,
            filter: filter,
            perpage: rowsPerPage,
            sortby: sortBy,
            order: order
        }
        const response = await rqts.get(resource + '/', params)
        return response
    }

}
export default rqts
