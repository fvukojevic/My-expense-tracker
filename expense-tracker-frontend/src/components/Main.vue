<template>
    <div class="row">
        <div class="col-sm-12 col-md-12">
            <div v-if="user === null">
                <g-signin-button
                        :params="googleSignInParams"
                        @success="onSignInSuccess"
                        @error="onSignInError">
                    Sign in with Google
                </g-signin-button>
            </div>
            <div v-else>
                <div class="col-md-12 col-sm-12">
                    <h1>Logged in! Hello {{ user.Ad }}</h1>
                </div>
                <transition name="flip" mode="out-in">
                    <component :is="mode" :mode="mode" @changeMode="changeMode($event)"></component>
                </transition>
                <br><br>
                <div class="col-sm-12 col-md-12">
                    <button class="btn btn-primary" @click="logout">Logout</button>
                </div>
            </div>
        </div>
    </div>


</template>

<script>
    import NewExpense from './NewExpense';
    import MyExpenses from './MyExpenses';

    export default {
        data() {
            return {
                mode:'app-new-expense',
                googleSignInParams: {
                    client_id: '16343444389-7t654ig50s9rmrefv70utk3soljo2pie.apps.googleusercontent.com'
                }
            }
        },
        computed: {
            user() {
                return this.$store.getters.getUser;
            }
        },
        methods: {
            onSignInSuccess(googleUser) {
                const profile = googleUser.getBasicProfile(); // etc etc
                this.$store.dispatch('login', profile);
            },
            onSignInError() {
            },
            logout() {
                this.$store.dispatch('logout');
            },
            changeMode($event) {
                this.mode = $event[0];
            }
        },
        components: {
            appNewExpense: NewExpense,
            appMyExpenses: MyExpenses
        }
    }
</script>

<style scoped>
    .g-signin-button {
        /* This is where you control how the button looks. Be creative! */
        display: inline-block;
        cursor: pointer;
        padding: 4px 8px;
        border-radius: 3px;
        background-color: #3c82f7;
        color: #fff;
        box-shadow: 0 3px 0 #0f69ff;
    }

    .flip-enter-active {
        animation: flip-in 0.5s ease-out forwards;
    }

    .flip-leave-active {
        animation: flip-out 0.5s ease-out forwards;
    }

    @keyframes flip-out {
        from {
            transform: rotateY(0deg);
        }
        to {
            transform: rotateY(90deg);
        }
    }

    @keyframes flip-in {
        from {
            transform: rotateY(90deg);
        }
        to {
            transform: rotateY(0deg);
        }
    }
</style>