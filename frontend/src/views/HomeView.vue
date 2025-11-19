<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="flex flex-col items-center justify-center min-h-[80vh] text-center space-y-16">
    <div class="space-y-8 max-w-4xl animate-fade-in-up">
      <div class="inline-flex items-center px-4 py-2 rounded-full bg-slate-100 dark:bg-slate-900 text-slate-600 dark:text-slate-400 text-sm font-medium mb-4 border border-slate-200 dark:border-slate-800">
        <span class="flex h-2 w-2 rounded-full bg-teal-500 mr-2"></span>
        Powered by Google Gemini 2.5
      </div>
      <h1 class="text-5xl md:text-7xl font-bold text-slate-900 dark:text-white tracking-tight leading-tight">
        Hiring Reimagined with <span class="text-teal-600 dark:text-teal-400">AI Precision</span>
      </h1>
      <p class="text-xl text-slate-600 dark:text-slate-400 leading-relaxed max-w-2xl mx-auto">
        Instantly match resumes to job descriptions with deep semantic understanding. 
        Save hours of manual screening and find the perfect fit in seconds.
      </p>
    </div>

    <div class="grid md:grid-cols-2 gap-8 w-full max-w-5xl px-4">
      <!-- Candidate Card -->
      <RouterLink to="/candidate" class="group relative bg-white dark:bg-slate-900 p-10 rounded-2xl border border-slate-200 dark:border-slate-800 hover:border-teal-500/50 dark:hover:border-teal-500/50 transition-all duration-300 text-left overflow-hidden hover:-translate-y-1">
        <div class="relative z-10">
          <div class="w-12 h-12 bg-slate-100 dark:bg-slate-800 rounded-xl flex items-center justify-center mb-6 text-slate-900 dark:text-white group-hover:bg-teal-500 group-hover:text-white transition-colors duration-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" /></svg>
          </div>
          <h2 class="text-2xl font-bold text-slate-900 dark:text-white mb-3">For Candidates</h2>
          <p class="text-slate-500 dark:text-slate-400 mb-8 leading-relaxed">Upload your resume and find the best matching jobs from a list of descriptions. Get tailored advice on how to improve.</p>
          <span class="inline-flex items-center text-teal-600 dark:text-teal-400 font-semibold group-hover:translate-x-2 transition-transform duration-300">
            Find Your Match <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
          </span>
        </div>
      </RouterLink>

      <!-- HR Card -->
      <RouterLink to="/hr" class="group relative bg-white dark:bg-slate-900 p-10 rounded-2xl border border-slate-200 dark:border-slate-800 hover:border-teal-500/50 dark:hover:border-teal-500/50 transition-all duration-300 text-left overflow-hidden hover:-translate-y-1">
        <div class="relative z-10">
          <div class="w-12 h-12 bg-slate-100 dark:bg-slate-800 rounded-xl flex items-center justify-center mb-6 text-slate-900 dark:text-white group-hover:bg-teal-500 group-hover:text-white transition-colors duration-300">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" /></svg>
          </div>
          <h2 class="text-2xl font-bold text-slate-900 dark:text-white mb-3">For Recruiters</h2>
          <p class="text-slate-500 dark:text-slate-400 mb-8 leading-relaxed">Upload a job description and multiple resumes. Get an instant ranked list of candidates with detailed suitability scores.</p>
          <span class="inline-flex items-center text-teal-600 dark:text-teal-400 font-semibold group-hover:translate-x-2 transition-transform duration-300">
            Rank Candidates <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 8l4 4m0 0l-4 4m4-4H3"></path></svg>
          </span>
        </div>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
  opacity: 0;
  transform: translateY(20px);
}

@keyframes fadeInUp {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
