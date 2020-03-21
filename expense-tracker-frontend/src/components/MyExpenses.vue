<template>
    <div id="signup">
        <div class="signup-form">
            <ul class="list-group">
                <li class="list-group-item" v-for="expense in userExpenses" :key="expense.id">{{expense.category_name}}: {{expense.amount}} €</li>
                <hr>
                <li class="list-group-item"><b>Total</b>: {{total}} €</li>
            </ul>
            <br><br>
            <datepicker v-model="range" range></datepicker>
            <br>
            <button class="button" type="button" @click="applyFilters"> Apply filters </button>
            <br><br>
            <button class="button" type="button" style="width:30%; margin-right:2em" @click="changeMode"> &#8592; Back </button>
            <a href="#" @click="download">Download Excel file</a>
        </div>
    </div>
</template>

<script>
    import datepicker from 'vue-date'

    export default {
        beforeCreate() {
            this.$store.dispatch('fetchUserExpenses')
        },
        created() {
            let today = new Date();
            let dd = String(today.getDate()).padStart(2, '0');
            let mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
            let yyyy = today.getFullYear();
            today = yyyy + '-' + mm + '-' + dd;
            this.range = ['2020-01-01', today]
        },
        computed: {
            userExpenses() {
                return this.$store.getters.getMyExpenses;
            },
            total() {
                let total = 0;
                if(this.userExpenses !== null) {
                    this.userExpenses.forEach((expense) => {
                        total += parseFloat(expense.amount);
                    });
                    return total;
                }
                return total
            },
        },
        data() {
            return {
                range: null
            }
        },
        methods: {
            applyFilters() {
                this.$store.dispatch('fetchUserExpensesFromTo', this.range);
            },
            changeMode() {
                this.$emit('changeMode', ['app-new-expense'])
            },
            download() {
                this.$store.dispatch('download', this.$store.getters.getToken)
            }
        },
        beforeDestroy() {
            this.changeMode()
        },
        components: { datepicker }
    }
</script>

<style scoped>
    .signup-form {
        width: 400px;
        margin: 30px auto;
        border: 1px solid #eee;
        padding: 20px;
        box-shadow: 0 2px 3px #ccc;
    }

    .input {
        margin: 10px auto;
    }

    .input label {
        display: block;
        color: #4e4e4e;
        margin-bottom: 6px;
    }

    .input.inline label {
        display: inline;
    }

    .input input {
        font: inherit;
        width: 100%;
        padding: 6px 12px;
        box-sizing: border-box;
        border: 1px solid #ccc;
    }

    .input.inline input {
        width: auto;
    }

    .input input:focus {
        outline: none;
        border: 1px solid #521751;
        background-color: #eee;
    }

    .input select {
        border: 1px solid #ccc;
        font: inherit;
    }

    .button {
        border: 1px solid #521751;
        width:80%;
        background: #521751;
        color: white;
        padding: 6px;
        font: inherit;
        cursor: pointer;
    }

    .button:hover,
    .button:active {
        background-color: #8d4288;
    }

    .categories input {
        width: 90%;
    }
</style>