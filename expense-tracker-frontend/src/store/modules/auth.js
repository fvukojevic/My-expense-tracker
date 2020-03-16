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
        dispatch('setLogoutTimer', 300000) // 5 minutes timer
    },
    logout({commit}) {
        commit('logout');
        localStorage.removeItem('token');
        localStorage.removeItem('userData');
    },
    tryAutoLogin({commit}) {
        const token = localStorage.getItem('token');
        if(!token) {
            return;
        }
        const userData = localStorage.getItem('userData');
        console.log(userData);
        commit('authUser',  { SU: token, });
        commit('storeUser', JSON.parse(userData));
    },
    setLogoutTimer({dispatch}, expirationTime) {
        setTimeout(() => {
            dispatch('logout')
        }, expirationTime)
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
