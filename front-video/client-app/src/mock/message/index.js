const Mock = require('mockjs');
const Random = Mock.Random;

import moment from 'moment'

const messageList = Mock.mock({
    'data|10': [{
      eventTime: () => Random.datetime(),
      content: () => Random.csentence(5, 10),
      id: () => Random.guid()
    }]
  })

function uuid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random()*16|0, v = c == 'x' ? r : (r&0x3|0x8);
    return v.toString(16);
  });
}

export function getMessageList() {
  return {
    code: 200,
    data: messageList.data
  }
}

export function addMessage() {
  let list = messageList.data
  list.push({
    eventTime: moment().format('yyyy-MM-DD HH:mm:ss'),
    content: Random.csentence(5, 10),
    id: uuid(),
  })

  return {
    code: 200,
    data: messageList.data
  }
}

