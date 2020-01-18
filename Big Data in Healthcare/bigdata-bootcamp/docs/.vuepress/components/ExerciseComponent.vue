<template>
    <!-- <div class="exercise">
        <h3>Exercise</h3>
        <div class="question tab">
            <span v-html="this.question"></span>
        </div>
        <button class="toggle-display" @click="toggleDisplay()">collapse</button>
        <div class="answer">
            <span v-if="this.display" v-html="this.answer"></span>
        </div>
        
    </div> -->
    <FlashCard
        headerFront="Exercise"
        headerBack=""
        footerFront=""
        footerBack=""
        :front="question" 
        :complexBack="answerContent" 
        />
</template>

<script>
import FlashCard from "./FlashCard.vue";

// export default {
//     props: ['question', 'answer'],
//     components : { FlashCard },
//     // data() {
//     //     return {
//     //         display: false,
//     //         displayMessage: 'Display The Answer'
//     //     }
//     // },
//     // methods: {
//     //     toggleDisplay () {
//     //         this.display = ! this.display
//     //     }
//     // }
// }

export default {
  mount() {
    console.log("Hello");
  },
  props: {
    question: {
      type: String,
      default: ""
    },
    answer: {
      type: String,
      default: ""
    }
  },
  data() {
    return {};
  },
  computed: {
    answerContent() {
      if (this.answer) {
        return [this.answer];
      } else {
        //   var content = this.$slots.default
        //   console.log("%o", content.length)
        //   console.log("%o", content)
        //   console.log("-----------------------------------")
        //   console.log("%o", content[0])
        return this.$slots.default;
      }
    }
  },
  components: { FlashCard }
};
</script>

<style lang="stylus">
@import '../theme/styles/config.styl'
</style>
