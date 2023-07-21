const Mock = require('mockjs');
import { getMessageList, addMessage } from './message'

Mock.setup({ timeout: 500 })

Mock.mock(/\/api\/messages/, 'get', getMessageList)
Mock.mock(/\/api\/messages/, 'post', addMessage)

