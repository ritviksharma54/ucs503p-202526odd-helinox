<script setup>
import { ref } from 'vue'
import FileUpload from '../components/FileUpload.vue'
import axios from 'axios'

const jdFile = ref(null)
const resumeFiles = ref([])
const resumeZip = ref(null)
const loading = ref(false)
const result = ref(null)
const error = ref(null)

const analyze = async () => {
  const hasResumes = resumeFiles.value.length > 0 || resumeZip.value

  if (!jdFile.value || !hasResumes) {
    error.value = "Please upload a job description and at least one resume (files or ZIP)."
    return
  }

  loading.value = true
  error.value = null
  result.value = null

  const formData = new FormData()
  formData.append('jd_file', jdFile.value)
  
  for (let i = 0; i < resumeFiles.value.length; i++) {
    formData.append('resumes', resumeFiles.value[i])
  }

  if (resumeZip.value) {
    formData.append('resume_zip', resumeZip.value)
  }

  try {
    const response = await axios.post('http://localhost:5000/api/analyze', formData, {
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
      <h1 class="text-3xl md:text-4xl font-bold text-slate-900 dark:text-white tracking-tight">Rank Candidates</h1>
      <p class="text-base md:text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto">Upload a job description and multiple resumes to find the best talent.</p>
    </div>

    <div class="bg-white dark:bg-slate-900 rounded-2xl p-6 md:p-8 space-y-6 border border-slate-200 dark:border-slate-800">
      
      <!-- Job Description -->
      <div class="space-y-3">
        <h3 class="text-sm font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Job Description</h3>
        <FileUpload label="Upload File (PDF/TXT)" v-model="jdFile" accept=".pdf,.txt" />
      </div>

      <div class="border-t border-slate-200 dark:border-slate-800"></div>

      <!-- Resumes -->
      <div class="space-y-3">
        <h3 class="text-sm font-semibold text-slate-700 dark:text-slate-300 uppercase tracking-wide">Candidate Resumes</h3>
        <div class="grid md:grid-cols-2 gap-4">
          <FileUpload label="Upload Files (PDF)" v-model="resumeFiles" accept=".pdf" multiple />
          <FileUpload label="Or Upload ZIP" v-model="resumeZip" accept=".zip" />
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
        {{ loading ? 'Analyzing Candidates...' : 'Rank Candidates' }}
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
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
          </div>
          <h2 class="text-xl font-bold text-slate-900 dark:text-white">Job Context</h2>
        </div>
        <p class="text-slate-600 dark:text-slate-400 leading-relaxed">{{ result['Job Description Summary'] }}</p>
      </div>

      <div class="space-y-6">
        <h2 class="text-2xl font-bold text-slate-900 dark:text-white">Ranked Candidates</h2>
        <div v-for="(candidate, index) in result.Candidates.sort((a, b) => b['Suitability Score'] - a['Suitability Score'])" :key="index" class="bg-white dark:bg-slate-900 rounded-2xl p-6 border border-slate-200 dark:border-slate-800 hover:border-teal-500/50 dark:hover:border-teal-500/50 transition-all duration-300 relative overflow-hidden hover:-translate-y-1">
          <div class="absolute top-0 left-0 w-1 h-full" :class="candidate['Suitability Score'] > 70 ? 'bg-teal-500' : (candidate['Suitability Score'] > 40 ? 'bg-yellow-500' : 'bg-rose-500')"></div>
          
          <div class="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 pl-4">
            <div class="flex items-center mb-4 md:mb-0">
              <div class="flex items-center justify-center w-10 h-10 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 font-bold mr-4 text-lg">
                {{ index + 1 }}
              </div>
              <div>
                <h3 class="text-xl font-bold text-slate-900 dark:text-white">{{ candidate['Candidate Name'] }}</h3>
                <p class="text-sm text-slate-500 dark:text-slate-400 font-medium">{{ candidate['Recent Job Titles']?.[0] }}</p>
              </div>
            </div>
            <div class="flex items-center pl-14 md:pl-0">
              <span class="text-3xl font-bold mr-2" :class="candidate['Suitability Score'] > 70 ? 'text-teal-500' : (candidate['Suitability Score'] > 40 ? 'text-yellow-500' : 'text-rose-500')">
                {{ candidate['Suitability Score'] }}%
              </span>
              <span class="text-xs text-slate-400 uppercase font-bold tracking-wider">Match</span>
            </div>
          </div>
          
          <div class="pl-4 md:pl-14">
            <p class="text-slate-600 dark:text-slate-400 mb-6 leading-relaxed bg-slate-50 dark:bg-slate-800/50 p-4 rounded-xl border border-slate-100 dark:border-slate-800 text-sm">
              {{ candidate.Reasoning }}
            </p>

            <div class="grid md:grid-cols-2 gap-6 text-sm mb-6">
              <div class="flex items-start">
                <svg class="w-5 h-5 text-slate-400 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222"/></svg>
                <div>
                  <span class="font-semibold text-slate-700 dark:text-slate-300 block">Education</span>
                  <span class="text-slate-600 dark:text-slate-400">{{ candidate.Education }}</span>
                </div>
              </div>
              <div class="flex items-start">
                <svg class="w-5 h-5 text-slate-400 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>
                <div>
                  <span class="font-semibold text-slate-700 dark:text-slate-300 block">Experience</span>
                  <span class="text-slate-600 dark:text-slate-400">{{ candidate['Years of Experience'] }}</span>
                </div>
              </div>
            </div>

            <div>
              <h4 class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">Key Skills</h4>
              <div class="flex flex-wrap gap-2">
                <span v-for="skill in candidate['Key Skills']" :key="skill" class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700">
                  {{ skill }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
