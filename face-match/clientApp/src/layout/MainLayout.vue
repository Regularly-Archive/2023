<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Navigation -->
    <nav class="sticky top-0 bg-white shadow z-10">
      <div class="container mx-auto px-4">
        <div class="flex justify-between h-12">
          <div class="flex">
            <!-- Logo -->
            <div class="flex-shrink-0 flex items-center">
              <h1 class="text-lg font-bold text-blue-600">Face Match</h1>
            </div>
            <!-- Navigation Links -->
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link 
                to="/search" 
                class="inline-flex items-center px-1 pt-0.5 border-b-2"
                :class="[$route.path === '/search' ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700']">
                以图搜图
              </router-link>
              <router-link 
                to="/upload" 
                class="inline-flex items-center px-1 pt-0.5 border-b-2"
                :class="[$route.path === '/upload' ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700']">
                人脸上传
              </router-link>
            
              <router-link 
                to="/manage" 
                class="inline-flex items-center px-1 pt-0.5 border-b-2"
                :class="[$route.path === '/manage' ? 'border-blue-500 text-gray-900' : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700']">
                图片管理
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Mobile menu -->
      <div class="sm:hidden">
        <div class="pt-1 pb-1 space-y-1">
          <router-link 
            to="/search" 
            class="block pl-3 pr-4 py-1.5 border-l-4 text-base font-medium"
            :class="[$route.path === '/search' ? 'bg-blue-50 border-blue-500 text-blue-700' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700']">
            搜索
          </router-link>
          <router-link 
            to="/upload" 
            class="block pl-3 pr-4 py-1.5 border-l-4 text-base font-medium"
            :class="[$route.path === '/upload' ? 'bg-blue-50 border-blue-500 text-blue-700' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700']">
            上传
          </router-link>
          <router-link 
            to="/manage" 
            class="block pl-3 pr-4 py-1.5 border-l-4 text-base font-medium"
            :class="[$route.path === '/manage' ? 'bg-blue-50 border-blue-500 text-blue-700' : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700']">
            管理
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="py-4 mt-12 overflow-auto">
      <router-view></router-view>
    </main>
  </div>
</template>

<script>
export default {
  name: 'MainLayout'
}
</script>
