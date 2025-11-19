<script setup>
import { ref } from 'vue'
import FileUpload from '../components/FileUpload.vue'
import axios from 'axios'

const resumeFile = ref(null)
const resumeText = ref("")
const jdFiles = ref([])
const jdZip = ref(null)
const loading = ref(false)
const result = ref(null)
const error = ref(null)

const analyze = async () => {
  const hasResume = resumeFile.value || resumeText.value.trim()
  const hasJDs = jdFiles.value.length > 0 || jdZip.value

  if (!hasResume || !hasJDs) {
    error.value = "Please provide a resume (file or text) AND job descriptions (files or ZIP)."
    return
  }

  loading.value = true
  error.value = null
  result.value = null

  const formData = new FormData()
  
  if (resumeFile.value) {
    formData.append('resume_file', resumeFile.value)
  } else {
    formData.append('resume_text', resumeText.value)
  }
  
  for (let i = 0; i < jdFiles.value.length; i++) {
    formData.append('jd_files', jdFiles.value[i])
  }

  if (jdZip.value) {
    formData.append('jd_zip', jdZip.value)
  }

  try {
    const response = await axios.post('/api/find_jobs', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    result.value = response.data
  } catch (err) {
    error.value = err.response?.data?.error || "An error occurred during analysis."
    console.error(err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-5xl mx-auto space-y-12">
    <div class="text-center space-y-4">
      <h1 class="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white tracking-tight">Find Your Perfect Job</h1>
      <p class="text-base md:text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">Upload your resume and job descriptions to see which ones fit you best.</p>
    </div>

    <div class="bg-white dark:bg-slate-900 rounded-2xl p-6 md:p-8 space-y-6 border border-slate-200 dark:border-slate-800">
      
      <!-- Resume Section - Single Line -->
      <div class="space-y-3">
        <h3 class="text-sm font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Your Resume</h3>
        <div class="grid md:grid-cols-2 gap-4">
          <textarea 
            v-model="resumeText" 
            rows="4"
            class="w-full rounded-xl border-2 border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 transition-colors p-4 text-sm resize-none"
            placeholder="Paste your resume text here..."
          ></textarea>
          <div class="flex items-center justify-center">
            <FileUpload label="" v-model="resumeFile" accept=".pdf" />
          </div>
        </div>
      </div>

      <div class="border-t border-slate-200 dark:border-slate-800"></div>

      <!-- Job Descriptions -->
      <div class="space-y-3">
        <h3 class="text-sm font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Job Descriptions</h3>
        <div class="grid md:grid-cols-2 gap-4">
          <FileUpload label="Upload Files (PDF/TXT)" v-model="jdFiles" accept=".pdf,.txt" multiple />
          <FileUpload label="Or Upload ZIP" v-model="jdZip" accept=".zip" />
        </div>
      </div>
      
      <button 
        @click="analyze" 
        :disabled="loading"
        class="w-full flex justify-center items-center py-4 px-6 rounded-xl text-base font-semibold text-white bg-teal-600 hover:bg-teal-500 disabled:bg-slate-300 dark:disabled:bg-slate-800 disabled:text-slate-500 disabled:cursor-not-allowed transition-all transform active:scale-[0.99]"
      >
        <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        {{ loading ? 'Analyzing Matches...' : 'Find Matches' }}
      </button>

      <div v-if="error" class="p-4 bg-rose-50 dark:bg-rose-900/20 text-rose-600 dark:text-rose-400 rounded-xl border border-rose-100 dark:border-rose-900/30 flex items-center">
        <svg class="w-5 h-5 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
        {{ error }}
      </div>
    </div>

    <div v-if="result" class="space-y-8 animate-fade-in">
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-6 md:p-8 border border-slate-200 dark:border-slate-800">
        <div class="flex items-center mb-4">
          <div class="w-10 h-10 bg-teal-50 dark:bg-teal-900/30 rounded-lg flex items-center justify-center text-teal-600 dark:text-teal-400 mr-4">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          </div>
          <h2 class="text-xl font-bold text-slate-900 dark:text-white">Analysis Summary</h2>
        </div>
        <p class="text-slate-600 dark:text-slate-400 leading-relaxed">{{ result['Candidate Summary'] }}</p>
      </div>

      <div class="grid gap-6 md:grid-cols-2">
        <div v-for="job in result.Jobs" :key="job['Job Id']" class="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 hover:border-teal-500/50 dark:hover:border-teal-500/50 transition-all duration-300 flex flex-col h-full hover:-translate-y-1">
          <div class="flex justify-between items-start mb-4 gap-4">
            <div class="flex-1 min-w-0">
              <h3 class="text-lg font-bold text-slate-900 dark:text-white leading-tight">{{ job['Job Title'] }}</h3>
              <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">{{ job.Company }}</p>
            </div>
            <div class="flex flex-col items-end flex-shrink-0">
              <span class="text-2xl font-bold" :class="job['Suitability Score'] > 70 ? 'text-teal-500' : (job['Suitability Score'] > 40 ? 'text-yellow-500' : 'text-rose-500')">
                {{ job['Suitability Score'] }}%
              </span>
              <span class="text-xs text-slate-400 uppercase font-bold tracking-wider">Match</span>
            </div>
          </div>
          
          <p class="text-sm text-slate-600 dark:text-slate-400 mb-6 flex-grow line-clamp-3">{{ job['JD Summary'] }}</p>
          
          <div class="space-y-4 pt-4 border-t border-slate-100 dark:border-slate-800">
            <div>
              <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"/></svg>
                Key Matches
              </h4>
              <div class="flex flex-wrap gap-2">
                <span v-for="match in job.Matches" :key="match" class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-teal-50 dark:bg-teal-900/20 text-teal-700 dark:text-teal-400 border border-teal-100 dark:border-teal-900/30">
                  {{ match }}
                </span>
              </div>
            </div>
            <div>
              <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center">
                <svg class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
                Missing Skills
              </h4>
              <div class="flex flex-wrap gap-2">
                <span v-for="gap in job.Gaps" :key="gap" class="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-medium bg-rose-50 dark:bg-rose-900/20 text-rose-700 dark:text-rose-400 border border-rose-100 dark:border-rose-900/30">
                  {{ gap }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
