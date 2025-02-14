const routes = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: '', component: () => import('pages/IndexPage.vue') }
    ]
  },
  {
    path: '/myratings',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '', component: () => import('pages/MyRatingsPage.vue')}
    ]
  },
  {
    path: '/settings',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '', component: () => import('pages/SettingsPage.vue')}
    ]
  },
  {
    path: '/feedback',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '', component: () => import('pages/SendFeedbackPage.vue')}
    ]
  },
  {
    path: '/help',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '', component: () => import('pages/HelpPage.vue')}
    ]
  },
  {
    path: '/profile',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '', component: () => import('pages/ProfilePage.vue')}
    ]
  },
  {
    path: '/signup',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {path: '', component: () => import('pages/SignupPage.vue')}
    ]
  },
  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
