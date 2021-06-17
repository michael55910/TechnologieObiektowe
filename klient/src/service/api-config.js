import axios from "axios";

const API = axios.create({
    baseURL: "/api",
    headers: {
        "Content-type": "application/json",
    },
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFTOKEN"/*,
    withCredentials: true*/
})

/*fetch('http://localhost:8000/');*/

/*API.get('http://localhost:8000/', {withCredentials: true}).then().catch(() => {});*/


export default API;