<script setup>
import { ref } from 'vue'

const props = defineProps({
  label: String,
  accept: {
    type: String,
    default: '.pdf,.txt'
  },
  multiple: {
    type: Boolean,
    default: false
  },
  modelValue: [File, Array, null]
})

const emit = defineEmits(['update:modelValue'])
const isDragging = ref(false)
const fileInput = ref(null)

const handleDrop = (e) => {
  isDragging.value = false
  const files = e.dataTransfer.files
  handleFiles(files)
}

const handleInput = (e) => {
  handleFiles(e.target.files)
}

const handleFiles = (files) => {
  if (props.multiple) {
    emit('update:modelValue', Array.from(files))
  } else {
    emit('update:modelValue', files[0] || null)
  }
}

const triggerClick = () => {
  fileInput.value.click()
}

const removeFile = (index = null) => {
  if (props.multiple) {
    const newFiles = [...props.modelValue]
    newFiles.splice(index, 1)
    emit('update:modelValue', newFiles)
  } else {
    emit('update:modelValue', null)
  }
}
</script>

<template>
  <div class="w-full group h-full flex flex-col">
    <label class="block text-sm font-semibold text-slate-700 dark:text-slate-300 mb-2 ml-1">{{ label }}</label>
    <div
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      @click="triggerClick"
      class="relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300 ease-in-out flex-grow flex flex-col items-center justify-center"
      :class="[
        isDragging 
          ? 'border-teal-500 bg-teal-50/50 dark:bg-teal-900/20 scale-[1.01]' 
          : 'border-slate-300 dark:border-slate-700 hover:border-teal-400 dark:hover:border-teal-500 hover:bg-slate-50 dark:hover:bg-slate-900 bg-white dark:bg-slate-950'
      ]"
    >
      <input
        ref="fileInput"
        type="file"
        class="hidden"
        :accept="accept"
        :multiple="multiple"
        @change="handleInput"
      />
      
      <div class="space-y-3 pointer-events-none">
        <div class="w-12 h-12 mx-auto bg-slate-100 dark:bg-slate-800 text-slate-400 dark:text-slate-500 rounded-xl flex items-center justify-center group-hover:scale-110 group-hover:text-teal-500 dark:group-hover:text-teal-400 transition-all duration-300">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
          </svg>
        </div>
        <div class="text-sm text-slate-600 dark:text-slate-400">
          <span class="font-semibold text-teal-600 dark:text-teal-400">Click to upload</span> or drag and drop
        </div>
        <p class="text-xs text-slate-400 dark:text-slate-500 uppercase tracking-wide">
          {{ accept.replace(/,/g, ' • ').replace(/\./g, '') }}
        </p>
      </div>
    </div>
    
    <!-- File List -->
    <div v-if="modelValue && (Array.isArray(modelValue) ? modelValue.length > 0 : true)" class="mt-4 space-y-2">
      <template v-if="multiple && Array.isArray(modelValue)">
        <div v-for="(file, index) in modelValue" :key="file.name" class="flex items-center justify-between p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <div class="flex items-center space-x-3 overflow-hidden">
            <div class="w-8 h-8 bg-teal-50 dark:bg-teal-900/30 text-teal-600 dark:text-teal-400 rounded flex items-center justify-center flex-shrink-0">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            </div>
            <span class="text-sm font-medium text-slate-700 dark:text-slate-300 truncate">{{ file.name }}</span>
          </div>
          <button @click.stop="removeFile(index)" class="p-1 text-slate-400 hover:text-rose-500 transition-colors rounded-full hover:bg-rose-50 dark:hover:bg-rose-900/20">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </template>
      
      <template v-else-if="!multiple && modelValue">
        <div class="flex items-center justify-between p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <div class="flex items-center space-x-3 overflow-hidden">
            <div class="w-8 h-8 bg-teal-50 dark:bg-teal-900/30 text-teal-600 dark:text-teal-400 rounded flex items-center justify-center flex-shrink-0">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>
            </div>
            <span class="text-sm font-medium text-slate-700 dark:text-slate-300 truncate">{{ modelValue.name }}</span>
          </div>
          <button @click.stop="removeFile()" class="p-1 text-slate-400 hover:text-rose-500 transition-colors rounded-full hover:bg-rose-50 dark:hover:bg-rose-900/20">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
      </template>
    </div>
  </div>
</template>
