Vue.component("item", {
  props: ['name'],
  template: '<div class="ingredient">{{ name }}</div>'
});


Vue.component("drink-details", {
  props: ['drink', 'showList'],
  template: `
  <div>
    <template v-if="showList">
      <item
        v-for="ingredient in drink.ingredients"
        v-bind:key="ingredient.id"
        v-bind:name="ingredient.name"
      >
      </item>
      <item v-if="drink.garnish" v-bind:name="drink.garnish.name"></item>
      <item v-if="drink.technique" v-bind:name="drink.technique.name"></item>
      <item v-if="drink.container" v-bind:name="drink.container.name"></item>
    </template>
   </div>
   `
});


Vue.component("drink", {
  props: ['drink'],
  data: function() {
    return {
      showList: false
    }
  },
  methods: {
    toggleList: function() {
      this.showList = !this.showList
    }
  },
  template: `
    <div class="status">
      <div class="title" v-on:click="toggleList">
        <span>
          <span v-if="showList" class="toggler">-</span>
          <span v-else class="toggler">+</span>
        </span>
        {{ drink.name }}
      </div>
      <drink-details v-bind:drink="drink" v-bind:show-list="showList"></drink-details>
    </div>
  `
});


let url = '/api-graphql/';
let payload = {query: `
query {
  allDrinks {
    id
    name
    ingredients {
      id
      name
    }
    garnish {
      name
    }
    technique {
      name
    }
    container {
      name
    }
  }
}`};


let app = new Vue({
  el: "#app",
  data: {
    drinks: null
  },
  methods: {
    fetch_drinks() {
      fetch(url, {
        method: 'POST',
        body: JSON.stringify(payload),
        headers: { 'Content-Type': 'application/json' }
      })
        .then(response => response.json())
        .then(data => this.drinks = data["data"]["allDrinks"])
        .catch(error => console.error(error))
    }
  },
  created() {
    this.fetch_drinks()
  }

});
