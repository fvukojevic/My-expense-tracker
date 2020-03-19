import axios from 'axios';

const state = {
    token: null,
    user: null
};

const mutations = {
    authUser: (state, userData) => {
        state.token = userData.SU;
    },
    storeUser: (state, userData) => {
        state.user = userData;
    },
    logout: (state) => {
        state.token = null;
        state.user = null;
    }
};

const actions = {
    login({commit, dispatch}, userData) {
        commit('authUser', userData);
        commit('storeUser', userData);
        localStorage.setItem('token', userData.SU);
        localStorage.setItem('userData', JSON.stringify(userData));
        dispatch('storeUserOnTheServer', userData);
        dispatch('setLogoutTimer', 300000) // 5 minutes timer
    },
    logout({commit}) {
        commit('logout');
        localStorage.removeItem('token');
        localStorage.removeItem('userData');
    },
    tryAutoLogin({commit, dispatch}) {
        const token = localStorage.getItem('token');
        if(!token) {
            return;
        }
        const userData = localStorage.getItem('userData');
        commit('authUser',  { SU: token, });
        commit('storeUser', JSON.parse(userData));
        dispatch('initCategories', token)
    },
    setLogoutTimer({dispatch}, expirationTime) {
        setTimeout(() => {
            dispatch('logout')
        }, expirationTime)
    },
    // eslint-disable-next-line no-empty-pattern
    storeUserOnTheServer({ dispatch }, userData) {
        const userServerData = {
            SU: userData.SU,
            Ad: userData.Ad,
            email: userData.zu
        };
        axios.post('/users', userServerData)
            .then(() => {
                dispatch('initCategories', userServerData.SU);
            })
    }
};

const getters = {
    getUser: state => {
        return state.user;
    },
    getToken: state => {
        return state.token;
    }
};

export default {
    state,
    getters,
    mutations,
    actions,
}
