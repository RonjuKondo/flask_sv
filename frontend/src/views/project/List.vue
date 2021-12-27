<template>
  <div class="project_list">
    <p>{{ message }}</p>
    <h3>プロジェクト一覧</h3>
    <v-simple-table>
      <template v-slot;default>
        <thead>
          <tr>
            <th>編集</th>
            <th>プロジェクト名称</th>
            <th>説明</th>
            <th>作成者</th>
            <th>作成日時</th>
            <th>更新者</th>
            <th>更新日時</th>
            <th>ステータス</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="project in projects" v-bind:key="project.title">
            <td>
              <Update v-bind:project-title="project.title"></Update>
            </td>
            <td>{{ project.title }}</td>
            <td>{{ project.description }}</td>
            <td>{{ project.created_by }}</td>
            <td>{{ project.created_at }}</td>
            <td>{{ project.updated_by }}</td>
            <td>{{ project.updated_at }}</td>
            <td>{{ project.status }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </div>
</template>
<script>
import Update from '@/views/project/Update.vue'

var request = {
  operation_account_id: 100
}
var url = 'http://localhost:5000/api/project/search'
const config = {
  headers: {
    'Content-Type': 'application/json'
  }
}

export default {
  name: 'List',
  data () {
    return {
      projects: [],
      message: null
    }
  },
  mounted () {
    var self = this
    this.axios
      .post(url, request, config)
      .then(function (response) {
        console.log('List axios response %o', response.data.body)
        self.projects = response.data.body
        self.message = response.data.status.message
      })
      .catch(err => {
        console.log('List axios error')
        console.log(response)
        console.log(err)
      })
  },
  components: {
    Update
  }
}
</script>
