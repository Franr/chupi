Vue.component("ingredient-item", {
  props: ['name'],
  template: '<div>{{ name }}</div>'
});

Vue.component("ingredient-list", {
  props: ['ingredients', 'showList'],
  template: `
  <div>
    <template v-if="showList">
      <ingredient-item
        v-for="ingredient in ingredients"
        class="ingredient"
        v-bind:key="ingredient.id"
        v-bind:name="ingredient.name"
      >
      </ingredient-item>
    </template>
   </div>
   `
});

Vue.component("drink", {
  props: ['name', 'ingredients'],
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
        {{ name }}
      </div>
      <ingredient-list v-bind:ingredients="ingredients" v-bind:show-list="showList"></ingredient-list>
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
  }
}`};

let app = new Vue({
  el: "#app",
  data: {
    drinks: null,
    loadedDrinks: false
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
