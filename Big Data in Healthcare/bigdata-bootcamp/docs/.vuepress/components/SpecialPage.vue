<template>
  <div class="special-page">
    <Content custom/>
    <div class="footer" v-if="data.footer">
      {{ data.footer }}
    </div>
  </div>
</template>

<script>
import NavLink from "../theme/NavLink.vue";

export default {
  components: { NavLink },
  computed: {
    data() {
      return this.$page.frontmatter;
    },
    actionLink() {
      return {
        link: this.data.actionLink,
        text: this.data.actionText
      };
    }
  }
};
</script>

<style lang="stylus">
@import '../theme/styles/config.styl';

.special-page {
  padding: $navbarHeight 2rem 0;
  max-width: 960px;
  margin: 0px auto;

  .main-explain-area {
    font-family: 'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    padding: 15px inherit;
  }

  .jumbotron {
    padding: 30px 15px;
    margin-bottom: 30px;
    color: inherit;
    background-color: #eee;

    /* border */
    border: 1px solid;
    border-color: #ccc;
    border-radius: 10px;
    -moz-border-radius: 10px; /* Old Firefox */

    /* shadow */
    box-shadow: 3px 3px 3px #ddd;

    h1 {
      color: inherit;
    }

    p, ul {
      margin-bottom: 15px;
      font-size: 21px;
      font-weight: 200;
    }

    ul {
      list-style-type: none; /* remove bullets */
    }

    hr {
      border-top-color: #d5d5d5;
    }
  }

  .footer {
    padding: 2.5rem;
    border-top: 1px solid $borderColor;
    text-align: center;
    color: lighten($textColor, 25%);
  }
}

@media (max-width: $MQMobile) {
  .special-page {
    .sponsors {
      flex-direction: column;
    }

    .sponsor {
      max-width: 100%;
      padding: 0 2.5rem;
    }
  }
}

@media (max-width: $MQMobileNarrow) {
  .special-page {
    padding-left: 1.5rem;
    padding-right: 1.5rem;

    .hero {
      img {
        max-height: 210px;
        margin: 2rem auto 1.2rem;
      }

      h1 {
        font-size: 2rem;
      }

      h1, .description, .action {
        margin: 1.2rem auto;
      }

      .description {
        font-size: 1.2rem;
      }

      .action-button {
        font-size: 1rem;
        padding: 0.6rem 1.2rem;
      }
    }

    .sponsor {
      h2 {
        font-size: 1.25rem;
      }
    }
  }
}
</style>
