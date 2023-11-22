import './Markdown.css';
import { useState } from 'react';
import ReactMarkdown from 'react-markdown'
import gfm from 'remark-gfm'

function Markdown() {
  const [content, setContent] = useState('')
  function handleChange(e) {
      setContent(e.target.value)
  }
  return (
    <div className="box">
      <div className="column">
          <textarea rows="10" cols="25" defaultValue={content} onChange={handleChange}></textarea>
      </div>
      <div className="column">
        <ReactMarkdown remarkPlugins={[gfm]}>{content}</ReactMarkdown>
      </div>
    </div>
  );
}

export default Markdown;
