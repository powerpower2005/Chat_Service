import Vue from 'vue'
import VueRouter from 'vue-router'
import LoginForm from '../components/LoginForm.vue'
import ChatRoomList from '../components/ChatRoomList.vue'
import ChatRoom from '../components/ChatRoom.vue'
import SignUpForm from '../components/SignUpForm.vue'
import AuthLayout from '../layouts/AuthLayout.vue'
import ChatLayout from '../layouts/ChatLayout.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: AuthLayout,
    children: [
      {
        path: '',
        name: 'Login',
        component: LoginForm
      }
    ]
  },
  {
    path: '/chat',
    component: ChatLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'ChatRoomList',
        component: ChatRoomList
      },
      {
        path: ':roomId',
        name: 'ChatRoom',
        component: ChatRoom,
        props: true,
        meta: { 
          requiresAuth: true,
          title: '채팅방',
          permissions: ['CHAT_ACCESS'],
          layout: 'chat'
        }
      }
    ]
  },
  {
    path: '/signup',
    name: 'SignUp',
    component: SignUpForm
  }
]

const router = new VueRouter({
  mode: 'history',
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const token = localStorage.getItem('token')
    if (!token) {
      next('/')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router 