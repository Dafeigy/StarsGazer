<template>
  <div class="min-h-screen bg-[#1C1C1C] text-white">
    <div class="flex">
      <!-- Sidebar -->
      <div class="w-64 h-screen fixed left-0 bg-[#242424] p-4 flex flex-col">
        <div class="flex items-center gap-2 px-2 mb-6">
          <!-- <img
            src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-yjUTK7xnJWwxK1IOit8kuKdR2PElSm.png"
            alt="Perplexity Logo"
            class="w-8 h-8"
          /> -->
          <span class="text-xl">StarsGazer</span>
        </div>
        
        <div class="flex items-center gap-2 px-2 py-1 text-gray-300 mb-4">
          <span class="text-sm">New Search</span>
          <span class="text-xs bg-[#3A3A3A] px-2 py-0.5 rounded">Ctrl + I</span>
        </div>
        
        <nav class="space-y-2 text-gray-300">
          <a href="#" class="flex items-center gap-2 px-2 py-2 rounded hover:bg-[#3A3A3A]">
            <Search class="w-5 h-5" />
            <span>首页</span>
          </a>
          <a href="#" class="flex items-center gap-2 px-2 py-2 rounded hover:bg-[#3A3A3A]">
            <Globe class="w-5 h-5" />
            <span>发现</span>
          </a>
          <a href="#" class="flex items-center gap-2 px-2 py-2 rounded hover:bg-[#3A3A3A]">
            <span class="w-5 h-5">◇</span>
            <span>空间</span>
          </a>
          <a href="#" class="flex items-center gap-2 px-2 py-2 rounded hover:bg-[#3A3A3A]">
            <span class="w-5 h-5">📚</span>
            <span>图书馆</span>
          </a>
        </nav>

        <div class="mt-auto space-y-2">
          <button class="w-full bg-[#00A3A3] hover:bg-[#008F8F] text-white px-4 py-2 rounded-md">
            注册
          </button>
          <button class="w-full text-gray-300 hover:bg-[#3A3A3A] px-4 py-2 rounded-md">
            登录
          </button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="ml-64 flex-1 p-4">
        <main class="max-w-3xl mx-auto mt-20">
          <h1 class="text-4xl font-medium text-center mb-8">Which star are you looking at?</h1>
          
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search Anything in your starred repo:"
              class="w-full bg-[#2A2A2A] border-gray-700 rounded-lg pl-4 pr-24 py-6 text-lg focus:outline-none focus:ring-2 focus:ring-[#00A3A3]"
            />
            <div class="absolute right-2 top-1/2 -translate-y-1/2 flex items-center gap-2">
              <button class="text-gray-400 hover:text-gray-300 px-2 py-1 rounded">
                Focus
              </button>
              <button class="text-gray-400 hover:text-gray-300 px-2 py-1 rounded">
                <Plus class="w-5 h-5" />
              </button>
              <div class="w-12 flex items-center justify-center border-l border-gray-700">
                <span class="text-sm text-gray-400">Pro</span>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
            <button
              v-for="(suggestion, index) in suggestions"
              :key="index"
              class="flex items-center gap-2 p-6 bg-[#2A2A2A] hover:bg-[#333333] rounded-lg justify-start text-left"
              @click="handleSuggestionClick(suggestion)"
            >
              <span class="text-2xl">{{ suggestion.icon }}</span>
              <span>{{ suggestion.text }}</span>
            </button>
          </div>
        </main>

        <footer class="fixed bottom-4 right-4 flex items-center gap-4 text-sm text-gray-400">
          <a
            v-for="(link, index) in footerLinks"
            :key="index"
            href="#"
            class="hover:text-gray-300"
          >
            {{ link }}
          </a>
          <div class="flex items-center gap-2">
            <span>Simplified Chinese (简体中文)</span>
            <button class="p-1 hover:bg-[#3A3A3A] rounded">
              <Globe class="w-4 h-4" />
            </button>
          </div>
        </footer>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Search, Globe, Plus } from 'lucide-vue-next'

const searchQuery = ref('')

const suggestions = ref([
  { icon: '🎯', text: '矩阵乘法的高效实现' },
  { icon: '🏠', text: '使用GPT生成ECharts图表' },
  { icon: '💫', text: '戴森球计划的计算器' },
  { icon: '🏛️', text: 'OAI开发的参考指南' }
])

const footerLinks = ref(['Pro', '企业', '商店', '博客', '职业'])

const handleSuggestionClick = (suggestion) => {
  searchQuery.value = suggestion.text
}
</script>

<style scoped>
/* Add any additional custom styles here */
input::placeholder {
  color: #6B7280;
}

/* Ensure smooth transitions */
.hover\:bg-\[\#3A3A3A\]:hover {
  transition: background-color 0.2s ease;
}

/* Ensure proper button focus states */
/* button:focus {
  outline: none;
  ring: 2px;
  ring-color: #00A3A3;
} */
</style>