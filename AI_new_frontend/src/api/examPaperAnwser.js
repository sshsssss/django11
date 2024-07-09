import { post } from '@/utils/request'

export default {
  page: query => post('/api/admin/examPaperAnswer/page', query),
  read: id => post('/api/student/exampaper/answer/read/' + id),
  edit: form => post('/api/student/exampaper/answer/edit', form)
}
