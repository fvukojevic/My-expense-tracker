import axios from 'axios';

const state = {
    categories: []
};

const mutations = {
    setCategories: (state, categories) => {
        state.categories = categories;
    },
    appendCategory: (state, categoryName) => {
        state.categories.push(categoryName);
    }
};

const actions = {
    initCategories({commit}, userIdentifier) {
        const categories = [];
        axios.get('/categories')
            .then((response) => {
                const data = response.data;
                data.forEach((item) => {
                    categories.push(item.name)
                });
            }).then(() => {
            axios.get('/user/categories/' + userIdentifier)
                .then((response) => {
                    const data = response.data;
                    data.forEach((item) => {
                        categories.push(item.name)
                    });
                }).then(() => {
                    commit('setCategories', categories);
            });
        });
    },
    addCategory({commit}, categoryData) {
        axios.post('/user/categories/' + categoryData.SU, {name: categoryData.name})
            .then((response) => {
                if(response.data.statusCode === 200) {
                    commit('appendCategory', categoryData.name)
                } else {
                    // eslint-disable-next-line no-console
                    console.log(response)
                }
        })
    }
};

const getters = {
    getCategories: state => {
        return state.categories;
    }
};

export default {
    state,
    getters,
    mutations,
    actions,
}