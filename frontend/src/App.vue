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

const audioLength = computed(() => {
  const arrayLength = audioMeta.value.end_time.length
  return arrayLength > 0?  audioMeta.value.end_time[arrayLength - 1]: 0
})

function playSound(){
  const sound = new Howl({
    src: [audioMeta.value.audioUrl]
  });
  sound.play();
}

function handleTimeupdate(event){
    console.log('Current time: ' + event.target.currentTime);
}

async function sendText() {
  try {
    const response = await fetch('http://localhost:8000/tts', {
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
                <div style="min-height: 100px;" >
                  <span v-for="(word, index) in audioMeta.words" :id="`word${index}`" cl>{{word}}&nbsp;</span>
                </div>
<!--                <div class="d-flex flex-row justify-content-between">-->
<!--                  <div>{{audioMeta.currentPosition}} / {{audioLength}}</div>-->
<!--                </div>-->
<!--                <input type="range" class="form-range" id="customRange1" v-model="audioMeta.currentPosition" min="0" :max="audioLength" step="0.01">-->
<!--                <button class="btn btn-primary me-1" @click="textSent = false">Edit</button>-->
<!--                <button class="btn btn-primary" @click="playSound">Play</button>-->
<!--                <button class="btn btn-primary ms-1" @click="audioMeta.currentPosition = 0">Replay</button>-->
                  <audio id="audio-player" :src="audioMeta.audioUrl" @timeupdate="handleTimeupdate" controls></audio>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
</template>

<style scoped>

</style>
