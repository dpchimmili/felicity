import { createApp } from 'vue'
import VueMarkdownIt from 'vue3-markdown-it';
import urql from '@urql/vue';
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import 'notyf/notyf.min.css';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { library, dom } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'

import LayoutDashboard from './views/layouts/LayoutDashboard.vue';
import LayoutEmpty from './views/layouts/LayoutEmpty.vue';

import './index.css'
import './assets/css/style.css'

import App from './App.vue'
import router from './router'
import store from './store'
import { graphql_url } from './conf'
import { urqlClient } from './urql'

library.add(fas, fab)
dom.watch()

const app = createApp(App)
app.component('font-awesome-icon', FontAwesomeIcon)
app.component('default-layout', LayoutDashboard)
app.component('empty-layout', LayoutEmpty)
app.use(urql, urqlClient)  // { url: graphql_url } replaces urqlClient
app.use(VueSweetalert2)
app.use(VueMarkdownIt)
app.use(router)
app.use(store)
app.mount('#app')