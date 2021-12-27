
<template>
  <div class="about">
    <p>{{ message }}</p>
    <h1>プロジェクト</h1>
    <v-form ref="form">
      <v-simple-table>
        <thead></thead>
        <tbody>
          <tr>
            <th>プロジェクト名称</th>
            <td>
              <v-text-field
                v-model="title"
                :counter="64"
                :rules="nameRules"
                :value="title"
                label="プロジェクト名称"
                required
              ></v-text-field>
            </td>
          </tr>
          <tr>
            <th>説明</th>
            <td>
              <v-menu v-model="menu" max-width="290px" min-width="290px">
                <!-- ポップアップを追加する要素にv-on="on" -->
                <template v-slot:activator="{ on }">
                  <v-text-field
                    v-model="description"
                    :counter="128"
                    :rules="nameRules"
                    :value="description"
                    label="説明"
                    required
              ></v-text-field>
                </template>
                <v-date-picker v-model="description"></v-date-picker>
              </v-menu>
            </td>
          </tr>
          
          <tr>
            <th>作成者</th>
            <td>
              <v-text-field
                v-model="created_by"
                :value="created_by"
                :counter="10"
                :rules="nameRules"
                label="作成者"
                required
              ></v-text-field>
            </td>
          </tr>
        </tbody>
      </v-simple-table>
      <v-btn class="mr-4" @click="submit">保存</v-btn>
      <v-btn @click="reset">リセット</v-btn>
    </v-form>
  </div>
</template>
<script>

var contentType = 'application/json'
var url = 'http://localhost:5000/api/project/create'
const config = {
  headers: {
    'Content-Type': contentType
  }
}

export default {
  name: 'project_create',
  data: function () {
    return {
      title: '',
      description: '',
      created_by: '',
      message: '出力メッセージ'
    }
  },
  computed: {
    form () {
      return {
        title: this.title,
        description: this.discription,
        operation_account_id: parseInt(this.created_by)
      }
    }
  },
  methods: {
    validate () {
      this.$refs.form.validate()
    },
    reset () {
      this.$refs.form.reset()
    },
    resetValidation () {
      this.$refs.form.resetValidation()
    },
    submit () {
      console.log(this.form)
      this.axios
        .post(url, this.form, config)
        .then(function (response) {
          console.log('Create axios response')
          console.log(response)
          document.location = 'http://localhost:8080/project'
        })
        .catch(err => {
          console.log('Create axios error')
          console.log(err)
        })
    },
    clear () {
      this.$v.$reset()
      this.title = ''
      this.description = ''
      this.created_by = ''
    }

  }
}
</script>
