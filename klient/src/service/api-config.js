import axios from "axios";

const API = axios.create({
    baseURL: "/api",
    headers: {
        "Content-Type": "application/json; charset=utf-8",
    },
    xsrfCookieName: "csrftoken",
    xsrfHeaderName: "X-CSRFToken",
    /*withCredentials: true*/
})

// fetch('http://localhost:8000/');
// fetch('/');

/*API.get('http://localhost:8000/', {withCredentials: true}).then().catch(() => {});*/


export default API;