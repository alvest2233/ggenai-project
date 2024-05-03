import { useState } from 'react';
import MonacoEditor from 'react-monaco-editor';

export default function SiteMessage(contents) {
  const [showSource, setShowSource] = useState(false);

  const handleClick = () => {
    setShowSource(!showSource);
  };

  return (
    <div style={{ width: '600px', height: '400px' }}>
      <button onClick={handleClick}>
        Toggle Source Code
      </button>
      {showSource ? (
        <MonacoEditor
          width="100%"
          height="100%"
          language="html"
          theme="vs-dark"
          value={contents.sourceCode}
          options={{ readOnly: true }}
        />
      ) : (
        <iframe srcDoc={contents.sourceCode} width="100%" height="100%" />
      )}
    </div>
  );
}