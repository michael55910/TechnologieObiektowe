import Vue from "vue";
import Router from "vue-router";

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: "/",
            alias: "/home",
            name: "Home",
            component: () => import("./components/Home")
        }
    ]
});