<template>
  <div class="home">
    <div class="hero">
      <img v-if="data.heroImage" :src="$withBase(data.heroImage)" alt="hero">
      <h1>{{ data.heroText || $title || 'Hello' }}</h1>
      <h1 v-if="data.heroSubText" >{{ data.heroSubText }}</h1>
      <p class="description">
        {{ data.tagline || $description || 'Welcome to your VuePress site' }}
      </p>
      <p class="action" v-if="data.actionText && data.actionLink">
        <NavLink class="action-button" :item="actionLink"/>
      </p>
    </div>
    <Content custom/>
    <div class="sponsors-container" v-if="data.sponsors && data.sponsors.length">
      <h2>Sponsors</h2>
      <div class="sponsors">
        <div class="sponsor" v-for="sponsor in data.sponsors">
          <!-- <h2>{{ sponsor.title }}</h2> -->
          <a :href="sponsor.link" >
              <img :src="$withBase(sponsor.image)" :alt="sponsor.title" />
          </a>
        </div>
      </div>
    </div>
    <div class="footer" v-if="data.footer">
      {{ data.footer }}
    </div>
  </div>
</template>

<script>
import NavLink from "./NavLink.vue";

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
@import './styles/config.styl';

.home {
  padding: $navbarHeight 2rem 0;
  max-width: 960px;
  margin: 0px auto;

  .hero {
    text-align: center;

    img {
      max-height: 280px;
      display: block;
      margin: 3rem auto 1.5rem;
    }

    h1 {
      font-size: 3rem;
    }

    h1, .description, .action {
      margin: 1.8rem auto;
    }

    .description {
      max-width: 35rem;
      font-size: 1.6rem;
      line-height: 1.3;
      color: lighten($textColor, 14%);
    }

    .action-button {
      display: inline-block;
      font-size: 1.2rem;
      color: #fff;
      background-color: $accentColor;
      padding: 0.8rem 1.6rem;
      border-radius: 4px;
      transition: background-color 0.1s ease;
      box-sizing: border-box;
      border-bottom: 1px solid darken($accentColor, 10%);

      &:hover {
        background-color: lighten($accentColor, 10%);
      }
    }
  }

  .sponsors-container {
    // border-top: 1px solid $borderColor;
    padding: 1.2rem 0;
    margin-top: 2.5rem;

      .sponsors {
        // border-top: 1px solid $borderColor;
        // padding: 1.2rem 0;
        // margin-top: 2.5rem;
        display: flex;
        flex-wrap: wrap;
        // align-items: flex-start;
        align-items: center;
        align-content: strech;
        // justify-content: space-between;
        justify-content: center;

        .sponsor {
          flex-grow: 1;
          flex-basis: 30%;
          max-width: 30%;
          margin: 10px;

          h2 {
            font-size: 1.4rem;
            font-weight: 500;
            border-bottom: none;
            padding-bottom: 0;
            color: lighten($textColor, 10%);
          }

          img {
            width: 100%;
            height: 100%;
          }
        }

      }
  }

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
  .home {
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
  .home {
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
