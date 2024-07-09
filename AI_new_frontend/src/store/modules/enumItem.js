// initial state
const state = {
    user: {
      sexEnum: [{ key: 1, value: '男' }, { key: 2, value: '女' }],
      statusEnum: [{ key: 1, value: '启用' }, { key: 2, value: '禁用' }],
      levelEnum: [{ key: 1, value: '初级' }, { key: 2, value: '中级' }, { key: 3, value: '高级' }],
      roleEnum: [{ key: 1, value: '学生' }, { key: 3, value: '管理员' }],
      statusTag: [{ key: 1, value: 'success' }, { key: 2, value: 'danger' }],
      statusBtn: [{ key: 1, value: '禁用' }, { key: 2, value: '启用' }]
    },
    exam: {
      examPaper: {
        paperTypeEnum: [{ key: 1, value: '模拟考试' }, { key: 4, value: '定时考试' }, { key: 6, value: '任务考试' }]
      },
      question: {
        typeEnum: [{ key: 1, value: '单选题' }, { key: 2, value: '多选题' }, { key: 3, value: '判断题' }, { key: 4, value: '填空题' }, { key: 5, value: '简答题' }],
        editUrlEnum: [{ key: 1, value: '/exam/question/edit/singleChoice', name: '单选题' },
          { key: 2, value: '/exam/question/edit/multipleChoice', name: '多选题' },
          { key: 3, value: '/exam/question/edit/trueFalse', name: '判断题' },
          { key: 4, value: '/exam/question/edit/gapFilling', name: '填空题' },
          { key: 5, value: '/exam/question/edit/shortAnswer', name: '简答题' }]
      }
    }
  }
  
  // getters
  const getters = {
    enumFormat: (state) => (arrary, key) => {
      return format(arrary, key)
    }
  }
  
  // actions
  const actions = {}
  
  // mutations
  const mutations = {}
  
  const format = function (array, key) {
    for (let item of array) {
      if (item.key === key) {
        return item.value
      }
    }
    return null
  }
  
  export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  }
  