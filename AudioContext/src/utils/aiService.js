import axios from 'axios';

const API_KEY = 'your_openai_api_key_here';
const API_URL = 'https://api.openai.com/v1/chat/completions';

export async function getAIResponse(prompt) {
  try {
    const response = await axios.post(API_URL, {
      model: "gpt-3.5-turbo",
      messages: [{ role: "user", content: prompt }]
    }, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      }
    });

    return response.data.choices[0].message.content;
  } catch (error) {
    console.error('Error getting AI response:', error);
    return '抱歉，我现在无法回答您的问题。';
  }
}