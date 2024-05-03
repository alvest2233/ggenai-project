export default function SiteMessage(contents) {
    return (
        <iframe srcDoc={contents.sourceCode} width="100%" height="100%" />
    );
  }