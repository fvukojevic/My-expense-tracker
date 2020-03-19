import axios from 'axios';

const state = {
    userExpenses: null,
};

const mutations = {
    setUserExpenses: (state, expenseData) => {
      state.userExpenses = expenseData
    }
};

const actions = {
    // eslint-disable-next-line no-empty-pattern
    storeExpense({}, expenseData) {
        axios.post('/expenses', expenseData)
            .then((response) => {
                // eslint-disable-next-line no-console
                console.log(response);
            })
    },
    fetchUserExpenses({getters, commit}) {
        const token = getters.getToken;
        axios.get('/expenses/' + token)
            .then((response) => {
                commit('setUserExpenses', response.data);
            })
    }
};

const getters = {
    getMyExpenses: state => {
      return state.userExpenses;
    }
};

export default {
    state,
    actions,
    mutations,
    getters
}