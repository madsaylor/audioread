<script setup>
import {ref, computed} from "vue";
import {Howl} from 'howler';


const text = ref('')
const textSent = ref(false)
const howlerObject = ref(null)
const audioMeta = ref({
  currentPosition: 0,
  words: [],
  start_time: [],
  end_time: [],
  audioUrl: ''
})

const currentWordIndex = ref(0)

function handleTimeupdate(event){
  const position = event.target.currentTime;
  const startTime = audioMeta.value.start_time.map((time, index) => ({ time, index }))
  .filter( item => position >= item.time).pop();
  currentWordIndex.value = startTime.index
}

function reset(){
  currentWordIndex.value = 0
  textSent.value = false
}

async function sendText() {
  try {
    const response = await fetch('/api/tts', {
      method: 'POST',
      body:text.value,
    });

    if (!response.ok) {
      throw new Error('Network response was not ok' + response.statusText);
    }
    const result = await response.json();
    audioMeta.value = Object.assign(
      {},
      audioMeta.value,
      {
        audioUrl: result.audioUrl,
        ...result.adjusted_alignment
      }
    )
    console.log(audioMeta.value)

    textSent.value = true
  } catch (error) {
    console.error('Error:', error);
  }
}

</script>

<template>
    <main>
      <nav class="navbar">
        <div class="container-fluid">
          <a class="navbar-brand ms-5" href="/">
            🧞‍♂️&nbsp;Book Genius
          </a>
        </div>
      </nav>
      <div>
        <div class="container-fluid bg-body-tertiary">
          <div class="col-md-8 p-lg-5 ms-1 mb-5">
            <h1 class="display-3 fw-bold">Make your own audiobook</h1>
            <h3 class="fw-normal text-muted mb-3">Convert any text to audio</h3>
          </div>
        </div>
        <div class="container mt-2">
          <div class="row">
            <div class="col-6 mx-auto" >
              <div v-if="!textSent">
                <div class="form-floating mb-3">
                  <textarea class="form-control" v-model="text" placeholder="Enter the text here" id="floatingTextarea2" style="min-height: 154px"></textarea>
                  <label for="floatingTextarea2">Enter the text here</label>
                </div>
                <button class="btn btn-primary w-25" @click="sendText">Listen</button>
              </div>
              <div v-if="textSent">
                <div style="min-height: 100px;" class="d-flex flex-row flex-wrap align-content-start" >
                  <span v-for="(word, index) in audioMeta.words" :id="`word${index}`"
                        :class="{'bg-info-subtle': index === currentWordIndex}">{{word}}&nbsp;</span>
                </div>
                <div class="d-flex mt-5">
                  <button class="btn btn-primary btn-sm me-1 w-25" @click="reset">Edit</button>
                  <audio id="audio-player" class="w-75"
                       :src="audioMeta.audioUrl" @timeupdate="handleTimeupdate" controls></audio>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
</template>

<style scoped>

</style>
