<template>
    <div id="signup">
        <div class="signup-form">
            <form @submit.prevent="onSubmit">
                <div class="input" :class="{invalid: $v.amount.$error}">
                    <label for="expense">Enter new Amount</label>
                    <input
                            type="text"
                            id="expense"
                            @blur="$v.amount.$touch()"
                            v-model="amount">
                    <small v-if="$v.amount.$error">Amount must be a positive number</small>
                </div>
                <div class="input">
                    <label for="country">Categories</label>
                    <select class="form-control" id="country" v-model="selectedCategory">
                        <option v-for="category in categories" :key="category.id"> {{ category }}</option>
                        <option>Other</option>
                    </select>
                </div>
                <br><br>
                <div class="categories">
                    <h3>Category List</h3>
                    <button type="button" disabled>Add Category By Pressing &#10003;</button>
                    <div class="category-list">
                        <input
                                class="input"
                                type="text"
                                v-model="newCategory">
                        <button @click="addCategory()" type="button">&#10003;</button>
                        <small>Note: Every added category will be deleted after the form submit</small>
                    </div>
                </div>
                <br>
                <div class="submit">
                    <button type="submit" :disabled="$v.$invalid">Submit</button>
                    <button @click="changeMode" style="margin-left:2em">See My Expenses</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
    import {required} from "vuelidate/lib/validators";
    import expense from "../store/modules/expense";

    const validFloat = (expense) => {
        const castExpense = parseFloat(expense);
        if(isNaN(castExpense)) return false;
        return castExpense > 0;
    };

    export default {
        props: {
          mode: String,
        },
        data() {
            return {
                amount: null,
                selectedCategory: 'Other',
                newCategory: null,
            }
        },
        methods: {
            addCategory() {
                const categoryData = {
                    SU: this.user.SU,
                    name: this.newCategory
                };
                this.$store.dispatch('addCategory', categoryData);
            },
            changeMode() {
                this.$emit('changeMode', ['app-my-expenses'])
            },
            onSubmit() {
                const expenseData = {
                    SU: this.user.SU,
                    name: this.selectedCategory,
                    amount: this.amount
                };
                this.$store.dispatch('storeExpense', expenseData)
            }
        },
        computed: {
            user() {
                return this.$store.getters.getUser;
            },
            categories() {
                return this.$store.getters.getCategories;
            }
        },
        validations: {
            amount: {
                required,
                validFloat
            }
        }
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

    .categories button {
        border: 1px solid #521751;
        background: #521751;
        color: white;
        padding: 6px;
        font: inherit;
        cursor: pointer;
    }

    .categories button:hover,
    .categories button:active {
        background-color: #8d4288;
    }

    .categories input {
        width: 90%;
    }

    .submit button {
        border: 1px solid #521751;
        color: #521751;
        padding: 10px 20px;
        font: inherit;
        cursor: pointer;
    }

    .submit button:hover,
    .submit button:active {
        background-color: #521751;
        color: white;
    }

    .submit button[disabled],
    .submit button[disabled]:hover,
    .submit button[disabled]:active {
        border: 1px solid #ccc;
        background-color: transparent;
        color: #ccc;
        cursor: not-allowed;
    }

    .input.invalid label{
        color:red;
    }

    .input.invalid input {
        border: 1px solid red;
        background-color: #ffc9aa;
    }
</style>