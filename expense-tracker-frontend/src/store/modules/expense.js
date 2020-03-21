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
            .then(() => {
            })
    },
    fetchUserExpenses({getters, commit}) {
        const token = getters.getToken;
        axios.get('/expenses/' + token)
            .then((response) => {
                commit('setUserExpenses', response.data);
            })
    },
    fetchUserExpensesFromTo({getters, commit}, range) {
        const data = {
            'start_date': range[0],
            'end_date': range[1],
        };
        const token = getters.getToken;
        axios.post('/expenses/' + token, data)
            .then((response) => {
                commit('setUserExpenses', response.data);
            })
    },
    // eslint-disable-next-line no-empty-pattern
    download({}, token) {
        axios.get('/download/' + token).then((res) => {
            // eslint-disable-next-line no-console
            console.log(res)
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