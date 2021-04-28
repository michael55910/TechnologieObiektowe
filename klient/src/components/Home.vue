<template>
<b-card no-body>
    <b-tabs card>
      <b-tab title="Kursy" lazy active>
<!--        <b-card-text>Tab contents 1</b-card-text>-->
        <Rates/>
      </b-tab>
      <b-tab title="Porównanie" lazy>
        <Comparison/>
      </b-tab>
      <b-tab title="Przewidywania" lazy>
        <Predictions/>
      </b-tab>
      <b-tab title="Personalizacja" lazy>
        <Personalization/>
      </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
import Rates from "@/components/Rates";
import Comparison from "@/components/Comparison";
import Predictions from "@/components/Predictions";
import Personalization from "@/components/Personalization";
export default {
  name: "Home",
  components: {Personalization, Predictions, Comparison, Rates}
}
</script>

<style scoped>

</style>