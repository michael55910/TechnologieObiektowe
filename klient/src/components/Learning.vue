<template>
  <div>
    <b-form inline>
      <b-input-group prepend="Para kryptowalut " class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="selectedPairSymbol" :options="pairs" text-field="symbol"
                       value-field="symbol"/>
      </b-input-group>
      <b-input-group prepend="Interwał" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="selectedInterval" :options="intervals"/>
      </b-input-group>
      <b-input-group prepend="Metoda" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-select v-model="selectedLearningMethod" :options="learningMethods"/>
      </b-input-group>
      <b-input-group prepend="Szerokość okna" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-input type="number" v-model="windowSize"/>
      </b-input-group>
      <b-input-group prepend="Ilość prognozowanych świeczek" class="mb-2 mr-sm-2 mb-sm-0">
        <b-form-input type="number" v-model="predictionSize"/>
      </b-input-group>

      <b-button variant="primary" @click="startLearning">Rozpocznij uczenie</b-button>
    </b-form>
  </div>
</template>

<script>
import DataService from "@/service/DataService";

export default {
  name: "Learning",
  props: {
    pairs: {
      type: Array,
      required: true
    },
    intervals: {
      type: Array,
      required: true
    },
    learningMethods: {
      type: Array,
      required: true
    },
  },
  data() {
    return {
      selectedPairSymbol: 'BNBBTC',
      selectedInterval: '1M',
      selectedLearningMethod: 'MLRW',
      windowSize: 10,
      predictionSize: 1,
      learningInProgress: false
    }
  },
  methods: {
    startLearning() {
      this.learningInProgress = true;
      // console.log(this.selectedLearningMethod);
      DataService.trainModel(this.selectedPairSymbol, this.selectedInterval, this.selectedLearningMethod, this.windowSize, this.predictionSize)
          .then(response => {
            if (response.status === 200) {
              console.log('Learning success');
            }
            this.learningInProgress = false;
          })
          .catch(error => {
            console.log(error);
          });
    }
  }
}
</script>

<style scoped>

</style>